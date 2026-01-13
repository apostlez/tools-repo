"""
Strategy Testing Script
전략 테스트 및 검증 스크립트
"""

import sys
import os
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

# 환경 변수 로드
load_dotenv()


def fetch_market_data(symbol: str = 'BTC/USDT', 
                     timeframe: str = '1h',
                     limit: int = 200,
                     use_testnet: bool = True) -> pd.DataFrame:
    """
    거래소에서 시장 데이터 가져오기
    
    Args:
        symbol: 거래 심볼
        timeframe: 시간 프레임 (1m, 5m, 15m, 1h, 4h, 1d)
        limit: 데이터 개수
        use_testnet: Testnet 사용 여부
        
    Returns:
        OHLCV DataFrame
    """
    print(f"\n📊 Fetching market data: {symbol} ({timeframe})")
    
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
            'adjustForTimeDifference': True,
        }
    })
    
    if use_testnet:
        exchange.set_sandbox_mode(True)
    
    # OHLCV 데이터 가져오기
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
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
    print(f"   Price: ${signal.price:,.2f}")
    print(f"   Strength: {signal.strength:.2%}")
    print(f"   Reason: {signal.reason}")
    print(f"   Timestamp: {signal.timestamp}")
    
    # 최근 가격 정보
    current_price = df['close'].iloc[-1]
    price_change_24h = ((current_price - df['close'].iloc[-24]) / df['close'].iloc[-24] * 100) if len(df) >= 24 else 0
    
    print(f"\n💹 Market Info:")
    print(f"   Current Price: ${current_price:,.2f}")
    print(f"   24h Change: {price_change_24h:+.2f}%")
    print(f"   24h High: ${df['high'].iloc[-24:].max():,.2f}")
    print(f"   24h Low: ${df['low'].iloc[-24:].min():,.2f}")
    
    # 관련 지표 값 출력
    print(f"\n📊 Current Indicators:")
    if 'rsi_14' in df_with_indicators.columns:
        print(f"   RSI(14): {df_with_indicators['rsi_14'].iloc[-1]:.2f}")
    if 'macd' in df_with_indicators.columns:
        print(f"   MACD: {df_with_indicators['macd'].iloc[-1]:.4f}")
        print(f"   MACD Signal: {df_with_indicators['macd_signal'].iloc[-1]:.4f}")
        print(f"   MACD Histogram: {df_with_indicators['macd_histogram'].iloc[-1]:.4f}")
    if 'sma_20' in df_with_indicators.columns:
        print(f"   SMA(20): ${df_with_indicators['sma_20'].iloc[-1]:,.2f}")
    if 'sma_50' in df_with_indicators.columns:
        print(f"   SMA(50): ${df_with_indicators['sma_50'].iloc[-1]:,.2f}")


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
    
    print(f"\n💰 Initial Balance: ${initial_balance:,.2f}")
    print(f"📅 Period: {df.index[0]} ~ {df.index[-1]}")
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
                print(f"  🟢 BUY  | {current_time} | ${current_price:,.2f} | Amount: {amount:.6f}")
            except ValueError as e:
                pass  # 잔액 부족 등
        
        # 매도 시그널 & 포지션 보유
        elif signal.signal_type == SignalType.SELL and portfolio.has_position(symbol):
            portfolio.close_position(symbol, current_price, current_time)
            print(f"  🔴 SELL | {current_time} | ${current_price:,.2f}")
    
    # 남은 포지션 정리
    if portfolio.has_position(symbol):
        final_price = df_with_indicators['close'].iloc[-1]
        final_time = df_with_indicators.index[-1]
        portfolio.close_position(symbol, final_price, final_time)
        print(f"  🔴 SELL | {final_time} | ${final_price:,.2f} (Position closed)")
    
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
    print(f"   Initial Balance: ${performance['initial_balance']:,.2f}")
    print(f"   Final Balance: ${performance['current_balance']:,.2f}")
    print(f"   Total Profit: ${performance['total_profit']:,.2f}")
    print(f"   Return: {performance['return_pct']:+.2f}%")
    
    if performance['total_trades'] > 0:
        print(f"\n📈 Trade Analysis:")
        print(f"   Average Profit: ${performance['average_profit']:,.2f}")
        print(f"   Best Trade: ${performance['best_trade']:,.2f}")
        print(f"   Worst Trade: ${performance['worst_trade']:,.2f}")
    
    # Buy & Hold 비교
    buy_hold_return = ((df['close'].iloc[-1] - df['close'].iloc[50]) / df['close'].iloc[50]) * 100
    print(f"\n🔄 Strategy vs Buy & Hold:")
    print(f"   Strategy Return: {performance['return_pct']:+.2f}%")
    print(f"   Buy & Hold Return: {buy_hold_return:+.2f}%")
    print(f"   Outperformance: {(performance['return_pct'] - buy_hold_return):+.2f}%")


def main():
    """메인 함수"""
    print("="*70)
    print("  Auto Trading System - Strategy Testing")
    print("="*70)
    
    # 설정
    SYMBOL = 'BTC/USDT'
    TIMEFRAME = '1h'
    LIMIT = 200
    INITIAL_BALANCE = 10000
    
    try:
        # 1. 시장 데이터 가져오기
        df = fetch_market_data(SYMBOL, TIMEFRAME, LIMIT, use_testnet=True)
        
        # 2. 전략 인스턴스 생성
        strategies = [
            RSIStrategy(oversold=30, overbought=70),
            MACDStrategy(),
            MovingAverageCrossStrategy(fast_period=20, slow_period=50),
            OBVStrategy(obv_ma_period=20, divergence_lookback=5)
        ]
        
        # 3. 각 전략 테스트
        for strategy in strategies:
            test_strategy(strategy, df, SYMBOL)
        
        # 4. 백테스트 시뮬레이션 (첫 번째 전략으로)
        print("\n\n")
        print("="*70)
        print("  Running Detailed Backtest")
        print("="*70)
        
        selected_strategy = RSIStrategy(oversold=30, overbought=70)
        run_backtest_simulation(selected_strategy, df, SYMBOL, INITIAL_BALANCE)
        
        print("\n" + "="*70)
        print("  ✅ All tests completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
