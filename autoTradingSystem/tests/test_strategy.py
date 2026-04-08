"""
Strategy Testing Script
전략 테스트 및 검증 스크립트
"""

import sys
import os

# Windows 터미널 UTF-8 인코딩 설정 (이모지 출력 지원)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

import json
import time
import ccxt
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.indicators import calculate_all_indicators
from src.strategies import (
    RSIStrategy,
    MACDStrategy,
    MovingAverageCrossStrategy,
    OBVStrategy,
    SignalType,
    PortfolioManager
)
from src.strategies.custom_strategies import RSIOBVStrategy, MACDRSIOBVStrategy, BollingerScalpStrategy
from config.trading_config import RISK_CONFIG

# 환경 변수 로드
load_dotenv()

_RETRYABLE_ERRORS = (
    ccxt.NetworkError,
    ccxt.RequestTimeout,
    ccxt.ExchangeNotAvailable,
    ccxt.DDoSProtection,
)


def _fetch_with_retry(fn, *args, max_retries: int = 3, base_delay: float = 5.0, **kwargs):
    """
    네트워크 오류 시 지수 백오프(exponential backoff)로 재시도

    재시도 대상: NetworkError, RequestTimeout, ExchangeNotAvailable, DDoSProtection
    대기 시간: base_delay × 2^(attempt-1)  →  5s, 10s, 20s
    """
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except _RETRYABLE_ERRORS as e:
            last_exc = e
            delay = base_delay * (2 ** (attempt - 1))
            print(f"⚠️  Network error (attempt {attempt}/{max_retries}): {e} — retrying in {delay:.0f}s...")
            time.sleep(delay)
        except Exception:
            raise
    print(f"❌ All {max_retries} retries exhausted: {last_exc}")
    raise last_exc


