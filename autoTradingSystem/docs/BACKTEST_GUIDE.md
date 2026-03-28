# 백테스팅 가이드

전략을 실제 자금 없이 과거 데이터로 검증하는 방법을 설명합니다.

---

## 목차

1. [백테스팅이란?](#1-백테스팅이란)
2. [백테스팅 실행](#2-백테스팅-실행)
3. [결과 해석](#3-결과-해석)
4. [출력 파일](#4-출력-파일)
5. [파라미터 변경](#5-파라미터-변경)
6. [전략별 백테스트](#6-전략별-백테스트)
7. [구현 구조](#7-구현-구조)
8. [한계 및 주의사항](#8-한계-및-주의사항)

---

## 1. 백테스팅이란?

백테스팅은 매매 전략이 **과거 시장 데이터에서 어떻게 작동했을지** 시뮬레이션하는 과정입니다.

본 시스템의 백테스팅은 다음 방식으로 동작합니다:

```
[Option A] Upbit API에서 OHLCV 데이터 수집 (배치 요청으로 최신 N개 보장)
[Option B] raw_*.csv 파일에서 OHLCV 데이터 로드 ← API 없이 재실행 가능
        ↓
기술적 지표 전체 계산 (RSI, MACD, OBV 등)
        ↓
캔들 50번째부터 순서대로 반복
        ↓
strategy.analyze() → BUY / SELL / HOLD 시그널 생성
        ↓
BUY 시그널 + 포지션 없음 → 잔액 95% 매수  (진입 이유·RSI·OBV 출력)
SELL 시그널 + 포지션 보유 → 전량 매도     (손익·진입/청산가·이유·RSI·OBV 출력)
        ↓
최종 손익, 승률, Buy & Hold 대비 성과 출력
        ↓
logs/backtest_YYMMDDHHMI.json 저장
        ↓
tests/generate_chart.py → 백테스트 대시보드 차트 생성
tests/chart_from_csv.py → 캔들스틱 차트 생성 (CSV 실행 시)
```

> 처음 50 캔들은 지표 계산을 위한 **워밍업 기간**이므로 거래가 발생하지 않습니다.

---

## 2. 백테스팅 실행

### Option A — API로 최신 데이터 수집 후 실행

```bat
run_strategy_test.bat
```

또는 직접:

```bash
venv\Scripts\activate
python tests/test_strategy.py
```

**실행 조건**
- `venv/` 가상환경이 설치되어 있어야 합니다 (`setup.bat` 실행)
- `.env` 파일에 Upbit API 키가 설정되어 있어야 합니다

```env
UPBIT_ACCESS_KEY=your_upbit_access_key
UPBIT_SECRET_KEY=your_upbit_secret_key
```

### Option B — 저장된 CSV 파일로 실행 (API 불필요)

API 키 없이, 이전에 수집된 raw CSV 파일을 그대로 재사용할 수 있습니다.

```bat
run_strategy_test.bat logs\raw_XRP_KRW_1m_2603290425.csv
```

또는 직접:

```bash
python tests/test_strategy.py logs/raw_XRP_KRW_1m_2603290425.csv
```

> CSV 파일명은 `raw_{SYMBOL}_{TIMEFRAME}_{YYMMDDHHMI}.csv` 형식이어야 합니다.  
> 심볼(`XRP/KRW`)은 파일명에서 자동으로 추출됩니다.

### 차트 자동 생성

`run_strategy_test.bat` 실행 시 전략 테스트 완료 후 차트가 **자동으로 생성**됩니다.

| 스크립트 | 실행 조건 | 생성 파일 |
|----------|-----------|----------|
| `tests/generate_chart.py` | 항상 | `logs/backtest_*_chart.png` |
| `tests/chart_from_csv.py` | CSV 인자 있을 때 | `logs/raw_*_chart.png` |

차트를 단독으로 생성할 때:

```bash
# 최신 JSON 자동 선택
python tests/generate_chart.py

# JSON 직접 지정
python tests/generate_chart.py logs/backtest_2603290446.json

# 최신 CSV 자동 선택
python tests/chart_from_csv.py

# CSV 직접 지정
python tests/chart_from_csv.py logs/raw_XRP_KRW_1m_2603290425.csv
```

---

## 3. 결과 해석

실행하면 두 단계로 결과가 출력됩니다.

### [1단계] 전략별 현재 시그널 분석 (4개 전략)

각 전략이 현재 시장에서 생성하는 시그널을 보여줍니다.

```
======================================================================
  Testing Strategy: RSI Strategy
======================================================================

📋 Strategy Info:
   Name: RSI Strategy
   Parameters: {'oversold': 30, 'overbought': 70, 'rsi_period': 14}
   Required Indicators: ['rsi_14']

🎯 Signal Result:
   Type: HOLD                  ← BUY / SELL / HOLD
   Price: $84,523.10
   Strength: 0.00%             ← 시그널 강도 (0~1), HOLD는 0
   Reason: RSI neutral: 52.34
   Timestamp: 2026-03-27 ...

💹 Market Info:
   Current Price: $84,523.10
   24h Change: +2.15%
   24h High: $85,100.00
   24h Low: $83,200.00

📊 Current Indicators:
   RSI(14): 52.34
   MACD: 45.2318
   MACD Signal: 38.1204
   MACD Histogram: 7.1114
   SMA(20): $83,210.50
   SMA(50): $81,450.30
```

### [2단계] RSI 전략 백테스트 시뮬레이션

```
======================================================================
  Backtest Simulation: RSI Strategy
======================================================================

💰 Initial Balance: 1,000,000 KRW
📅 Period: 2026-03-27 12:09:00 ~ 2026-03-28 05:28:00
💱 Exchange: Upbit | Symbol: XRP/KRW

🔄 Running backtest...
  🟢 BUY  | 2026-03-27 13:34:00 | 2,020.00 KRW | Amount: 470.297030
          Balance   : 50,000 KRW (remaining after buy)
          Reason    : RSI oversold: 28.45 < 30
          Strength  : 51.83%
          RSI       : 28.45
          OBV       : 11,234,567
  🔴 SELL | 2026-03-27 13:45:00 | 2,033.00 KRW
       ✅ Trade P&L : +6,114 KRW  (+0.64%)
          Entry     : 2,020.00 KRW → Exit: 2,033.00 KRW
          Reason    : RSI overbought: 71.32 > 70
          RSI       : 71.32
          OBV       : 12,345,678
  ...

======================================================================
  Backtest Results
======================================================================

📊 Trading Statistics:
   Total Trades:   8           ← 총 거래 횟수 (매수+매도 쌍)
   Winning Trades: 5           ← 수익이 난 거래
   Losing Trades:  3           ← 손실이 난 거래
   Win Rate:       62.50%      ← 승률

💵 Financial Results:
   Initial Balance:      1,000,000 KRW
   Final Balance:        1,013,405 KRW
   Total Profit:           +13,405 KRW
   Return:                  +1.34%  ← 전략 수익률

📈 Trade Analysis:
   Average Profit:          +1,676 KRW  ← 거래당 평균 손익
   Best Trade:              +5,213 KRW  ← 最고 수익 거래
   Worst Trade:             -1,832 KRW  ← 最대 손실 거래

🔄 Strategy vs Buy & Hold:
   Strategy Return:   +1.34%
   Buy & Hold Return: +0.82%
   Outperformance:    +0.52%   ← 양수면 전략이 단순 보유보다 우수
```

#### 거래 로그 해석

| 항목 | 설명 |
|------|------|
| **Trade P&L** | 해당 거래의 실현 손익 (✅ 이익 / ❌ 손실) |
| **Entry → Exit** | 매수가 vs 청산가 — 가격 방향 한눈에 확인 |
| **Reason** | 전략이 BUY/SELL을 낸 구체적 이유 (지표 값 포함) |
| **Strength** | 신호 강도 (0~100%) — 낮으면 경계선 신호 |
| **RSI / OBV** | 해당 시점 실제 지표 값 — 패턴 분석에 활용 |

#### 결과 지표 해석 요령

| 지표 | 좋은 기준 | 설명 |
|------|-----------|------|
| **Win Rate** | 50% 이상 | 절반 이상 거래에서 수익 |
| **Return** | Buy & Hold 이상 | 단순 보유 대비 초과 수익 |
| **Best/Worst Trade 비율** | Best가 Worst보다 2배 이상 | 리스크 대비 보상 (Risk/Reward) |
| **Total Trades** | 충분한 표본 필요 | 거래 횟수가 너무 적으면 결과 신뢰도 낮음 |

---

## 4. 출력 파일

백테스팅 실행 후 `logs/` 폴더에 다음 파일이 생성됩니다.

### raw_*.csv — OHLCV 원시 데이터

API로 수집한 경우 자동 저장됩니다. Option B 실행의 입력 파일로 재사용 가능합니다.

```
logs/raw_XRP_KRW_1m_2603290425.csv
```

```csv
timestamp,open,high,low,close,volume
2026-03-28 12:46:00,2029.0,2029.0,2028.0,2029.0,14967.59
...
```

### backtest_*.json — 백테스트 결과

전략별 요약 결과, 개별 거래 P&L, 현재 지표값이 저장됩니다.

```
logs/backtest_2603290446.json
```

```json
{
  "symbol": "XRP/KRW",
  "period": "2026-03-28 12:46:00 ~ 2026-03-28 19:25:00",
  "initial_balance": 1000000,
  "buy_and_hold_return": 0.1,
  "strategies": {
    "RSI Strategy": {
      "trades": 2, "wins": 1, "losses": 1,
      "return_pct": -0.14, "profit": -1399.58, "vs_bh": -0.24
    },
    ...
  },
  "trade_pnl": {
    "RSI Strategy": [2827.0, -4226.58],
    ...
  },
  "current_indicators": {
    "Current Price": 2037.0,
    "RSI(14)": 54.55,
    "MACD": -0.588,
    ...
  }
}
```

### *_chart.png — 차트 이미지

| 파일 | 내용 |
|------|------|
| `logs/backtest_*_chart.png` | 전략별 수익률·승률·P&L 비교 대시보드 |
| `logs/raw_*_chart.png` | 캔들스틱 + 거래량 + RSI + MACD |

---

## 5. 파라미터 변경

`tests/test_strategy.py` 파일의 `main()` 함수에서 수정합니다.

```python
# tests/test_strategy.py — main() 함수 내부
# (CSV 파일 지정 시 TIMEFRAME/LIMIT은 무시됩니다)

TIMEFRAME       = '1m'          # 시간 프레임 (1m/5m/15m/1h/4h/1d)
LIMIT           = 400           # 가져올 캔들 수 (Upbit는 200개 한도→배치 자동 처리)
INITIAL_BALANCE = 1_000_000     # 초기 자본 (KRW)
```

#### 시간 프레임별 데이터 기간 (LIMIT=200 기준)

| TIMEFRAME | LIMIT=400 기준 데이터 기간 | 적합한 용도 |
|-----------|--------------------------|------------|
| `1m`      | 약 6.7시간 | 초단기 스캘핑 전략 검증 |
| `5m`      | 약 1.4일 | 단기 전략 |
| `15m`     | 약 4.2일 | 단기~중기 |
| `1h`      | 약 16.7일 | 일반 전략 검증 |
| `4h`      | 약 66.7일 | 중기 추세 전략 |
| `1d`      | 약 13.3개월 | 장기 전략, 큰 그림 확인 |

> Upbit API는 1회 최대 200개 제한이 있으나, `fetch_market_data()`가 자동으로 배치 요청을 수행해 `LIMIT`개까지 수집합니다. 항상 가장 최신 캔들 기준으로 수집됩니다.

---

## 6. 전략별 백테스트

기본적으로 `run_backtest_simulation()`은 `RSIStrategy`로 실행됩니다.  
다른 전략을 백테스트하려면 `tests/test_strategy.py`의 `main()` 하단을 수정합니다.

### RSI Strategy (기본)

```python
from src.strategies import RSIStrategy

selected_strategy = RSIStrategy(
    oversold=30,      # 과매도 기준 (낮을수록 보수적 매수)
    overbought=70     # 과매수 기준 (높을수록 보수적 매도)
)
run_backtest_simulation(selected_strategy, df, SYMBOL, INITIAL_BALANCE)
```

**매매 로직**: RSI < `oversold` → 매수 / RSI > `overbought` → 매도

### MACD Strategy

```python
from src.strategies import MACDStrategy

selected_strategy = MACDStrategy()  # 파라미터 고정: 12/26/9
run_backtest_simulation(selected_strategy, df, SYMBOL, INITIAL_BALANCE)
```

**매매 로직**: MACD Histogram이 0 상향 돌파 → 매수 / 하향 돌파 → 매도

### Moving Average Cross Strategy

```python
from src.strategies import MovingAverageCrossStrategy

selected_strategy = MovingAverageCrossStrategy(
    fast_period=20,   # 단기 이동평균선 기간
    slow_period=50    # 장기 이동평균선 기간
)
run_backtest_simulation(selected_strategy, df, SYMBOL, INITIAL_BALANCE)
```

**매매 로직**: 골든크로스(단기 > 장기) → 매수 / 데드크로스 → 매도

### OBV Strategy

```python
from src.strategies import OBVStrategy

selected_strategy = OBVStrategy(
    obv_ma_period=20,         # OBV 이동평균 기간
    divergence_lookback=5     # 다이버전스 확인 기간
)
run_backtest_simulation(selected_strategy, df, SYMBOL, INITIAL_BALANCE)
```

**매매 로직**: 가격과 OBV 추세가 일치하고 OBV가 MA 돌파 → 매수/매도

### RSI + OBV 복합 전략 (RSIOBVStrategy)

```python
from src.strategies.custom_strategies import RSIOBVStrategy

selected_strategy = RSIOBVStrategy(
    oversold=30,
    overbought=70,
    rsi_period=14,
    obv_ma_period=20,
    obv_weight=0.5    # OBV 영향력 (0.0=RSI만 / 1.0=OBV 최대 반영)
)
run_backtest_simulation(selected_strategy, df, SYMBOL, INITIAL_BALANCE)
```

**매매 로직**: RSI 기본 시그널에 OBV 방향성으로 강도(strength) 조정

---

## 7. 구현 구조

### 파일 구조

```
autoTradingSystem/
├── tests/
│   ├── test_strategy.py      # 백테스트 실행 (CSV or API)
│   ├── generate_chart.py     # 백테스트 대시보드 차트 (JSON → PNG)
│   └── chart_from_csv.py     # 캔들스틱 차트 (CSV → PNG)
├── logs/
│   ├── raw_*.csv             # OHLCV 원시 데이터
│   ├── backtest_*.json       # 백테스트 결과
│   └── *_chart.png           # 생성된 차트
└── run_strategy_test.bat     # 통합 실행 스크립트
```

### 핵심 클래스

| 클래스 | 위치 | 역할 |
|--------|------|------|
| `PortfolioManager` | `src/strategies/base_strategy.py` | 포트폴리오 상태 추적, 손익 계산 |
| `BaseStrategy` | `src/strategies/base_strategy.py` | 전략 추상 클래스 |
| `Signal` | `src/strategies/base_strategy.py` | BUY/SELL/HOLD 시그널 객체 |
| `calculate_all_indicators()` | `src/indicators/technical_indicators.py` | 모든 기술적 지표 일괄 계산 |

### 계산되는 기술적 지표

| 컬럼명 | 지표 |
|--------|------|
| `sma_20`, `sma_50`, `sma_200` | 단순 이동평균 |
| `ema_12`, `ema_26` | 지수 이동평균 |
| `rsi_14` | RSI (14기간) |
| `macd`, `macd_signal`, `macd_histogram` | MACD (12/26/9) |
| `bb_upper`, `bb_middle`, `bb_lower` | 볼린저 밴드 (20, 2σ) |
| `stoch_k`, `stoch_d` | Stochastic (14/3) |
| `atr` | Average True Range (14) |
| `obv` | On-Balance Volume |
| `vwap` | Volume-Weighted Average Price |

### 커스텀 전략 작성

새 전략을 만들어 백테스트하려면 `src/strategies/custom_strategies.py`에 추가합니다:

```python
from src.strategies import BaseStrategy, Signal, SignalType
from datetime import datetime

class MyStrategy(BaseStrategy):
    def __init__(self, my_param: int = 20):
        super().__init__("My Strategy", {'my_param': my_param})
        self.my_param = my_param

    def get_required_indicators(self):
        return ['rsi_14', 'sma_20']   # 필요한 지표 컬럼명

    def analyze(self, df, symbol) -> Signal:
        rsi = df['rsi_14'].iloc[-1]
        price = df['close'].iloc[-1]

        if rsi < 30:
            return Signal(SignalType.BUY, price, datetime.now(), symbol, 0.8, "RSI oversold")
        elif rsi > 70:
            return Signal(SignalType.SELL, price, datetime.now(), symbol, 0.8, "RSI overbought")

        return Signal(SignalType.HOLD, price, datetime.now(), symbol, 0.0, "Neutral")
```

---

## 8. 한계 및 주의사항

### 현재 백테스팅의 한계

| 항목 | 현재 구현 | 실제 거래 |
|------|-----------|----------|
| 수수료 | 미반영 | Upbit 0.05% / trade |
| 슬리피지 | 미반영 | 시장 주문 시 발생 |
| 포지션 크기 | 잔액의 95% 고정 | 리스크 관리에 따라 가변 |
| 거래 타입 | 시장가 가정 | 지정가/시장가 선택 가능 |
| 데이터 | Upbit 최신 캔들 (배치 수집) | 장기 과거 데이터 |

### 과최적화(Overfitting) 주의

백테스트에서 좋은 결과가 나왔다고 실제 거래에서도 동일한 성과를 보장하지 않습니다.

- 파라미터를 특정 기간에 맞게 과도하게 최적화하지 마세요
- 최소 3~6개월 이상의 데이터로 검증하세요 (`LIMIT` 증가 + `TIMEFRAME` 조정)
- 검증용 데이터(out-of-sample)를 따로 빼두고 마지막에 검증하세요

### 권장 검증 절차

```
1. 백테스트 (과거 데이터)   → 기본 성과 확인
        ↓
2. 파라미터 조정 → 다른 기간으로 재검증
        ↓
3. DRY RUN (main.py)       → 실시간 시뮬레이션 (실제 API, 가상 주문)
        ↓
4. 소액 실거래              → 극소액으로 실제 검증
```

DRY RUN 실행 방법은 [BOT_GUIDE.md](BOT_GUIDE.md)를 참조하세요.
