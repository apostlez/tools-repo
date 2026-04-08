# Trading Strategies Configuration

## Available Strategies

### 1. RSI Strategy (상대강도지수 전략)

**전략 설명:**
- RSI 지표를 사용하여 과매수/과매도 상태를 판단
- RSI < 30: 과매도 → 매수 시그널
- RSI > 70: 과매수 → 매도 시그널

**파라미터:**
```python
RSIStrategy(
    oversold=30,      # 과매도 기준 (기본값: 30)
    overbought=70,    # 과매수 기준 (기본값: 70)
    rsi_period=14     # RSI 계산 기간 (기본값: 14)
)
```

**적합한 시장:**
- 횡보장 (Range-bound market)
- 변동성이 큰 시장

**장점:**
- 구현이 간단하고 명확함
- 과매수/과매도 구간에서 효과적

**단점:**
- 강한 트렌드 시장에서는 잘못된 시그널 가능
- 단일 지표 의존으로 인한 신뢰도 문제

---

### 2. MACD Strategy (이동평균 수렴확산 전략)

**전략 설명:**
- MACD 라인과 시그널 라인의 크로스오버로 매매 판단
- MACD 라인이 시그널 라인을 상향 돌파 → 매수 (골든 크로스)
- MACD 라인이 시그널 라인을 하향 돌파 → 매도 (데드 크로스)

**파라미터:**
```python
MACDStrategy(
    fast_period=12,    # 빠른 EMA 기간 (기본값: 12)
    slow_period=26,    # 느린 EMA 기간 (기본값: 26)
    signal_period=9    # 시그널 라인 기간 (기본값: 9)
)
```

**적합한 시장:**
- 트렌드가 있는 시장
- 중장기 투자

**장점:**
- 트렌드 전환 시점 포착에 유리
- 모멘텀과 추세를 동시에 파악

**단점:**
- 후행성 지표 (지연된 시그널)
- 횡보장에서 잦은 거짓 시그널

---

### 3. Moving Average Cross Strategy (이동평균선 교차 전략)

**전략 설명:**
- 단기/장기 이동평균선의 교차로 매매 판단
- 단기 MA가 장기 MA를 상향 돌파 → 매수 (골든 크로스)
- 단기 MA가 장기 MA를 하향 돌파 → 매도 (데드 크로스)

**파라미터:**
```python
MovingAverageCrossStrategy(
    fast_period=20,    # 단기 MA 기간 (기본값: 20)
    slow_period=50     # 장기 MA 기간 (기본값: 50)
)
```

**일반적인 설정:**
- 단기 트레이딩: 5/20, 10/30
- 중기 트레이딩: 20/50, 50/100
- 장기 트레이딩: 50/200

**적합한 시장:**
- 명확한 트렌드가 있는 시장
- 장기 투자

**장점:**
- 가장 기본적이고 이해하기 쉬움
- 큰 트렌드 포착에 효과적

**단점:**
- 후행성 지표
- 횡보장에서 손실 위험

---

### 4. OBV Strategy (거래량 지표 전략)

**전략 설명:**
- OBV(On-Balance Volume) 지표를 사용하여 거래량 트렌드 분석
- 가격과 OBV의 트렌드 일치/불일치로 매매 판단
- 다이버전스 감지로 추세 반전 포착

**파라미터:**
```python
OBVStrategy(
    obv_ma_period=20,        # OBV 이동평균 기간 (기본값: 20)
    divergence_lookback=5    # 다이버전스 감지 기간 (기본값: 5)
)
```

**시그널 조건:**
- 가격 상승 + OBV 상승 (트렌드 확인) → 매수
- 가격 하락 + OBV 하락 (트렌드 확인) → 매도
- 가격 상승 but OBV 하락 (약세 다이버전스) → 매도
- 가격 하락 but OBV 상승 (강세 다이버전스) → 매수

**적합한 시장:**
- 거래량이 활발한 시장
- 트렌드 확인이 필요한 시장
- 추세 전환 시점 포착

**장점:**
- 거래량 기반으로 가격 움직임의 진정성 확인
- 다이버전스로 추세 반전 조기 감지
- 가격만으로는 알 수 없는 시장 심리 파악

