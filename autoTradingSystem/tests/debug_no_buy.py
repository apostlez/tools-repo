"""
선택 구간 (13:26 ~ 13:40) 매수 시그널 미발생 원인 분석
세 가지 조건 각각이 구간에서 어떻게 변하는지 추적
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np

df = pd.read_csv('autoTradingSystem/logs/raw_XRP_KRW_1m_2603290425.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')

# 지표 계산 (전략과 동일한 파라미터)
fast_ema = df['close'].ewm(span=8, adjust=False).mean()
slow_ema = df['close'].ewm(span=21, adjust=False).mean()
macd = fast_ema - slow_ema
macd_sig = macd.ewm(span=5, adjust=False).mean()
hist = macd - macd_sig

delta = df['close'].diff()
gain = delta.where(delta > 0, 0).rolling(window=9).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=9).mean()
rsi = 100 - (100 / (1 + gain / loss))

obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
obv_ma = obv.rolling(window=10).mean()
obv_rising = obv_ma > obv_ma.shift(1)

golden_cross = (macd >= macd_sig) & (macd.shift(1) < macd_sig.shift(1))
death_cross  = (macd <  macd_sig) & (macd.shift(1) >= macd_sig.shift(1))

# 분석 구간: 맥락을 위해 13:00 ~ 13:45
window_start = '2026-03-28 13:00'
window_end   = '2026-03-28 13:45'

print(f"{'시각':^19} {'Close':>6} {'MACD':>7} {'Sig':>7} {'Hist':>7} "
      f"{'RSI':>6} {'OBV_risen':>9} {'GC':>4} {'DC':>4}  {'조건충족'}")
print('-' * 105)

for ts in df[window_start:window_end].index:
    close  = df['close'][ts]
    m      = macd[ts]
    ms     = macd_sig[ts]
    h      = hist[ts]
    r      = rsi[ts]
    obv_r  = obv_rising[ts]
    gc     = golden_cross[ts]
    dc     = death_cross[ts]

    cond1 = gc           # Golden Cross
    cond2 = r < 55       # RSI 조건
    cond3 = obv_r        # OBV 상승

    all_ok = cond1 and cond2 and cond3

    # 13:26~13:40 선택 구간 강조
    highlight = "★ 선택구간" if '13:26' <= str(ts)[11:16] <= '13:40' else ""
    if all_ok:
        highlight += "  ← BUY!"

    print(f"{str(ts)[5:16]:^19} {close:>6.0f} {m:>7.3f} {ms:>7.3f} {h:>7.3f} "
          f"{r:>6.1f} {'Y' if obv_r else 'N':>9} {'Y' if gc else 'N':>4} {'Y' if dc else 'N':>4}  "
          f"GC={int(cond1)}/RSI={int(cond2)}/OBV={int(cond3)} {highlight}")

print()
print("=" * 60)
print("선택 구간 (13:26~13:40) 조건별 실패 이유 요약")
print("=" * 60)

sel_start = '2026-03-28 13:26'
sel_end   = '2026-03-28 13:40'
sel = df[sel_start:sel_end]

for ts in sel.index:
    r     = rsi[ts]
    obv_r = obv_rising[ts]
    gc    = golden_cross[ts]
    dc    = death_cross[ts]
    reasons = []
    if not gc:
        reasons.append(f"GC없음(MACD{macd[ts]:+.3f} vs Sig{macd_sig[ts]:+.3f})")
    if not (r < 55):
        reasons.append(f"RSI={r:.1f}≥55")
    if not obv_r:
        reasons.append(f"OBV_MA하락")
    status = "THREE_MISS" if len(reasons) == 3 else f"FAIL({len(reasons)})"
    print(f"  {str(ts)[11:16]}  {status:10s}  {' | '.join(reasons)}")
