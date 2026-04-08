# Auto Trading Bot - 사용 가이드

## 🚀 빠른 시작

### 1. 봇 실행

```bash
# 가상환경 활성화
venv\Scripts\activate

# 봇 실행
python main.py

# 또는 배치 파일 사용
run_bot.bat
```

### 2. 봇 중지

- **Ctrl + C** 키를 눌러 안전하게 중지
- 봇이 자동으로 남은 포지션을 정리하고 최종 성과를 출력합니다

## ⚙️ 설정

모든 설정은 [config/trading_config.py](config/trading_config.py)에서 수정 가능합니다.

### 거래 설정 (TRADING_CONFIG)

```python
TRADING_CONFIG = {
    'symbol': 'BTC/USDT',      # 거래 쌍
    'timeframe': '15m',         # 캔들 시간 프레임
    'update_interval': 60,      # 업데이트 주기 (초)
    'initial_balance': 10000,   # 시뮬레이션 초기 자본
    'dry_run': True,            # True: 시뮬레이션, False: 실제 거래 ⚠️
}
```

**시간 프레임 옵션:**
- `1m`: 1분봉
- `5m`: 5분봉
- `15m`: 15분봉 (권장)
- `1h`: 1시간봉
- `4h`: 4시간봉
- `1d`: 일봉

### 전략 설정 (STRATEGY_CONFIG)

```python
STRATEGY_CONFIG = {
    'name': 'RSIStrategy',  # 사용할 전략 선택
    
    # RSI 전략 파라미터
    'rsi': {
        'oversold': 30,     # 과매도 기준
        'overbought': 70,   # 과매수 기준
        'rsi_period': 14
    }
}
```

**사용 가능한 전략:**
- `RSIStrategy`: RSI 기반 과매수/과매도 전략
- `MACDStrategy`: MACD 크로스오버 전략
- `MovingAverageCrossStrategy`: 이동평균선 교차 전략

### 리스크 관리 (RISK_CONFIG)

```python
RISK_CONFIG = {
    'max_position_size': 0.1,    # 포지션 크기 (자본의 10%)
    'stop_loss_pct': 0.05,        # 손절매 5%
    'take_profit_pct': 0.10,      # 익절 10%
    'max_daily_loss': 0.03,       # 일일 최대 손실 3%
    'max_positions': 3,           # 최대 동시 포지션 수
    'risk_reward_ratio': 2.0,     # 최소 리스크/보상 비율
    'trailing_stop_pct': 0.03,    # 트레일링 스탑 3%
}
```

**중요 파라미터 설명:**

- **max_position_size**: 한 번의 거래에 사용할 최대 자본 비율
  - 0.1 = 전체 자본의 10%
  - 보수적: 0.05 (5%), 공격적: 0.2 (20%)

- **stop_loss_pct**: 손절매 비율
  - 0.05 = 진입가 대비 5% 하락 시 손절
  - 변동성 큰 코인: 0.07~0.10 권장
  - 변동성 작은 코인: 0.03~0.05 권장

- **take_profit_pct**: 익절 비율
  - 0.10 = 진입가 대비 10% 상승 시 익절
  - 손절매의 2배 이상 권장

- **max_daily_loss**: 일일 최대 손실 한도
  - 0.03 = 하루 3% 손실 시 거래 중단
  - 자본 보호를 위한 안전장치

- **risk_reward_ratio**: 리스크/보상 비율
  - 2.0 = 잃을 수 있는 금액 대비 2배 이상 벌 수 있을 때만 거래
  - 최소 2:1 권장

## 🎯 운영 모드

### DRY RUN 모드 (시뮬레이션)

```python
TRADING_CONFIG = {
    'dry_run': True,  # 시뮬레이션 모드
}

EXCHANGE_CONFIG = {
    'testnet': True,  # Binance Testnet 사용
}
```

- ✅ 실제 주문을 보내지 않음
- ✅ 가상 자본으로 시뮬레이션
- ✅ Testnet API 사용 (무료)
- ✅ 전략 검증 및 학습용

**권장 사용 기간**: 최소 1주일 이상

### LIVE 모드 (실제 거래) ⚠️

```python
TRADING_CONFIG = {
    'dry_run': False,  # 실제 거래 모드
}

EXCHANGE_CONFIG = {
    'testnet': False,  # 실제 Binance 사용
}
```

