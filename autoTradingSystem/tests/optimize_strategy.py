"""
Strategy Parameter Optimizer
각 전략의 최적 파라미터를 그리드 서치로 탐색하는 스크립트

사용법:
    python tests/optimize_strategy.py logs/raw_XRP_KRW_1m_2604032310.csv

탐색 항목:
    - 전략별 파라미터 (oversold, overbought, MACD 기간 등)
    - 리스크 파라미터 (stop_loss_pct, take_profit_pct)
"""

import sys
import os
import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Any

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.indicators import calculate_all_indicators
from src.strategies import (
    RSIStrategy, MACDStrategy, MovingAverageCrossStrategy,
    OBVStrategy, SignalType, PortfolioManager,
)
from src.strategies.custom_strategies import RSIOBVStrategy, MACDRSIOBVStrategy, BollingerScalpStrategy

INITIAL_BALANCE = 1_000_000
TRADING_FEE     = 0.0005   # Upbit taker 0.05%
TOP_N           = 5        # 전략별 상위 N개 출력


# ─────────────────────────────────────────────────────────────────────────────
# Core backtest (SL/TP 오버라이드 가능)
# ─────────────────────────────────────────────────────────────────────────────

def backtest_core(
    strategy,
    df_ind: pd.DataFrame,
    symbol: str,
    max_position_size: float,
    stop_loss_pct: float,
    take_profit_pct: float,
) -> Dict[str, Any]:
    """전략 + 리스크 파라미터 조합으로 백테스트 실행 후 성과 딕셔너리 반환"""

    portfolio = PortfolioManager(INITIAL_BALANCE)

    if hasattr(strategy, 'min_bars') and callable(strategy.min_bars):
        start_idx = max(2, strategy.min_bars())
    else:
        start_idx = max(50, len(df_ind) // 20)

    for i in range(start_idx, len(df_ind)):
        current_df   = df_ind.iloc[:i + 1]
        current_price = current_df['close'].iloc[-1]
        current_time  = current_df.index[-1]

        # ── Stop Loss / Take Profit 체크 ──────────────────────────────
        if portfolio.has_position(symbol):
            pos          = portfolio.positions[symbol]
            entry_price  = pos['entry_price']
            stop_price   = entry_price * (1 - stop_loss_pct)
            target_price = entry_price * (1 + take_profit_pct)

            if current_price <= stop_price:
                portfolio.close_position(symbol, current_price * (1 - TRADING_FEE), current_time)
                continue
            if current_price >= target_price:
                portfolio.close_position(symbol, current_price * (1 - TRADING_FEE), current_time)
                continue

        signal = strategy.analyze(current_df, symbol)

        # ── 매수 ─────────────────────────────────────────────────────
        if signal.signal_type == SignalType.BUY and not portfolio.has_position(symbol):
            invest    = portfolio.balance * max_position_size * signal.strength
            buy_price = current_price * (1 + TRADING_FEE)
            amount    = invest / buy_price
            if amount * buy_price > portfolio.balance:
                continue
            try:
                portfolio.open_position(symbol, amount, buy_price, current_time)
            except ValueError:
                pass

        # ── 매도 ─────────────────────────────────────────────────────
        elif signal.signal_type == SignalType.SELL and portfolio.has_position(symbol):
            sell_price = current_price * (1 - TRADING_FEE)
            portfolio.close_position(symbol, sell_price, current_time)

    # 남은 포지션 강제 청산
    if portfolio.has_position(symbol):
        final_price = df_ind['close'].iloc[-1] * (1 - TRADING_FEE)
        portfolio.close_position(symbol, final_price, df_ind.index[-1])

    perf = portfolio.get_performance()
    total_trades = perf.get('total_trades', 0)
    return {
        'return_pct':   round(perf.get('return_pct', 0.0), 4),
        'win_rate':     round(perf.get('win_rate', 0.0), 2),
        'total_trades': total_trades,
        'total_profit': round(perf.get('total_profit', 0.0), 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 그리드 서치
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class GridResult:
    strategy_name: str
    params: Dict[str, Any]
    result: Dict[str, Any]

    @property
    def return_pct(self):
        return self.result['return_pct']


def grid_search(name, factory_fn, param_grid, risk_grid, df_ind, symbol) -> List[GridResult]:
    """param_grid × risk_grid 모든 조합을 백테스트하여 결과 리스트 반환"""
    results = []
    param_keys   = list(param_grid.keys())
    param_values = list(param_grid.values())
    risk_keys    = list(risk_grid.keys())
    risk_values  = list(risk_grid.values())

    total = 1
    for v in param_values + risk_values:
        total *= len(v)
    print(f"\n  [{name}] 탐색 조합 수: {total}")

    for p_combo in itertools.product(*param_values):
        p_dict = dict(zip(param_keys, p_combo))
        strategy = factory_fn(**p_dict)
        # precompute는 파라미터 조합당 한 번만 실행 (리스크 루프에서 재사용)
        if hasattr(strategy, 'precompute'):
            strategy.precompute(df_ind)

        for r_combo in itertools.product(*risk_values):
            r_dict   = dict(zip(risk_keys, r_combo))
            res      = backtest_core(
                strategy, df_ind, symbol,
                max_position_size=r_dict['max_position_size'],
                stop_loss_pct=r_dict['stop_loss_pct'],
                take_profit_pct=r_dict['take_profit_pct'],
            )
            results.append(GridResult(
                strategy_name=name,
                params={**p_dict, **r_dict},
                result=res,
            ))

    results.sort(key=lambda x: x.return_pct, reverse=True)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# 파라미터 그리드 정의
# ─────────────────────────────────────────────────────────────────────────────

RISK_GRID = {
    'max_position_size': [0.3, 0.5, 0.8],
    'stop_loss_pct':     [0.005, 0.01],
    'take_profit_pct':   [0.005, 0.01, 0.02],
}

STRATEGY_GRIDS = {
    'RSIStrategy': {
        'factory': lambda **p: RSIStrategy(**p),
        'params': {
            'oversold':   [25, 30, 35],
            'overbought': [65, 70, 80],
        },
    },
    'MACDStrategy': {
        # MACDStrategy.analyze()는 사전 계산된 고정 macd_histogram 컬럼을 사용하므로
        # 파라미터 변경이 실제 계산에 영향 없음 → 리스크 파라미터만 탐색
        'factory': lambda **p: MACDStrategy(),
        'params': {},
    },
    'MovingAverageCrossStrategy': {
        # calculate_all_indicators는 sma_20, sma_50, sma_200만 계산하므로
        # 해당 값만 탐색 (fast < slow 조합만 유효)
        'factory': lambda **p: MovingAverageCrossStrategy(**p),
        'params': {
            'fast_period': [20],
            'slow_period': [50, 200],
        },
    },
    'OBVStrategy': {
        'factory': lambda **p: OBVStrategy(**p),
        'params': {
            'obv_ma_period':       [5, 10, 20],
            'divergence_lookback': [3, 5],
        },
    },
    'RSIOBVStrategy': {
        'factory': lambda **p: RSIOBVStrategy(**p),
        'params': {
            'oversold':    [25, 35],
            'overbought':  [65, 75],
            'obv_weight':  [0.3, 0.5, 0.7],
        },
    },
    'MACDRSIOBVStrategy': {
        'factory': lambda **p: MACDRSIOBVStrategy(**p),
        'params': {
            'macd_fast':          [5, 8],
            'macd_slow':          [15, 21],
            'macd_signal':        [3, 5],
            'rsi_buy_threshold':  [50.0, 55.0],
            'rsi_sell_threshold': [60.0, 70.0],
        },
    },
    'BollingerScalpStrategy': {
        'factory': lambda **p: BollingerScalpStrategy(**p),
        'params': {
            'bb_period':      [10, 20],
            'bb_std_mult':    [1.5, 2.0],
            'rsi_period':     [7, 9],
            'rsi_oversold':   [30, 35],
            'rsi_overbought': [60, 65],
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 출력 헬퍼
# ─────────────────────────────────────────────────────────────────────────────

def print_top(results: List[GridResult], top_n: int, buy_hold: float):
    SEP = '─' * 80
    print(f"\n  {'순위':<4} {'수익률':>7}  {'승률':>6}  {'거래수':>5}  {'수익(KRW)':>10}  파라미터")
    print(f"  {SEP}")
    for rank, r in enumerate(results[:top_n], 1):
        p_str = '  '.join(f"{k}={v}" for k, v in r.params.items())
        print(
            f"  #{rank:<3} {r.result['return_pct']:>+7.3f}%  "
            f"{r.result['win_rate']:>5.1f}%  "
            f"{r.result['total_trades']:>5}  "
            f"{r.result['total_profit']:>+10.0f}  "
            f"{p_str}"
        )
    print(f"  {SEP}")
    print(f"  Buy & Hold: {buy_hold:+.3f}%")


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    csv_path = sys.argv[1] if len(sys.argv) >= 2 else None
    if not csv_path:
        print("Usage: python tests/optimize_strategy.py <csv_path>")
        sys.exit(1)

    print("=" * 80)
    print("  Strategy Parameter Optimizer")
    print("=" * 80)
    print(f"  CSV: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    df.set_index('timestamp', inplace=True)

    # 파일명에서 심볼 추출
    basename = os.path.basename(csv_path)
    parts = basename.replace('.csv', '').split('_')
    symbol = f"{parts[1]}/{parts[2]}" if len(parts) >= 3 and parts[0] == 'raw' else 'XRP/KRW'

    df_ind = calculate_all_indicators(df.copy())

    # Buy & Hold 수익률
    buy_hold = (df['close'].iloc[-1] - df['close'].iloc[50]) / df['close'].iloc[50] * 100

    print(f"\n  심볼: {symbol}  |  캔들: {len(df)}  |  B&H: {buy_hold:+.3f}%")
    print(f"  기간: {df.index[0]} ~ {df.index[-1]}")

    all_best: List[GridResult] = []

    for name, cfg in STRATEGY_GRIDS.items():
        print(f"\n{'='*80}")
        print(f"  최적화 중: {name}")
        print(f"{'='*80}")
        results = grid_search(name, cfg['factory'], cfg['params'], RISK_GRID, df_ind, symbol)
        print_top(results, TOP_N, buy_hold)
        if results:
            all_best.append(results[0])

    # 전략 간 최종 비교
    print(f"\n\n{'='*80}")
    print("  전략별 최적 파라미터 요약")
    print(f"{'='*80}")
    print(f"  {'전략':<28} {'수익률':>8}  {'승률':>6}  {'거래수':>5}  최적 SL/TP")
    print(f"  {'─'*76}")
    all_best.sort(key=lambda x: x.return_pct, reverse=True)
    for r in all_best:
        sl  = r.params.get('stop_loss_pct', 0) * 100
        tp  = r.params.get('take_profit_pct', 0) * 100
        print(
            f"  {r.strategy_name:<28} {r.return_pct:>+8.3f}%  "
            f"{r.result['win_rate']:>5.1f}%  {r.result['total_trades']:>5}  "
            f"SL={sl:.1f}%  TP={tp:.1f}%"
        )
    print(f"  {'─'*76}")
    print(f"  {'Buy & Hold':<28} {buy_hold:>+8.3f}%")

    print("\n✅ 최적화 완료")


if __name__ == '__main__':
    main()