**단점:**
- 거래량이 적은 시장에서는 신뢰도 낮음
- 급격한 가격 변동 시 지연 가능
- 다른 지표와 함께 사용 권장

---

### 5. RSI + OBV Strategy (복합 가중치 전략) ⭐ Custom

**전략 설명:**
- RSI로 기본 매수/매도 시그널을 생성한 뒤, OBV 트렌드로 시그널 강도에 가중치를 곱하는 복합 전략
- OBV 이동평균의 변화율을 `tanh` 로 −1 ~ +1 정규화하여 방향성 팩터로 사용

**시그널 강도 계산식:**
```
BUY  강도 = rsi_strength × (1 + obv_weight × obv_factor)
SELL 강도 = rsi_strength × (1 − obv_weight × obv_factor)
```

| RSI 시그널 | OBV 방향 | 결과 |
|-----------|---------|------|
| BUY       | 상승 ↑  | 강도 **증폭** (강세 확인) |
| BUY       | 하락 ↓  | 강도 **감소** (신뢰도 낮은 반등) |
| SELL      | 하락 ↓  | 강도 **증폭** (약세 확인) |
| SELL      | 상승 ↑  | 강도 **감소** (신뢰도 낮은 하락) |

**파라미터:**
```python
RSIOBVStrategy(
    oversold=30,        # RSI 과매도 기준 (기본값: 30)
    overbought=70,      # RSI 과매수 기준 (기본값: 70)
    rsi_period=14,      # RSI 계산 기간 (기본값: 14)
    obv_ma_period=20,   # OBV 이동평균 기간 — 트렌드 판단용 (기본값: 20)
    obv_weight=0.5      # OBV 가중치 최대값 0.0 ~ 1.0 (기본값: 0.5)
)
```

**적합한 시장:**
- 거래량이 뒷받침되는 과매수/과매도 반전 시장
- RSI 단독 신호의 신뢰도를 높이고 싶은 경우

**장점:**
- RSI 단순 전략 대비 허위 시그널 감소
- OBV로 거래량 흐름을 반영해 시그널의 신뢰도 향상
- `obv_weight` 파라미터로 OBV 반영 강도 조절 가능

**단점:**
- OBV 데이터가 없거나 부족하면 RSI 전략과 동일하게 동작
- 두 지표 모두 후행성을 가지므로 급반전 시 지연 가능

---

## Strategy Testing

### 테스트 실행 방법

```bash
# 가상환경 활성화
venv\Scripts\activate

# 전략 테스트 실행 (실시간 데이터 수집 후 백테스트)
python tests\test_strategy.py

# CSV 파일로 백테스트 (오프라인)
python tests\test_strategy.py logs\raw_XRP_KRW_1m_YYMMDDHHNN.csv

# 배치 파일로 실행 (테스트 + 차트 생성 자동화)
run_strategy_test.bat [csv_path]
```

### 출력 정보

- 📋 전략 정보 (이름, 파라미터, 필요 지표)
- 🎯 현재 시그널 (BUY/SELL/HOLD, 강도, 이유)
- 💹 시장 정보 (현재가, 24시간 변동)
- 📊 기술적 지표 값
- 📈 백테스트 결과 (승률, 수익률, 거래 통계)
- 💾 JSON 결과 자동 저장 (`logs/backtest_YYMMDDHHNN.json`)

### 매도 보류(Defer) 로직

백테스트는 실제 봇과 동일한 매도 보류 조건을 적용합니다:

- 수익률 **< 0.5%** 이고 아직 보류 횟수가 3회 미만이면 매도를 보류
- 3회 소진 또는 수익률 ≥ 0.5% 도달 시 정상 매도 실행
- Stop Loss / Take Profit은 보류 없이 즉시 처리

```
⏸ SELL deferred (1/3) | 2026-04-07 05:16 | profit=+0.020% < 0.5% ...
⏸ SELL deferred (2/3) | 2026-04-07 05:17 | profit=+0.031% < 0.5% ...
🔴 SELL | 2026-04-07 05:18 | 2,021.00 KRW   ← 3회 소진 후 강제 매도
```