- ⚠️ **실제 자금 사용**
- ⚠️ 충분한 테스트 후에만 전환
- ⚠️ 소액으로 시작 권장
- ⚠️ API 키 권한 제한 (출금 비활성화)

## 📊 봇 동작 흐름

1. **초기화**
   - 거래소 연결
   - 전략 및 리스크 관리자 생성
   - 설정 로드

2. **반복 사이클** (매 update_interval마다)
   - 시장 데이터 조회 (OHLCV)
   - 기술적 지표 계산
   - 전략 시그널 생성
   - 포지션 청산 조건 체크 (손절/익절)
   - 시그널에 따른 거래 실행

3. **리스크 관리**
   - 포지션 사이즈 계산
   - 손절매/익절 가격 설정
   - 일일 손실 한도 확인
   - 최대 포지션 수 제한

4. **거래 실행**
   - 매수: BUY 시그널 + 포지션 없음
   - 매도: SELL 시그널 또는 손절/익절
   - **매도 보류**: 수익률 < 0.5% 이면 최대 3회까지 매도 보류 (화수 소진 시 강제 매도)

## 📈 성과 모니터링

봇은 10회 반복마다 성과를 자동으로 출력합니다:

```
📈 Performance Summary:
   Total Trades: 15
   Winning: 9, Losing: 6
   Win Rate: 60.00%
   Total Profit: $250.00
   Initial Balance: $10,000.00
   Current Balance: $10,250.00
   Total Return: +2.50%
   Open Positions: 1
```

## 📝 로그 파일

로그는 `logs/trading_bot.log`에 저장됩니다:

- 모든 거래 내역
- 시그널 생성 기록
- 에러 및 경고
- 성과 통계

## ⚡ 실전 팁

### 1. 전략 선택

**RSI Strategy**
- ✅ 횡보장에 효과적
- ✅ 변동성 큰 시장
- ❌ 강한 트렌드에서는 비효율

**MACD Strategy**
- ✅ 트렌드 포착에 유리
- ✅ 중장기 투자
- ❌ 지연된 시그널

**MA Cross Strategy**
- ✅ 명확한 트렌드 시장
- ✅ 장기 투자
- ❌ 횡보장에서 손실

### 2. 시간 프레임 선택

- **1m, 5m**: 데이 트레이딩, 높은 거래 빈도, 높은 리스크
- **15m, 1h**: 스윙 트레이딩, 균형잡힌 접근 (권장)
- **4h, 1d**: 포지션 트레이딩, 장기 투자

### 3. 리스크 관리 최적화

**보수적 설정:**
```python
max_position_size: 0.05  # 5%
stop_loss_pct: 0.03      # 3%
take_profit_pct: 0.10    # 10%
max_daily_loss: 0.02     # 2%
```

**공격적 설정:**
```python
max_position_size: 0.2   # 20%
stop_loss_pct: 0.08      # 8%
take_profit_pct: 0.15    # 15%
max_daily_loss: 0.05     # 5%
```

### 4. 안전 수칙

1. ✅ 항상 DRY RUN으로 먼저 테스트
2. ✅ 소액으로 시작
3. ✅ 손절매 반드시 설정
4. ✅ 일일 손실 한도 준수
5. ✅ API 키 출금 권한 비활성화
6. ✅ 정기적인 성과 검토
7. ✅ 시장 상황에 따른 전략 조정

## 🔧 문제 해결

### 봇이 거래를 안 함

- 시그널 강도 확인 (strength=0.0이면 포지션 없음)
- 매도 보류 중인지 확인 (`⏸ SELL deferred` 로그 참조)
- 리스크 관리 설정 확인 (일일 손실 한도 초과?)
- 잔액 부족 여부 확인
- 로그 파일 확인

### 연결 오류

- API 키 확인 (.env 파일)
- Testnet 모드 확인
- 인터넷 연결 확인

### 손실이 계속됨

- 전략 변경 고려
- 시간 프레임 조정
- 리스크 파라미터 재조정
- 시장 상황 분석 (트렌드 vs 횡보)

## 📚 다음 단계

1. ✅ DRY RUN으로 1주일 테스트
2. 📊 다양한 전략 비교
3. ⚙️ 파라미터 최적화
4. 📈 백테스트 결과 분석
5. 💰 소액 실전 거래 (LIVE 모드)
6.  웹 대시보드 구축

---

**⚠️ 면책 조항**: 자동 트레이딩은 높은 리스크를 수반합니다. 본인의 판단과 책임 하에 사용하시기 바랍니다.
