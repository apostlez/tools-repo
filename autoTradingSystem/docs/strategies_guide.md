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

# 전략 테스트 실행
python tests\test_strategy.py
```

### 전략 선택 방법

`config/trading_config.py` 의 `STRATEGY_NAME` 값을 변경하거나 `.env` 파일에 환경변수를 설정:

```bash
# .env 파일
STRATEGY_NAME=RSIOBVStrategy   # RSI+OBV 복합 전략 (기본)
# STRATEGY_NAME=RSIStrategy
# STRATEGY_NAME=MACDStrategy
# STRATEGY_NAME=MovingAverageCrossStrategy
# STRATEGY_NAME=OBVStrategy
# STRATEGY_NAME=MACDRSIOBVStrategy   # 1분봉 최적화 전략

# RSI+OBV 전용 파라미터
OBV_WEIGHT=0.5    # OBV 가중치 (0.0 ~ 1.0)

# MACD+RSI+OBV 전용 파라미터 (1분봉 최적화)
MACD_RSI_OBV_FAST=8
MACD_RSI_OBV_SLOW=21
MACD_RSI_OBV_SIGNAL=5
MACD_RSI_OBV_RSI_P=9
MACD_RSI_OBV_BUY=55.0
MACD_RSI_OBV_SELL=65.0
MACD_RSI_OBV_OBV_MA=10
```

### 테스트 내용

1. **시장 데이터 가져오기**: Binance Testnet에서 BTC/USDT 1시간봉 200개 조회
2. **전략별 시그널 생성**: 각 전략(RSI, MACD, MA Cross, OBV, **RSI+OBV**)의 현재 시그널 및 지표 값 확인
3. **백테스트 시뮬레이션**: RSI 전략으로 과거 데이터 백테스트 실행

### 출력 정보

- 📋 전략 정보 (이름, 파라미터, 필요 지표)
- 🎯 현재 시그널 (BUY/SELL/HOLD, 강도, 이유)
- 💹 시장 정보 (현재가, 24시간 변동)
- 📊 기술적 지표 값
- 📈 백테스트 결과 (승률, 수익률, 거래 통계)

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

### 6. MACD + RSI + OBV Strategy (골든 크로스 복합 전략) ⭐ Custom

> **상세 분석**: [docs/MACD_RSI_OBV_analysis.md](MACD_RSI_OBV_analysis.md)

**전략 설명:**
- MACD Golden Cross를 기본 진입 트리거로 사용하고, RSI와 OBV로 이중 필터를 적용하는 3중 복합 전략
- 1분봉 단기 트레이딩에 최적화된 파라미터로, XRP/KRW raw 데이터에서 7시간 동안 정확히 7번의 매수 시그널을 생성함을 검증

**시그널 조건:**

| 구분 | 조건 | 설명 |
|------|------|------|
| **BUY** | MACD Golden Cross | MACD 라인이 Signal 라인 위로 교차 |
| **BUY** | RSI < 55 | 과매수 아님 + 모멘텀 전환 확인 |
| **BUY** | OBV_MA 상승 | 매수세 유입 확인 (3가지 모두 충족 시 BUY) |
| **SELL** | RSI > 65 | 과매수 영역 진입 |
| **SELL** | OBV_MA 하락 | 매도세 우위 (2가지 모두 충족 시 SELL) |

**파라미터 (1분봉 최적화):**
```python
MACDRSIOBVStrategy(
    macd_fast=8,             # MACD 빠른 EMA (기본: 8)
    macd_slow=21,            # MACD 느린 EMA (기본: 21)
    macd_signal=5,           # Signal EMA (기본: 5)
    rsi_period=9,            # RSI 기간 (기본: 9)
    rsi_buy_threshold=55.0,  # 매수 허용 RSI 상한 (기본: 55)
    rsi_sell_threshold=65.0, # 매도 기준 RSI (기본: 65)
    obv_ma_period=10,        # OBV 이동평균 기간 (기본: 10)
)
```

**검증 결과 (XRP/KRW 1분봉, 2026-03-28):**

| # | 시각 | 가격 | RSI | 특이사항 |
|---|------|------|-----|---------|
| BUY 1 | 13:05 | 2,030 | 50.0 | 대형 Surge 35분 전 선진입 |
| BUY 2 | 14:13 | 2,046 | 54.5 | Surge 후 조정 완료 반등 |
| BUY 3 | 15:57 | 2,050 | 44.4 | 2차 급등 후 되돌림 반등 |
| BUY 4 | 16:42 | 2,048 | 50.0 | 중반 횡보 바닥 반등 |
| BUY 5 | 17:44 | 2,042 | 50.0 | 하락 속 단기 바닥 |
| BUY 6 | 18:18 | 2,041 | 50.0 | 후반 회복 구간 |
| BUY 7 | 18:30 | 2,040 | 40.0 | 과매도 반등 |

**적합한 시장:**
- 1분봉 단기 트레이딩
- 거래량이 뒷받침되는 모멘텀 반전 구간
- Surge(대형 급등) 전 선진입이 필요한 경우

**장점:**
- 3중 필터로 허위 시그널 최소화
- 거래량(OBV)으로 가격 움직임의 진정성 확인
- Golden Cross 기반으로 추세 전환 시점 포착

**단점:**
- RSI 임계값(55)이 보수적이어 급등 직전 구간을 간발 차로 놓칠 수 있음
- 1분봉 전용 파라미터 — 5분봉 이상에서는 재최적화 필요
- 연속 매도 시그널 발생 시 노이즈 유의

---

## 다음 단계

1. ✅ 전략 테스트 완료 → `tests/test_strategy.py` 실행
2. ✅ 커스텀 전략 구현 → `RSIOBVStrategy` (`src/strategies/custom_strategies.py`)
3. ✅ 실시간 트레이딩 시스템 구현 → `main.py` + `src/trading_bot.py`
4. ✅ 리스크 관리 모듈 추가 → `src/risk_manager.py`
5. 📝 전략 파라미터 최적화 (백테스트 기반)
6. 📊 성능 모니터링