---

## 분석 도구

### analyze_params.py — 파라미터 분포 분석

백테스트 전 CSV 데이터의 RSI/MACD/OBV 분포를 조사해 최적 파라미터를 선택하는 분석 스크립트.

```bash
python tests\analyze_params.py logs\raw_XRP_KRW_1m_YYMMDDHHNN.csv
```

**출력 예시:**
```
Candles: 400
Buy&Hold return: +0.84%
  OBV_MA=5,  RSI<55: 3/3=  8  2/3= 42  MACD_only= 58
  OBV_MA=5,  RSI<60: 3/3= 10  2/3= 50  MACD_only= 58
  OBV_MA=8,  RSI<55: 3/3=  6  2/3= 38  MACD_only= 58
--- RSI(9) distribution ---
  RSI < 55: 180 bars  |  RSI > 55: 220 bars
  RSI median: 50.2    mean: 50.9
```

**활용법:**
- `3/3` 진입 수가 0이면 `rsi_buy_threshold`를 높이거나 `obv_ma_period`를 줄임
- RSI 분포(median/mean)로 해당 기간의 추세 강도 파악
- `2/3`와 `3/3` 비율로 rsi_hard_cap 적절성 판단

### chart_from_csv_with_event.py — BUY/SELL 이벤트 차트

`test_strategy.py` 실행 후 생성된 JSON의 `trade_events`를 캔들스틱 차트에 오버레이하는 시각화 도구.

```bash
# test_strategy.py 먼저 실행 (JSON 생성)
python tests\test_strategy.py logs\raw_XRP_KRW_1m_YYMMDDHHNN.csv

# 이벤트 차트 생성 (최신 CSV/JSON 자동 선택)
python tests\chart_from_csv_with_event.py

# 파일 직접 지정
python tests\chart_from_csv_with_event.py logs\raw_XRP_KRW_1m_YYMMDDHHNN.csv logs\backtest_YYMMDDHHNN.json
```

**차트 구성:**
- 상단: 캔들스틱 + MA20/MA60 + BUY(▲)/SELL(▼) 마커 + 성과 요약 박스
- 매수/매도 연결선: 수익(청록) / 손실(빨강)
- SELL 마커에 종료가 + 수익률%  레이블 표시
- RSI·MACD 패널에 BUY/SELL 수직 점선 오버레이
- 전략별 PNG 자동 저장: `logs/raw_*_{전략명}_events.png`

**전역 설정 (파일 상단에서 수정):**
```python
# tests/chart_from_csv_with_event.py
RSI_PERIOD:  int = 14   # RSI 계산 기간
MACD_FAST:   int = 12   # MACD 빠른 EMA
MACD_SLOW:   int = 26   # MACD 느린 EMA
MACD_SIGNAL: int = 9    # MACD 시그널 EMA
```

`run_strategy_test.bat`은 테스트 실행 후 `chart_from_csv_with_event.py`를 자동으로 호출합니다.

---

## Custom Strategy 만들기

새로운 전략은 `src/strategies/custom_strategies.py` 에 추가하고 `BaseStrategy` 를 상속:

```python
# src/strategies/custom_strategies.py
from src.strategies import BaseStrategy, Signal, SignalType

class MyCustomStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(
            name="My Strategy",
            parameters={'param1': 10}
        )
    
    def get_required_indicators(self):
        return ['rsi_14', 'sma_20']  # 필요한 지표
    
    def analyze(self, df, symbol):
        # 전략 로직 구현
        if df['rsi_14'].iloc[-1] < 30 and df['close'].iloc[-1] < df['sma_20'].iloc[-1]:
            return Signal(
                SignalType.BUY,
                df['close'].iloc[-1],
                datetime.now(),
                symbol,
                0.8,
                "RSI oversold + below SMA"
            )
        return Signal(SignalType.HOLD, df['close'].iloc[-1], datetime.now(), symbol)
```

전략 추가 후 아래 두 파일을 업데이트:

