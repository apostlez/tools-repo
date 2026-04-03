"""
Raw 데이터 분석 스크립트
데이터 특성을 파악하고 최적 전략 파라미터를 계산합니다.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from itertools import product

from src.indicators import calculate_all_indicators
from src.strategies import SignalType, PortfolioManager
from src.strategies.custom_strategies import MACDRSIOBVStrategy, RSIOBVStrategy
from src.strategies.sample_strategies import RSIStrategy, MACDStrategy
from config.trading_config import RISK_CONFIG

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "logs/raw_XRP_KRW_1m_2604032310.csv"
INITIAL_BALANCE = 200_000
FEE = 0.0005


# ─────────────────────────────────────────────
# 1. 데이터 로드 및 기본 통계
# ─────────────────────────────────────────────
def load_data(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df.set_index("timestamp", inplace=True)
    return df


def print_data_stats(df):
    close = df["close"]
    returns = close.pct_change().dropna()
    bb_ma = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    bb_upper = bb_ma + 2 * bb_std
    bb_lower = bb_ma - 2 * bb_std
    bb_width = ((bb_upper - bb_lower) / bb_ma).dropna()

    print("=" * 60)
    print("  Raw Data Analysis")
    print("=" * 60)
    print(f"캔들 수       : {len(df)}")
    print(f"기간          : {df.index[0]} ~ {df.index[-1]}")
    print(f"가격 범위     : {df['low'].min():.2f} ~ {df['high'].max():.2f} KRW")
    print(f"전체 변동폭   : {df['high'].max()-df['low'].min():.2f} KRW "
          f"({(df['high'].max()-df['low'].min())/close.mean()*100:.2f}%)")
    print(f"ATR(1분 평균) : {(df['high']-df['low']).mean():.4f} KRW")
    print(f"평균 거래량   : {df['volume'].mean():.2f}")
    print()
    print(f"수익률 std    : {returns.std()*100:.4f}%")
    print(f"수익률 최대   : {returns.max()*100:.4f}%  최소: {returns.min()*100:.4f}%")
    print(f"|ret| < 0.1%  : {(returns.abs()<0.001).sum()} "
          f"({(returns.abs()<0.001).mean()*100:.1f}%)")
    print(f"|ret| 0.1~0.3%: {((returns.abs()>=0.001)&(returns.abs()<0.003)).sum()}")
    print(f"|ret| 0.3~0.5%: {((returns.abs()>=0.003)&(returns.abs()<0.005)).sum()}")
    print(f"|ret| 0.5%+   : {(returns.abs()>=0.005).sum()}")
    print()
    print(f"BB 평균 밴드폭: {bb_width.mean()*100:.4f}%")
    print(f"BB 최대 밴드폭: {bb_width.max()*100:.4f}%")
    print(f"BB 하단 터치  : {(close < bb_lower).sum()}회")
    print(f"BB 상단 터치  : {(close > bb_upper).sum()}회")


# ─────────────────────────────────────────────
# 2. 공통 백테스트 엔진 (실제 봇과 동일 조건)
# ─────────────────────────────────────────────
def backtest(strategy, df_ind, symbol,
             stop_loss_pct, take_profit_pct,
             max_position_size, fee=FEE,
             precomputed=None, start_idx=None, verbose=False):
    portfolio = PortfolioManager(INITIAL_BALANCE)

    if start_idx is None:
        start_idx = max(30, len(df_ind) // 20)
        if hasattr(strategy, "min_bars") and callable(strategy.min_bars):
            start_idx = max(2, strategy.min_bars())

    for i in range(start_idx, len(df_ind)):
        current_df = df_ind.iloc[:i + 1]
        if precomputed is not None:
            n = len(current_df)
            strategy._precomputed = {k: v.iloc[:n] for k, v in precomputed.items()}
        signal = strategy.analyze(current_df, symbol)

        price = current_df["close"].iloc[-1]
        ts = current_df.index[-1]

        # Stop Loss / Take Profit 체크
        if portfolio.has_position(symbol):
            pos = portfolio.positions[symbol]
            ep = pos["entry_price"]
            if price <= ep * (1 - stop_loss_pct):
                portfolio.close_position(symbol, price * (1 - fee), ts)
                if verbose:
                    print(f"  SL | {ts} | {price:,.2f}")
                continue
            if price >= ep * (1 + take_profit_pct):
                portfolio.close_position(symbol, price * (1 - fee), ts)
                if verbose:
                    print(f"  TP | {ts} | {price:,.2f}")
                continue

        if signal.signal_type == SignalType.BUY and not portfolio.has_position(symbol):
            invest = portfolio.balance * max_position_size * signal.strength
            buy_price = price * (1 + fee)
            amount = invest / buy_price
            if amount * buy_price <= portfolio.balance:
                try:
                    portfolio.open_position(symbol, amount, buy_price, ts)
                    if verbose:
                        print(f"  BUY | {ts} | {price:,.2f} | str={signal.strength:.2f}")
                except ValueError:
                    pass

        elif signal.signal_type == SignalType.SELL and portfolio.has_position(symbol):
            portfolio.close_position(symbol, price * (1 - fee), ts)
            if verbose:
                print(f"  SELL| {ts} | {price:,.2f} | {signal.reason}")

    # 잔여 포지션 정리
    if portfolio.has_position(symbol):
        final = df_ind["close"].iloc[-1] * (1 - fee)
        portfolio.close_position(symbol, final, df_ind.index[-1])

    perf = portfolio.get_performance()
    return perf.get("return_pct", 0.0), perf.get("total_trades", 0)


# ─────────────────────────────────────────────
# 3. 파라미터 최적화
# ─────────────────────────────────────────────
def optimize_macd_rsi_obv(df_ind, symbol):
    print("\n" + "=" * 60)
    print("  MACDRSIOBVStrategy 파라미터 최적화")
    print("=" * 60)

    # 데이터 범위 기반으로 TP/SL 탐색 범위 결정
    # ATR ≈ 1.66 KRW, 가격 ≈ 2000 KRW → ATR/price ≈ 0.083%
    sl_grid  = [0.003, 0.005, 0.008, 0.01]          # 0.3% ~ 1%
    tp_grid  = [0.003, 0.005, 0.008, 0.01, 0.015]   # 0.3% ~ 1.5%
    fast_grid    = [5, 8, 12]
    slow_grid    = [13, 21, 26]
    signal_grid  = [3, 5, 7]
    rsi_buy_grid = [45, 50, 55, 60]
    rsi_sell_grid= [60, 65, 70]
    obv_grid     = [5, 10, 15]

    best_ret, best_params = -999, None
    results = []
    total = (len(fast_grid) * len(slow_grid) * len(signal_grid) *
             len(rsi_buy_grid) * len(rsi_sell_grid) * len(obv_grid) *
             len(sl_grid) * len(tp_grid))
    print(f"  탐색 조합 수: {total:,}")

    count = 0
    for fast, slow, sig, rb, rs, obv_ma, sl, tp in product(
            fast_grid, slow_grid, signal_grid,
            rsi_buy_grid, rsi_sell_grid, obv_grid,
            sl_grid, tp_grid):
        if fast >= slow:
            continue
        if rb >= rs:
            continue
        if tp <= sl:
            continue

        strategy = MACDRSIOBVStrategy(
            macd_fast=fast, macd_slow=slow, macd_signal=sig,
            rsi_period=9, rsi_buy_threshold=rb, rsi_sell_threshold=rs,
            obv_ma_period=obv_ma,
        )
        # precompute
        precomp = strategy._compute_indicators(df_ind)
        strategy._precomputed = precomp

        ret, trades = backtest(
            strategy, df_ind, symbol,
            stop_loss_pct=sl, take_profit_pct=tp,
            max_position_size=RISK_CONFIG.get("max_position_size", 0.5),
            precomputed=precomp,
        )
        results.append((ret, trades, fast, slow, sig, rb, rs, obv_ma, sl, tp))
        if ret > best_ret:
            best_ret = ret
            best_params = (fast, slow, sig, rb, rs, obv_ma, sl, tp)
        count += 1
        if count % 500 == 0:
            print(f"    [{count}/{total}] best so far: {best_ret:+.2f}%")

    results.sort(key=lambda x: -x[0])
    print(f"\n  TOP 10 파라미터:")
    print(f"  {'수익률':>8} {'거래수':>5} {'fast':>4} {'slow':>4} {'sig':>3} "
          f"{'rsi_b':>5} {'rsi_s':>5} {'obv':>4} {'sl':>6} {'tp':>6}")
    print("  " + "-" * 65)
    for r in results[:10]:
        ret, tr, f, sl_v, sg, rb, rs, ob, sl, tp = r
        print(f"  {ret:>+8.2f}% {tr:>5}  {f:>4} {sl_v:>4} {sg:>3} "
              f"{rb:>5} {rs:>5} {ob:>4} {sl*100:>5.2f}% {tp*100:>5.2f}%")

    return best_params


def optimize_rsi_obv(df_ind, symbol):
    print("\n" + "=" * 60)
    print("  RSIOBVStrategy 파라미터 최적화")
    print("=" * 60)

    sl_grid       = [0.003, 0.005, 0.008, 0.01]
    tp_grid       = [0.003, 0.005, 0.008, 0.01, 0.015]
    oversold_grid = [25, 30, 35, 40]
    overbought_grid = [60, 65, 70, 75]
    obv_grid      = [5, 10, 15, 20]

    best_ret, best_params = -999, None
    results = []

    for os_, ob_, obv_ma, sl, tp in product(
            oversold_grid, overbought_grid, obv_grid, sl_grid, tp_grid):
        if ob_ <= os_:
            continue
        if tp <= sl:
            continue
        strategy = RSIOBVStrategy(oversold=os_, overbought=ob_, obv_ma_period=obv_ma)
        ret, trades = backtest(
            strategy, df_ind, symbol,
            stop_loss_pct=sl, take_profit_pct=tp,
            max_position_size=RISK_CONFIG.get("max_position_size", 0.5),
        )
        results.append((ret, trades, os_, ob_, obv_ma, sl, tp))
        if ret > best_ret:
            best_ret = ret
            best_params = (os_, ob_, obv_ma, sl, tp)

    results.sort(key=lambda x: -x[0])
    print(f"\n  TOP 10 파라미터:")
    print(f"  {'수익률':>8} {'거래수':>5} {'oversold':>8} {'overbought':>10} "
          f"{'obv_ma':>6} {'sl':>6} {'tp':>6}")
    print("  " + "-" * 55)
    for r in results[:10]:
        ret, tr, os_, ob_, obv_ma, sl, tp = r
        print(f"  {ret:>+8.2f}% {tr:>5} {os_:>8} {ob_:>10} {obv_ma:>6} "
              f"{sl*100:>5.2f}% {tp*100:>5.2f}%")

    return best_params


# ─────────────────────────────────────────────
# 4. 메인
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n📂 파일: {CSV_PATH}")
    df = load_data(CSV_PATH)
    print_data_stats(df)

    # 기준 심볼
    basename = os.path.basename(CSV_PATH)
    parts = basename.replace(".csv", "").split("_")
    symbol = f"{parts[1]}/{parts[2]}" if len(parts) >= 3 else "XRP/KRW"

    df_ind = calculate_all_indicators(df.copy())

    # 최적화 실행
    best_macd = optimize_macd_rsi_obv(df_ind, symbol)
    best_rsi  = optimize_rsi_obv(df_ind, symbol)

    print("\n" + "=" * 60)
    print("  최적 파라미터 요약")
    print("=" * 60)
    if best_macd:
        f, sl_v, sg, rb, rs, ob, sl, tp = best_macd
        print(f"  MACDRSIOBVStrategy: fast={f} slow={sl_v} signal={sg} "
              f"rsi_buy={rb} rsi_sell={rs} obv_ma={ob} "
              f"stop_loss={sl*100:.2f}% take_profit={tp*100:.2f}%")
    if best_rsi:
        os_, ob_, obv_ma, sl, tp = best_rsi
        print(f"  RSIOBVStrategy    : oversold={os_} overbought={ob_} "
              f"obv_ma={obv_ma} stop_loss={sl*100:.2f}% take_profit={tp*100:.2f}%")
