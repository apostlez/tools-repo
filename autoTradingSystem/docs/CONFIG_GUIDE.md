# Configuration Guide

## 설정 관리 방식

이 프로젝트는 2단계 설정 시스템을 사용합니다:

1. **기본값 (Default)**: `config/trading_config.py`에 정의
2. **오버라이드 (Override)**: `.env` 파일에 정의한 값으로 덮어쓰기

### 작동 방식

```
.env 파일에 설정 있음? 
  → YES: .env 값 사용
  → NO: trading_config.py의 기본값 사용
```

## 설정 방법

### 1. 빠른 시작 (.env 최소 설정)

`.env` 파일에 API 키만 설정:

```env
# 필수: API 키
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key

# 나머지는 모두 기본값 사용
```

### 2. 커스터마이징 (.env에서 특정 값만 변경)

원하는 설정만 `.env`에 추가:

```env
# API 키 (필수)
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key

# 거래 설정 변경
TRADING_SYMBOL=ETH/USDT
TRADING_TIMEFRAME=1h
UPDATE_INTERVAL=300

# 리스크 관리 조정
STOP_LOSS_PERCENTAGE=0.03
TAKE_PROFIT_PERCENTAGE=0.15
```

### 3. 전체 커스터마이징

`.env.example` 파일을 참고하여 모든 설정을 조정할 수 있습니다.

## 주요 설정 항목

### Exchange Configuration

| 환경변수 | 기본값 | 설명 |
|---------|-------|------|
| EXCHANGE_NAME | binance | 거래소 이름 |
| EXCHANGE_TESTNET | true | Testnet 사용 여부 |

### Trading Configuration

| 환경변수 | 기본값 | 설명 |
|---------|-------|------|
| TRADING_SYMBOL | BTC/USDT | 거래 쌍 |
| TRADING_TIMEFRAME | 15m | 캔들 시간 프레임 |
| UPDATE_INTERVAL | 60 | 업데이트 주기 (초) |
| INITIAL_BALANCE | 10000 | 초기 자본 (DRY_RUN 모드) |
| DRY_RUN | true | 시뮬레이션 모드 |

### Strategy Configuration

| 환경변수 | 기본값 | 설명 |
|---------|-------|------|
| STRATEGY_NAME | RSIStrategy | 사용할 전략 |
| RSI_OVERSOLD | 30 | RSI 과매도 기준 |
| RSI_OVERBOUGHT | 70 | RSI 과매수 기준 |

### Risk Management

| 환경변수 | 기본값 | 설명 |
|---------|-------|------|
| MAX_POSITION_SIZE | 0.1 | 최대 포지션 크기 (10%) |
| STOP_LOSS_PERCENTAGE | 0.05 | 손절매 비율 (5%) |
| TAKE_PROFIT_PERCENTAGE | 0.10 | 익절 비율 (10%) |
| MAX_DAILY_LOSS | 0.03 | 일일 최대 손실 (3%) |
| MAX_POSITIONS | 3 | 최대 동시 포지션 수 |

## 예제 시나리오

### 예제 1: 보수적 트레이딩

```env
# .env
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret

# 보수적 설정
MAX_POSITION_SIZE=0.05
STOP_LOSS_PERCENTAGE=0.03
TAKE_PROFIT_PERCENTAGE=0.10
MAX_DAILY_LOSS=0.02
```

### 예제 2: 이더리움 1시간봉 트레이딩

```env
# .env
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret

# 이더리움, 1시간봉
TRADING_SYMBOL=ETH/USDT
TRADING_TIMEFRAME=1h
UPDATE_INTERVAL=300

# MACD 전략 사용
STRATEGY_NAME=MACDStrategy
```

### 예제 3: 실전 모드 (⚠️ 주의)

```env
# .env
BINANCE_API_KEY=your_real_api_key
BINANCE_SECRET_KEY=your_real_secret

# 실전 모드
EXCHANGE_TESTNET=false
DRY_RUN=false

# 보수적 설정 권장
MAX_POSITION_SIZE=0.05
INITIAL_BALANCE=100  # 실제 잔액 (소액 권장)
```

## 설정 우선순위

```
1. .env 파일의 환경변수 (최우선)
2. trading_config.py의 기본값
```

## 팁

1. **처음 사용**: API 키만 설정하고 나머지는 기본값 사용
2. **테스트**: `.env`에서 한 번에 하나씩만 변경하며 테스트
3. **실전 전환**: 충분한 시뮬레이션 후 `.env`에서 `DRY_RUN=false`, `EXCHANGE_TESTNET=false` 설정
4. **버전 관리**: `.env` 파일은 Git에 커밋하지 않음 (API 키 보호)

## 설정 확인

봇 실행 시 현재 적용된 설정이 콘솔에 출력됩니다:

```
📊 Trading Configuration:
   Symbol: BTC/USDT
   Timeframe: 15m
   Update Interval: 60s
   Mode: DRY RUN (Simulation)
```