def load_from_csv(csv_path: str) -> tuple[pd.DataFrame, str]:
    """
    CSV 파일에서 시장 데이터 로드

    Args:
        csv_path: CSV 파일 경로 (raw_XRP_KRW_1m_*.csv 형식)

    Returns:
        (OHLCV DataFrame, symbol 문자열)
    """
    print(f"\n📂 Loading market data from CSV: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    df.set_index('timestamp', inplace=True)

    # 파일명에서 심볼 추출: raw_XRP_KRW_1m_*.csv → XRP/KRW
    basename = os.path.basename(csv_path)  # raw_XRP_KRW_1m_2603290425.csv
    parts = basename.replace('.csv', '').split('_')  # ['raw', 'XRP', 'KRW', '1m', ...]
    if len(parts) >= 3 and parts[0] == 'raw':
        symbol = f"{parts[1]}/{parts[2]}"
    else:
        symbol = 'UNKNOWN/KRW'

    print(f"✅ Loaded {len(df)} candles  |  Symbol: {symbol}")
    print(f"   Period: {df.index[0]} ~ {df.index[-1]}")
    return df, symbol


def fetch_market_data(symbol: str = 'XRP/KRW', # XRP/KRW
                     timeframe: str = '1m',
                     limit: int = 200) -> pd.DataFrame:
    """
    Upbit 거래소에서 시장 데이터 가져오기
    
    Args:
        symbol: 거래 심볼 (예: 'XRP/KRW', 'BTC/KRW')
        timeframe: 시간 프레임 (1m, 5m, 15m, 1h, 4h, 1d)
        limit: 데이터 개수
        
    Returns:
        OHLCV DataFrame
    """
    print(f"\n📊 Fetching market data: {symbol} ({timeframe}) from Upbit")
    
    access_key = os.getenv('UPBIT_ACCESS_KEY')
    secret_key = os.getenv('UPBIT_SECRET_KEY')
    
    exchange = ccxt.upbit({
        'apiKey': access_key,
        'secret': secret_key,
        'enableRateLimit': True,
    })
    
    # OHLCV 데이터 가져오기 (Upbit 최대 200개 제한 → 배치로 수집 후 병합)
    BATCH = 200  # Upbit API 1회 최대 요청 수
    timeframe_ms = exchange.parse_timeframe(timeframe) * 1000

    # 첫 번째 요청: since 없이 호출 → Upbit가 가장 최신 캔들 반환
    all_ohlcv = _fetch_with_retry(exchange.fetch_ohlcv, symbol, timeframe, limit=BATCH)

    # limit > 200 이면 더 과거 배치를 이어서 수집
    while len(all_ohlcv) < limit:
        oldest_ts = all_ohlcv[0][0]
        since = oldest_ts - BATCH * timeframe_ms
        batch = _fetch_with_retry(exchange.fetch_ohlcv, symbol, timeframe, since=since, limit=BATCH)
        # 중복 제거: 이미 가진 것보다 과거 데이터만 유지
        batch = [c for c in batch if c[0] < oldest_ts]
        if not batch:
            break
        all_ohlcv = batch + all_ohlcv

    # 가장 최근 limit 개만 사용
    ohlcv = all_ohlcv[-limit:]

    # DataFrame 변환
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    print(f"✅ Fetched {len(df)} candles")
    print(f"   Period: {df.index[0]} ~ {df.index[-1]}")

    # Raw 데이터 저장
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    timestamp_tag = datetime.now().strftime('%y%m%d%H%M')
    safe_symbol = symbol.replace('/', '_')
    raw_path = os.path.join(logs_dir, f"raw_{safe_symbol}_{timeframe}_{timestamp_tag}.csv")
    df.to_csv(raw_path, encoding='utf-8')
    print(f"💾 Raw data saved → {raw_path}")

    return df


def test_strategy(strategy, df: pd.DataFrame, symbol: str):
    """
    전략 테스트 및 시그널 분석
    
    Args:
        strategy: 테스트할 전략
        df: 시장 데이터
        symbol: 거래 심볼
    """
    print(f"\n{'='*70}")
    print(f"  Testing Strategy: {strategy.name}")
    print(f"{'='*70}")
    
    # 전략 정보 출력
    info = strategy.get_info()
    print(f"\n📋 Strategy Info:")
    print(f"   Name: {info['name']}")
    print(f"   Parameters: {info['parameters']}")
    print(f"   Required Indicators: {info['required_indicators']}")
    
    # 지표 계산
    print(f"\n🔧 Calculating indicators...")
    df_with_indicators = calculate_all_indicators(df.copy())
    print(f"✅ Indicators calculated")
    
    # 시그널 생성
    print(f"\n🎯 Generating signal...")
    signal = strategy.analyze(df_with_indicators, symbol)
    
    print(f"\n📈 Signal Result:")
    print(f"   Type: {signal.signal_type.value}")
    print(f"   Price: {signal.price:,.2f} KRW")
    print(f"   Strength: {signal.strength:.2%}")
    print(f"   Reason: {signal.reason}")
    print(f"   Timestamp: {signal.timestamp}")
    
    # 최근 가격 정보
    current_price = df['close'].iloc[-1]
    price_change_24h = ((current_price - df['close'].iloc[-24]) / df['close'].iloc[-24] * 100) if len(df) >= 24 else 0
    
    print(f"\n💹 Market Info:")
    print(f"   Current Price: {current_price:,.2f} KRW")
    print(f"   24h Change: {price_change_24h:+.2f}%")
    print(f"   24h High: {df['high'].iloc[-24:].max():,.2f} KRW")
    print(f"   24h Low: {df['low'].iloc[-24:].min():,.2f} KRW")
    
    # 관련 지표 값 출력
    print(f"\n📊 Current Indicators:")
    if 'rsi_14' in df_with_indicators.columns:
        print(f"   RSI(14): {df_with_indicators['rsi_14'].iloc[-1]:.2f}")
    if 'macd' in df_with_indicators.columns:
        print(f"   MACD: {df_with_indicators['macd'].iloc[-1]:.4f}")
        print(f"   MACD Signal: {df_with_indicators['macd_signal'].iloc[-1]:.4f}")
        print(f"   MACD Histogram: {df_with_indicators['macd_histogram'].iloc[-1]:.4f}")
    if 'sma_20' in df_with_indicators.columns:
        print(f"   SMA(20): {df_with_indicators['sma_20'].iloc[-1]:,.2f} KRW")
    if 'sma_50' in df_with_indicators.columns:
        print(f"   SMA(50): {df_with_indicators['sma_50'].iloc[-1]:,.2f} KRW")


def run_backtest_simulation(strategy, df: pd.DataFrame, symbol: str, initial_balance: float = 10000):
    """
    백테스트 시뮬레이션 — 실제 봇(RiskManager)과 동일한 조건 적용:
      - 포지션 사이즈: 잔액 × max_position_size × signal.strength
      - Stop Loss / Take Profit: RISK_CONFIG 기준
      - 수수료: TRADING_FEE (단방향)

    Args:
        strategy: 테스트할 전략
        df: 시장 데이터
        symbol: 거래 심볼
        initial_balance: 초기 자본
    """
    # ── RISK_CONFIG 에서 봇과 동일한 파라미터 로드 ──────────────────
    max_position_size = RISK_CONFIG.get('max_position_size', 0.1)
    stop_loss_pct     = RISK_CONFIG.get('stop_loss_pct', 0.05)
    take_profit_pct   = RISK_CONFIG.get('take_profit_pct', 0.10)
    TRADING_FEE       = 0.0005  # Upbit taker fee 0.05%

    print(f"\n{'='*70}")
    print(f"  Backtest Simulation: {strategy.name}")
    print(f"{'='*70}")
    print(f"  ⚙️  Risk Config  | position_size={max_position_size*100:.0f}%  "
          f"stop_loss={stop_loss_pct*100:.1f}%  take_profit={take_profit_pct*100:.1f}%  "
          f"fee={TRADING_FEE*100:.3f}%")

    # 지표 계산
    df_with_indicators = calculate_all_indicators(df.copy())

    # 전략에 precompute 메서드가 있으면 전체 데이터로 미리 계산 (EWM 수렴 보장)
    if hasattr(strategy, 'precompute'):
        strategy.precompute(df_with_indicators)

    # 포트폴리오 매니저
    portfolio = PortfolioManager(initial_balance)

    print(f"\n💰 Initial Balance: {initial_balance:,.0f} KRW")
    print(f"📅 Period: {df.index[0]} ~ {df.index[-1]}")
    print(f"💱 Exchange: Upbit | Symbol: {symbol}")
    print(f"\n🔄 Running backtest...")

    _MAX_DEFER  = 3      # 매도 보류 최대 횟수 (bot 과 동일)
    _MIN_PROFIT = 0.005  # 최소 보장 수익률 0.5% (bot 과 동일)
    sell_defer_count = 0  # 매도 보류 횟수 카운터

    # 각 시점마다 시그널 확인 및 거래 실행
    if hasattr(strategy, 'min_bars') and callable(strategy.min_bars):
        start_idx = max(2, strategy.min_bars())
    else:
        start_idx = max(50, len(df_with_indicators) // 20)

    for i in range(start_idx, len(df_with_indicators)):
        current_df = df_with_indicators.iloc[:i+1]
        signal = strategy.analyze(current_df, symbol)

        current_price = current_df['close'].iloc[-1]
        current_time = current_df.index[-1]

        # ── Stop Loss / Take Profit 체크 (포지션 보유 중) ──────────
        if portfolio.has_position(symbol):
            pos = portfolio.positions[symbol]
            entry_price = pos['entry_price']

            stop_price   = entry_price * (1 - stop_loss_pct)
            target_price = entry_price * (1 + take_profit_pct)

            if current_price <= stop_price:
                trade_pnl = (current_price - entry_price) * pos['amount']
                pct = (current_price - entry_price) / entry_price * 100
                portfolio.close_position(symbol, current_price * (1 - TRADING_FEE), current_time)
                print(f"  🔴 STOP LOSS  | {current_time} | {current_price:,.2f} KRW")
                print(f"       ❌ Trade P&L : {trade_pnl:>+,.0f} KRW  ({pct:+.2f}%)")
                print(f"          Entry: {entry_price:,.2f} → SL: {stop_price:,.2f}")
                continue

            if current_price >= target_price:
                trade_pnl = (current_price - entry_price) * pos['amount']
                pct = (current_price - entry_price) / entry_price * 100
                portfolio.close_position(symbol, current_price * (1 - TRADING_FEE), current_time)
                print(f"  🔴 TAKE PROFIT | {current_time} | {current_price:,.2f} KRW")
                print(f"       ✅ Trade P&L : {trade_pnl:>+,.0f} KRW  ({pct:+.2f}%)")
                print(f"          Entry: {entry_price:,.2f} → TP: {target_price:,.2f}")
                continue

        # ── 매수 시그널 & 포지션 없음 ───────────────────────────────
        if signal.signal_type == SignalType.BUY and not portfolio.has_position(symbol):
            # 봇과 동일한 포지션 사이즈: 잔액 × max_position_size × signal.strength
            invest = portfolio.balance * max_position_size * signal.strength
            buy_price = current_price * (1 + TRADING_FEE)  # 수수료 적용
            amount = invest / buy_price
            if amount * buy_price > portfolio.balance:
                continue  # 잔액 부족 건너뜀
            try:
                portfolio.open_position(symbol, amount, buy_price, current_time)

                rsi_val = current_df['rsi_14'].iloc[-1] if 'rsi_14' in current_df.columns else float('nan')
                obv_val = current_df['obv'].iloc[-1] if 'obv' in current_df.columns else float('nan')

                print(f"  🟢 BUY  | {current_time} | {current_price:,.2f} KRW | Amount: {amount:.6f}")
                print(f"          Balance   : {portfolio.balance:,.0f} KRW (remaining after buy)")
                print(f"          Reason    : {signal.reason}")
                print(f"          Strength  : {signal.strength:.2%}")
                print(f"          SL: {buy_price*(1-stop_loss_pct):,.2f}  TP: {buy_price*(1+take_profit_pct):,.2f}")
                print(f"          RSI       : {rsi_val:.2f}" if not pd.isna(rsi_val) else "          RSI       : N/A")
                print(f"          OBV       : {obv_val:,.0f}" if not pd.isna(obv_val) else "          OBV       : N/A")
            except ValueError:
                pass

        # ── 매도 시그널 & 포지션 보유 ───────────────────────────────
        elif signal.signal_type == SignalType.SELL and portfolio.has_position(symbol):
            pos = portfolio.positions[symbol]
            entry_price = pos['entry_price']
            profit_pct_raw = (current_price - entry_price) / entry_price

            # 수익 0.5% 미만 시 최대 3회까지 매도 보류 (bot 과 동일 로직)
            if profit_pct_raw < _MIN_PROFIT and sell_defer_count < _MAX_DEFER:
                sell_defer_count += 1
                print(
                    f"  ⏸ SELL deferred ({sell_defer_count}/{_MAX_DEFER}) | {current_time} | "
                    f"profit={profit_pct_raw*100:+.3f}% < {_MIN_PROFIT*100:.1f}% "
                    f"| entry={entry_price:,.2f} current={current_price:,.2f}"
                )
            else:
                sell_defer_count = 0
                amount = pos['amount']
                sell_price = current_price * (1 - TRADING_FEE)
                trade_pnl = (sell_price - entry_price) * amount
                price_change_pct = (sell_price - entry_price) / entry_price * 100
                result_icon = "✅" if trade_pnl >= 0 else "❌"

                portfolio.close_position(symbol, sell_price, current_time)

                rsi_val = current_df['rsi_14'].iloc[-1] if 'rsi_14' in current_df.columns else float('nan')
                obv_val = current_df['obv'].iloc[-1] if 'obv' in current_df.columns else float('nan')

                print(f"  🔴 SELL | {current_time} | {current_price:,.2f} KRW")
                print(f"       {result_icon} Trade P&L : {trade_pnl:>+,.0f} KRW  ({price_change_pct:+.2f}%)")
                print(f"          Entry     : {entry_price:,.2f} KRW → Exit: {sell_price:,.2f} KRW")
                print(f"          Reason    : {signal.reason}")
                print(f"          RSI       : {rsi_val:.2f}" if not pd.isna(rsi_val) else "          RSI       : N/A")
                print(f"          OBV       : {obv_val:,.0f}" if not pd.isna(obv_val) else "          OBV       : N/A")

    # 남은 포지션 정리 (강제 청산)
    if portfolio.has_position(symbol):
        pos = portfolio.positions[symbol]
        entry_price = pos['entry_price']
        amount = pos['amount']
        final_price = df_with_indicators['close'].iloc[-1] * (1 - TRADING_FEE)
        final_time = df_with_indicators.index[-1]
        trade_pnl = (final_price - entry_price) * amount
        price_change_pct = (final_price - entry_price) / entry_price * 100
        result_icon = "✅" if trade_pnl >= 0 else "❌"

        portfolio.close_position(symbol, final_price, final_time)

        print(f"  🔴 SELL | {final_time} | {final_price:,.2f} KRW (Position closed at end)")
        print(f"       {result_icon} Trade P&L : {trade_pnl:>+,.0f} KRW  ({price_change_pct:+.2f}%)")
        print(f"          Entry     : {entry_price:,.2f} KRW → Exit: {final_price:,.2f} KRW")
    
    # 성과 출력
    performance = portfolio.get_performance()
    
    print(f"\n{'='*70}")
    print(f"  Backtest Results")
    print(f"{'='*70}")
    
    print(f"\n📊 Trading Statistics:")
    print(f"   Total Trades: {performance['total_trades']}")
    print(f"   Winning Trades: {performance.get('winning_trades', 0)}")
    print(f"   Losing Trades: {performance.get('losing_trades', 0)}")
    print(f"   Win Rate: {performance.get('win_rate', 0):.2f}%")
    
    print(f"\n💵 Financial Results:")
    print(f"   Initial Balance: {performance.get('initial_balance', initial_balance):>14,.0f} KRW")
    print(f"   Final Balance:   {performance.get('current_balance', initial_balance):>14,.0f} KRW")
    print(f"   Total Profit:    {performance.get('total_profit', 0):>+14,.0f} KRW")
    print(f"   Return: {performance.get('return_pct', 0):+.2f}%")
    
    if performance['total_trades'] > 0:
        print(f"\n📈 Trade Analysis:")
        print(f"   Average Profit: {performance['average_profit']:>+14,.0f} KRW")
        print(f"   Best Trade:     {performance['best_trade']:>+14,.0f} KRW")
        print(f"   Worst Trade:    {performance['worst_trade']:>+14,.0f} KRW")
    
    # Buy & Hold 비교
    buy_hold_return = ((df['close'].iloc[-1] - df['close'].iloc[50]) / df['close'].iloc[50]) * 100
    strategy_return = performance.get('return_pct', 0.0)
    print(f"\n🔄 Strategy vs Buy & Hold:")
    print(f"   Strategy Return: {strategy_return:+.2f}%")
    print(f"   Buy & Hold Return: {buy_hold_return:+.2f}%")
    print(f"   Outperformance: {(strategy_return - buy_hold_return):+.2f}%")

    trade_pnls = [round(t['profit'], 2) for t in portfolio.trade_history if t['type'] == 'SELL']

    # 차트 표시용 거래 이벤트 (timestamp는 문자열로 직렬화)
    def _ts_str(ts):
        return ts.strftime('%Y-%m-%d %H:%M:%S') if hasattr(ts, 'strftime') else str(ts)

    trade_events = []
    for t in portfolio.trade_history:
        ev = {
            'type': t['type'],
            'timestamp': _ts_str(t['timestamp']),
            'price': round(float(t['price']), 4),
        }
        if t['type'] == 'SELL':
            ev['profit_pct'] = round(float(t.get('profit_pct', 0.0)), 4)
        trade_events.append(ev)

    return performance, buy_hold_return, trade_pnls, trade_events

def main():
    """메인 함수"""
    print("="*70)
    print("  Auto Trading System - Strategy Testing")
    print("="*70)
    
    # 설정
    SYMBOL = 'XRP/KRW' # 'POLYX/KRW'          # ← 심볼 변경 시 여기만 수정 (예: 'BTC/KRW', 'ETH/KRW', 'XRP/KRW')
    TIMEFRAME = '1m'
    LIMIT = 400
    INITIAL_BALANCE = 1_000_000  # KRW

    # CSV 파일 경로가 인자로 전달된 경우 fetch 대신 로드
    csv_path = sys.argv[1] if len(sys.argv) >= 2 else None
    
    try:
        # 1. 시장 데이터 가져오기
        if csv_path:
            df, SYMBOL = load_from_csv(csv_path)
        else:
            df = fetch_market_data(SYMBOL, TIMEFRAME, LIMIT)

        # 2. 전략 인스턴스 생성 (단일 정의 — 시그널 분석과 백테스트 모두 동일 인스턴스 사용)
        #    ※ 파라미터를 변경할 때는 이 한 곳만 수정하면 됩니다.
        strategies = [
            RSIStrategy(oversold=40, overbought=70),
            MACDStrategy(),
            MovingAverageCrossStrategy(fast_period=20, slow_period=50),
            OBVStrategy(obv_ma_period=14, divergence_lookback=5),
            RSIOBVStrategy(oversold=40, overbought=70, obv_weight=0.7),
            MACDRSIOBVStrategy(
                macd_fast=8,          # 8  — fast EMA
                macd_slow=21,         # 21 — slow EMA
                macd_signal=3,        # 5→3: Signal 선 빠르게 → MACD Bullish 판정 더 선행
                rsi_period=4,         # 4 9  — 작을수록 빠르게 반응
                rsi_buy_threshold=62.0,   # 55→62: 매수 구간 확대
                rsi_sell_threshold=80.0,  # 74→80: XRP 1분봉 RSI(9)는 추세 시 80까지 자주 도달
                obv_ma_period=5,      # 8→5: OBV MA 빠르게 → 매수 진입 선행
            ),
#            BollingerScalpStrategy(
#                bb_period=20,
#                bb_std_mult=2.0,
#                rsi_period=9,
#                rsi_oversold=35.0,
#                rsi_overbought=65.0,
#                bb_width_threshold=0.003,
#            ),
        ]

        # 3. 각 전략 시그널 분석
        for strategy in strategies:
            test_strategy(strategy, df, SYMBOL)

        # 4. 백테스트 시뮬레이션 (위와 동일한 인스턴스 재사용 — 파라미터 불일치 원천 차단)
        summary = []  # 전략별 결과 수집
        all_trade_pnls = []
        all_trade_events = []
        for strategy in strategies:
            print("\n\n")
            print("="*70)
            print(f"  Running Backtest: {strategy.name}")
            print("="*70)
            perf, bhr, pnls, events = run_backtest_simulation(strategy, df, SYMBOL, INITIAL_BALANCE)
            summary.append({
                'name': strategy.name,
                'trades': perf['total_trades'],
                'wins': perf.get('winning_trades', 0),
                'losses': perf.get('losing_trades', 0),
                'win_rate': perf.get('win_rate', 0.0),
                'profit': perf.get('total_profit', 0.0),
                'return_pct': perf.get('return_pct', 0.0),
                'outperformance': perf.get('return_pct', 0.0) - bhr,
                'buy_hold_return': bhr,
            })
            all_trade_pnls.append(pnls)
            all_trade_events.append(events)

        # 5. 전략별 결과 요약
        print("\n\n")
        print("="*70)
        print("  \U0001f4ca Backtest Summary")
        print("="*70)
        print(f"  {'전략':<17} {'거래수':>5} {'승률':>7} {'수익(KRW)':>10} {'수익률':>5} {'vs B&H':>8}")
        print(f"  {'-'*65}")
        for r in summary:
            profit_str = f"{r['profit']:+,.2f}"
            print(
                f"  {r['name']:<22} {r['trades']:>5} {r['win_rate']:>8.1f}% "
                f"{profit_str:>12} {r['return_pct']:>+7.2f}% {r['outperformance']:>+7.2f}%"
            )
        print(f"  {'-'*65}")
        if summary:
            bhr_val = summary[0]['buy_hold_return']
            print(f"  {'Buy & Hold':22} {'':>5} {'':>8} {'':>12} {bhr_val:>+7.2f}%")
        
        # JSON 결과 저장
        _logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        os.makedirs(_logs_dir, exist_ok=True)
        _timestamp_tag = datetime.now().strftime('%y%m%d%H%M')
        _json_path = os.path.join(_logs_dir, f"backtest_{_timestamp_tag}.json")

        _df_ind = calculate_all_indicators(df.copy())
        _indicators = {'Current Price': float(df['close'].iloc[-1])}
        for _key, _col in [('RSI(14)', 'rsi_14'), ('MACD', 'macd'),
                            ('MACD Signal', 'macd_signal'), ('MACD Hist', 'macd_histogram'),
                            ('SMA(20)', 'sma_20'), ('SMA(50)', 'sma_50')]:
            if _col in _df_ind.columns:
                _indicators[_key] = round(float(_df_ind[_col].iloc[-1]), 4)

        _result = {
            'symbol': SYMBOL,
            'period': f"{df.index[0].strftime('%Y-%m-%d %H:%M')} ~ {df.index[-1].strftime('%Y-%m-%d %H:%M')}",
            'initial_balance': INITIAL_BALANCE,
            'buy_and_hold_return': round(summary[0]['buy_hold_return'], 4) if summary else 0.0,
            'strategies': {
                r['name']: {
                    'trades': r['trades'],
                    'wins': r['wins'],
                    'losses': r['losses'],
                    'return_pct': round(r['return_pct'], 4),
                    'profit': round(r['profit'], 2),
                    'vs_bh': round(r['outperformance'], 4),
                }
                for r in summary
            },
            'trade_pnl': {
                r['name']: pnls
                for r, pnls in zip(summary, all_trade_pnls)
            },
            'trade_events': {
                r['name']: evs
                for r, evs in zip(summary, all_trade_events)
            },
            'current_indicators': _indicators,
        }

        with open(_json_path, 'w', encoding='utf-8') as _f:
            json.dump(_result, _f, indent=2, ensure_ascii=False)
        print(f"\n💾 Backtest results saved → {_json_path}")

        print("\n" + "="*70)
        print("  ✅ All tests completed successfully!")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
