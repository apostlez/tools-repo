"""
MACDRSIOBVStrategy 백테스트 검증 스크립트
raw XRP/KRW 1분봉 데이터로 7번의 매수 시그널을 확인
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from autoTradingSystem.src.strategies.custom_strategies import MACDRSIOBVStrategy

# ── 데이터 로드 & 지표 사전 계산 (trading_bot 역할) ─────────────────
csv_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'raw_XRP_KRW_1m_2603290425.csv')
df = pd.read_csv(csv_path)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')

# MACD (8, 21, 5)
fast_ema = df['close'].ewm(span=8, adjust=False).mean()
slow_ema = df['close'].ewm(span=21, adjust=False).mean()
df['macd'] = fast_ema - slow_ema
df['macd_signal'] = df['macd'].ewm(span=5, adjust=False).mean()

# RSI (9)
delta = df['close'].diff()
gain = delta.where(delta > 0, 0).rolling(window=9).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=9).mean()
df['rsi_9'] = 100 - (100 / (1 + gain / loss))

# OBV
df['obv'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()

# ── 전략 인스턴스 ────────────────────────────────────────────────────
strategy = MACDRSIOBVStrategy(
    macd_fast=8,
    macd_slow=21,
    macd_signal=5,
    rsi_period=9,
    rsi_buy_threshold=55.0,
    rsi_sell_threshold=65.0,
    obv_ma_period=10,
)

print(f'전략: {strategy.name}')
print(f'파라미터: {strategy.parameters}')
print()

# ── 봉별 시뮬레이션 ─────────────────────────────────────────────────
min_bars = 2  # 크로스 감지에 최소 2봉 필요; 지표 NaN은 전략 내부에서 처리
buy_signals = []
sell_signals = []

for i in range(min_bars, len(df)):
    window = df.iloc[:i+1]
    signal = strategy.analyze(window, 'XRP/KRW')
    ts = df.index[i]

    if signal.signal_type.value == 'BUY':
        buy_signals.append((ts, signal))
        print(f'[BUY  #{len(buy_signals)}] {ts} | price={signal.price:.0f}')
        print(f'         {signal.reason}')
    elif signal.signal_type.value == 'SELL':
        sell_signals.append((ts, signal))
        print(f'[SELL #{len(sell_signals)}] {ts} | price={signal.price:.0f}')
        print(f'         {signal.reason}')

print()
print(f'총 매수: {len(buy_signals)}회 | 총 매도: {len(sell_signals)}회')
assert len(buy_signals) == 7, f'Expected 7 buy signals, got {len(buy_signals)}'
print('✓ 7번 매수 시그널 검증 완료')
