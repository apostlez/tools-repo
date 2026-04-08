import pandas as pd
import numpy as np
import sys

csv = sys.argv[1] if len(sys.argv) > 1 else 'logs/raw_XRP_KRW_1m_2604062022.csv'
df = pd.read_csv(csv, parse_dates=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)
df.set_index('timestamp', inplace=True)

print(f'Candles: {len(df)}')
print(f'Period: {df.index[0]} ~ {df.index[-1]}')
print(f'Price range: {df.close.min():.2f} ~ {df.close.max():.2f}')
print(f'Buy&Hold return: {(df.close.iloc[-1]/df.close.iloc[0]-1)*100:+.2f}%')

delta = df.close.diff()
gain = delta.where(delta > 0, 0).rolling(9).mean()
loss = (-delta.where(delta < 0, 0)).rolling(9).mean()
rsi9 = 100 - 100 / (1 + gain / loss)

fast_ema = df.close.ewm(span=8, adjust=False).mean()
slow_ema = df.close.ewm(span=21, adjust=False).mean()
macd_line = fast_ema - slow_ema
macd_sig_line = macd_line.ewm(span=5, adjust=False).mean()
macd_bullish = (macd_line >= macd_sig_line) & (macd_line > macd_line.shift(1))

obv = (np.sign(df.close.diff()) * df.volume).fillna(0).cumsum()
for obv_p in [5, 8, 10]:
    obv_ma = obv.rolling(obv_p).mean()
    obv_rising = obv_ma > obv_ma.shift(1)
    for rsi_thr in [55, 60, 65]:
        buy3 = macd_bullish & (rsi9 < rsi_thr) & obv_rising
        buy2 = macd_bullish & ((rsi9 < rsi_thr) | obv_rising)
        print(f'  OBV_MA={obv_p}, RSI<{rsi_thr}: 3/3={buy3.sum():>3}  2/3={buy2.sum():>3}  MACD_only={macd_bullish.sum():>3}')

print()
print('--- RSI(9) distribution ---')
for thr in [40, 45, 50, 55, 60, 65, 70]:
    print(f'  RSI < {thr}: {(rsi9 < thr).sum():>3} bars  |  RSI > {thr}: {(rsi9 > thr).sum():>3} bars')
print(f'  RSI median: {rsi9.median():.1f}  mean: {rsi9.mean():.1f}')
