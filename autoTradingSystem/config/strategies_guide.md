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

## Strategy Testing

### 테스트 실행 방법

```bash
# 가상환경 활성화
venv\Scripts\activate

# 전략 테스트 실행
python test_strategy.py
```

### 테스트 내용

1. **시장 데이터 가져오기**: Binance Testnet에서 BTC/USDT 1시간봉 200개 조회
2. **전략별 시그널 생성**: 각 전략(RSI, MACD, MA Cross, OBV)의 현재 시그널 및 지표 값 확인
3. **백테스트 시뮬레이션**: RSI 전략으로 과거 데이터 백테스트 실행

### 출력 정보

- 📋 전략 정보 (이름, 파라미터, 필요 지표)
- 🎯 현재 시그널 (BUY/SELL/HOLD, 강도, 이유)
- 💹 시장 정보 (현재가, 24시간 변동)
- 📊 기술적 지표 값
- 📈 백테스트 결과 (승률, 수익률, 거래 통계)

---

## Custom Strategy 만들기

새로운 전략을 만들려면 `BaseStrategy`를 상속:

```python
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

---

## 다음 단계

1. ✅ 전략 테스트 완료 → `test_strategy.py` 실행
2. 📝 전략 파라미터 조정 및 최적화
3. 🔄 실시간 트레이딩 시스템 구현
4. 🛡️ 리스크 관리 모듈 추가
5. 📊 성능 모니터링 및 알림 시스템
