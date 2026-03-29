"""
Raw 데이터 기반 MACD+RSI+OBV 매수/매도 시그널 분석
목표: 7번의 매수 타이밍 식별
파라미터 확정: MACD(8,21,5) + RSI(9, thresh<55) + OBV_MA(10)
"""
import pandas as pd
import numpy as np

df = pd.read_csv('autoTradingSystem/logs/raw_XRP_KRW_1m_2603290425.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')

# ── 지표 계산 ────────────────────────────────────────────────────────
# MACD: fast=8, slow=21, signal=5  (1분봉 최적)
macd_line = df['close'].ewm(span=8, adjust=False).mean() - df['close'].ewm(span=21, adjust=False).mean()
signal_line = macd_line.ewm(span=5, adjust=False).mean()

# RSI: period=9  (1분봉 단기)
delta = df['close'].diff()
gain = delta.where(delta > 0, 0).rolling(window=9).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=9).mean()
rsi = 100 - (100 / (1 + gain / loss))

# OBV + OBV_MA(10)
obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
obv_ma = obv.rolling(window=10).mean()
obv_rising = obv_ma > obv_ma.shift(1)

# ── 시그널 조건 ─────────────────────────────────────────────────────
# 매수: MACD Golden Cross + RSI < 55 + OBV_MA 상승
golden_cross = (macd_line >= signal_line) & (macd_line.shift(1) < signal_line.shift(1))
buy_cond = golden_cross & (rsi < 55) & obv_rising

# 매도: RSI > 65 + OBV_MA 하락
sell_cond = (rsi > 65) & (~obv_rising)

print('=== 7 BUY SIGNALS (MACD GC + RSI<55 + OBV rising) ===')
buy_signals = df[buy_cond]
print(f'Total buy signals: {len(buy_signals)}')
for ts, row in buy_signals.iterrows():
    print(f'  {ts} | price={row["close"]:.0f} | RSI={rsi[ts]:.1f} | MACD={macd_line[ts]:.3f} | Sig={signal_line[ts]:.3f}')

print()
print('=== SELL SIGNALS (RSI>65 + OBV falling) ===')
sell_signals = df[sell_cond]
print(f'Total sell signals: {len(sell_signals)}')
for ts, row in sell_signals.iterrows():
    print(f'  {ts} | price={row["close"]:.0f} | RSI={rsi[ts]:.1f}')

print(f'\nBuy count={buy_cond.sum()}, Sell count={sell_cond.sum()}')
