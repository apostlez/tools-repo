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
from src.strategies.custom_strategies import RSIOBVStrategy

# 환경 변수 로드
load_dotenv()


def fetch_market_data(symbol: str = 'XRP/KRW', 
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
    all_ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=BATCH)

    # limit > 200 이면 더 과거 배치를 이어서 수집
    while len(all_ohlcv) < limit:
        oldest_ts = all_ohlcv[0][0]
        since = oldest_ts - BATCH * timeframe_ms
        batch = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=BATCH)
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
    간단한 백테스트 시뮬레이션
    
    Args:
        strategy: 테스트할 전략
        df: 시장 데이터
        symbol: 거래 심볼
        initial_balance: 초기 자본
    """
    print(f"\n{'='*70}")
    print(f"  Backtest Simulation: {strategy.name}")
    print(f"{'='*70}")
    
    # 지표 계산
    df_with_indicators = calculate_all_indicators(df.copy())
    
    # 포트폴리오 매니저
    portfolio = PortfolioManager(initial_balance)
    
    print(f"\n💰 Initial Balance: {initial_balance:,.0f} KRW")
    print(f"📅 Period: {df.index[0]} ~ {df.index[-1]}")
    print(f"💱 Exchange: Upbit | Symbol: {symbol}")
    print(f"\n🔄 Running backtest...")
    
    # 각 시점마다 시그널 확인 및 거래 실행
    for i in range(50, len(df_with_indicators)):  # 충분한 데이터 확보 후 시작
        current_df = df_with_indicators.iloc[:i+1]
        signal = strategy.analyze(current_df, symbol)
        
        current_price = current_df['close'].iloc[-1]
        current_time = current_df.index[-1]
        
        # 매수 시그널 & 포지션 없음
        if signal.signal_type == SignalType.BUY and not portfolio.has_position(symbol):
            # 전체 잔액의 95% 사용 (수수료 고려)
            amount = (portfolio.balance * 0.95) / current_price
            try:
                portfolio.open_position(symbol, amount, current_price, current_time)

                rsi_val = current_df['rsi_14'].iloc[-1] if 'rsi_14' in current_df.columns else float('nan')
                obv_val = current_df['obv'].iloc[-1] if 'obv' in current_df.columns else float('nan')

                print(f"  🟢 BUY  | {current_time} | {current_price:,.2f} KRW | Amount: {amount:.6f}")
                print(f"          Balance   : {portfolio.balance:,.0f} KRW (remaining after buy)")
                print(f"          Reason    : {signal.reason}")
                print(f"          Strength  : {signal.strength:.2%}")
                print(f"          RSI       : {rsi_val:.2f}" if not pd.isna(rsi_val) else "          RSI       : N/A")
                print(f"          OBV       : {obv_val:,.0f}" if not pd.isna(obv_val) else "          OBV       : N/A")
            except ValueError as e:
                pass  # 잔액 부족 등
        
        # 매도 시그널 & 포지션 보유
        elif signal.signal_type == SignalType.SELL and portfolio.has_position(symbol):
            pos = portfolio.positions[symbol]
            entry_price = pos['entry_price']
            amount = pos['amount']
            trade_pnl = (current_price - entry_price) * amount
            price_change_pct = (current_price - entry_price) / entry_price * 100
            result_icon = "✅" if trade_pnl >= 0 else "❌"

            portfolio.close_position(symbol, current_price, current_time)

            rsi_val = current_df['rsi_14'].iloc[-1] if 'rsi_14' in current_df.columns else float('nan')
            obv_val = current_df['obv'].iloc[-1] if 'obv' in current_df.columns else float('nan')

            print(f"  🔴 SELL | {current_time} | {current_price:,.2f} KRW")
            print(f"       {result_icon} Trade P&L : {trade_pnl:>+,.0f} KRW  ({price_change_pct:+.2f}%)")
            print(f"          Entry     : {entry_price:,.2f} KRW → Exit: {current_price:,.2f} KRW")
            print(f"          Reason    : {signal.reason}")
            print(f"          RSI       : {rsi_val:.2f}" if not pd.isna(rsi_val) else "          RSI       : N/A")
            print(f"          OBV       : {obv_val:,.0f}" if not pd.isna(obv_val) else "          OBV       : N/A")

    # 남은 포지션 정리
    if portfolio.has_position(symbol):
        pos = portfolio.positions[symbol]
        entry_price = pos['entry_price']
        amount = pos['amount']
        final_price = df_with_indicators['close'].iloc[-1]
        final_time = df_with_indicators.index[-1]
        trade_pnl = (final_price - entry_price) * amount
        price_change_pct = (final_price - entry_price) / entry_price * 100
        result_icon = "✅" if trade_pnl >= 0 else "❌"

        portfolio.close_position(symbol, final_price, final_time)

        print(f"  🔴 SELL | {final_time} | {final_price:,.2f} KRW (Position closed)")
        print(f"       {result_icon} Trade P&L : {trade_pnl:>+,.0f} KRW  ({price_change_pct:+.2f}%)")
        print(f"          Entry     : {entry_price:,.2f} KRW → Exit: {final_price:,.2f} KRW")
    
    # 성과 출력
    performance = portfolio.get_performance()
    
    print(f"\n{'='*70}")
    print(f"  Backtest Results")
    print(f"{'='*70}")
    
    print(f"\n📊 Trading Statistics:")
    print(f"   Total Trades: {performance['total_trades']}")
    print(f"   Winning Trades: {performance['winning_trades']}")
    print(f"   Losing Trades: {performance['losing_trades']}")
    print(f"   Win Rate: {performance['win_rate']:.2f}%")
    
    print(f"\n💵 Financial Results:")
    print(f"   Initial Balance: {performance['initial_balance']:>14,.0f} KRW")
    print(f"   Final Balance:   {performance['current_balance']:>14,.0f} KRW")
    print(f"   Total Profit:    {performance['total_profit']:>+14,.0f} KRW")
    print(f"   Return: {performance['return_pct']:+.2f}%")
    
    if performance['total_trades'] > 0:
        print(f"\n📈 Trade Analysis:")
        print(f"   Average Profit: {performance['average_profit']:>+14,.0f} KRW")
        print(f"   Best Trade:     {performance['best_trade']:>+14,.0f} KRW")
        print(f"   Worst Trade:    {performance['worst_trade']:>+14,.0f} KRW")
    
    # Buy & Hold 비교
    buy_hold_return = ((df['close'].iloc[-1] - df['close'].iloc[50]) / df['close'].iloc[50]) * 100
    print(f"\n🔄 Strategy vs Buy & Hold:")
    print(f"   Strategy Return: {performance['return_pct']:+.2f}%")
    print(f"   Buy & Hold Return: {buy_hold_return:+.2f}%")
    print(f"   Outperformance: {(performance['return_pct'] - buy_hold_return):+.2f}%")
    return performance, buy_hold_return

def main():
    """메인 함수"""
    print("="*70)
    print("  Auto Trading System - Strategy Testing")
    print("="*70)
    
    # 설정
    SYMBOL = 'XRP/KRW'
    TIMEFRAME = '1m'
    LIMIT = 400
    INITIAL_BALANCE = 1_000_000  # KRW (1,000,000원 = 약 $700 상당의 현실적 테스트 자금)
    
    try:
        # 1. 시장 데이터 가져오기
        df = fetch_market_data(SYMBOL, TIMEFRAME, LIMIT)

        # 2. 전략 인스턴스 생성 (단일 정의 — 시그널 분석과 백테스트 모두 동일 인스턴스 사용)
        #    ※ 파라미터를 변경할 때는 이 한 곳만 수정하면 됩니다.
        strategies = [
            RSIStrategy(oversold=30, overbought=70),
            MACDStrategy(),
            MovingAverageCrossStrategy(fast_period=20, slow_period=50),
            OBVStrategy(obv_ma_period=20, divergence_lookback=5),
            RSIOBVStrategy(oversold=30, overbought=70, obv_weight=0.7),
        ]

        # 3. 각 전략 시그널 분석
        for strategy in strategies:
            test_strategy(strategy, df, SYMBOL)

        # 4. 백테스트 시뮬레이션 (위와 동일한 인스턴스 재사용 — 파라미터 불일치 원천 차단)
        summary = []  # 전략별 결과 수집
        for strategy in strategies:
            print("\n\n")
            print("="*70)
            print(f"  Running Backtest: {strategy.name}")
            print("="*70)
            perf, bhr = run_backtest_simulation(strategy, df, SYMBOL, INITIAL_BALANCE)
            summary.append({
                'name': strategy.name,
                'trades': perf['total_trades'],
                'win_rate': perf['win_rate'],
                'profit': perf['total_profit'],
                'return_pct': perf['return_pct'],
                'outperformance': perf['return_pct'] - bhr,
                'buy_hold_return': bhr,
            })

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
        
        print("\n" + "="*70)
        print("  ✅ All tests completed successfully!")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