1. **`src/strategies/__init__.py`** — 클래스 임포트 및 `__all__` 에 추가
2. **`config/trading_config.py`** — `STRATEGY_CONFIG` 에 파라미터 섹션 추가
3. **`main.py`** — `create_strategy()` 와 `print_configuration()` 에 분기 추가

> **구현 예시**: `RSIOBVStrategy`, `MACDRSIOBVStrategy` (`src/strategies/custom_strategies.py`) 참고

---

### 6. MACD + RSI + OBV Strategy (2/3 스코어링 복합 전략) ⭐ Custom

> **상세 분석**: [docs/MACD_RSI_OBV_analysis.md](MACD_RSI_OBV_analysis.md)

**전략 설명:**
- MACD Bullish(상승 모멘텀 지속)를 필수 조건으로, RSI·OBV 중 1개 이상을 추가 충족하는 2/3 스코어링 매수 방식
- 단발 Golden Cross 대신 `_is_macd_bullish()` (MACD ≥ Signal AND MACD 상승 중)로 광범위한 진입 구간 포착
- 매도는 RSI가 과매수 임계값 **아래로 교차하는 순간**에만 발화 (지속 상태 매도가 아닌 하락 교차 감지)

**시그널 조건:**

| 구분 | 조건 | 설명 |
|------|------|------|
| **BUY 3/3** | MACD Bullish + RSI < buy_thr + OBV_MA 상승 | strength ≥ 0.4 |
| **BUY 2/3** | MACD Bullish + (RSI or OBV 1개 충족) | strength ≥ 0.25 × 0.4 |
| **2/3 차단** | RSI > buy_thr × 1.15 (rsi_hard_cap) | 과매수 상태 2/3 BUY 금지 |
| **SELL** | prev_RSI ≥ sell_thr AND curr_RSI < sell_thr | RSI 하락 교차 순간에 청산 |

**파라미터 (XRP/KRW 1분봉 최적화):**
```python
MACDRSIOBVStrategy(
    macd_fast=8,              # MACD 빠른 EMA
    macd_slow=21,             # MACD 느린 EMA
    macd_signal=3,            # Signal EMA — 빠른 반응
    rsi_period=4,             # RSI 기간 — 1분봉 단기 반응
    rsi_buy_threshold=62.0,   # 매수 허용 RSI 상한
    rsi_sell_threshold=80.0,  # 매도 교차 기준 RSI
    obv_ma_period=5,          # OBV 이동평균 기간
)
```

**강도(strength) 계산:**
```
rsi_score  = max(0, (rsi_buy_thr - RSI) / rsi_buy_thr)   # RSI 여유도
macd_score = |MACD_dist| / (price × 0.002)               # MACD 간격 (KRW 가격 정규화)
full_strength = (rsi_score + macd_score) / 2

3/3 BUY: strength = max(0.4, full_strength)
2/3 BUY: strength = max(0.25, full_strength × 0.4)
```

**적합한 시장:**
- 1분봉 단기 트레이딩
- 거래량이 뒷받침되는 모멘텀 반전 구간
- RSI가 과매수 구간에서 꺾이는 단기 고점 청산

**장점:**
- Golden Cross 단발 조건 대비 진입 기회 대폭 증가
- rsi_hard_cap으로 과매수 구간 무조건 진입 차단
- 매도가 추세 전환 확인 후 발화되어 조기 청산 방지

**단점:**
- RSI 임계값 tuning이 종목/시간대별로 필요
- 매도 조건 특성상 하락 가속 구간에서 청산 지연 가능
- 강한 하락 추세에서는 매도 교차 전 손절매 의존 필요

---

## 다음 단계

1. ✅ 전략 테스트 완료 → `tests/test_strategy.py` 실행
2. ✅ 커스텀 전략 구현 → `RSIOBVStrategy` (`src/strategies/custom_strategies.py`)
3. ✅ 실시간 트레이딩 시스템 구현 → `main.py` + `src/trading_bot.py`
4. ✅ 리스크 관리 모듈 추가 → `src/risk_manager.py`
5. 📝 전략 파라미터 최적화 (백테스트 기반)
6. 📊 성능 모니터링
