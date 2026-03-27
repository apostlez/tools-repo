# 백테스팅 가이드

전략을 실제 자금 없이 과거 데이터로 검증하는 방법을 설명합니다.

---

## 목차

1. [백테스팅이란?](#1-백테스팅이란)
2. [백테스팅 실행](#2-백테스팅-실행)
3. [결과 해석](#3-결과-해석)
4. [파라미터 변경](#4-파라미터-변경)
5. [전략별 백테스트](#5-전략별-백테스트)
6. [구현 구조](#6-구현-구조)
7. [한계 및 주의사항](#7-한계-및-주의사항)

---

## 1. 백테스팅이란?

백테스팅은 매매 전략이 **과거 시장 데이터에서 어떻게 작동했을지** 시뮬레이션하는 과정입니다.

본 시스템의 백테스팅은 다음 방식으로 동작합니다:

```
Binance Testnet에서 OHLCV 데이터 수집
        ↓
기술적 지표 전체 계산 (RSI, MACD, OBV 등)
        ↓
캔들 50번째부터 순서대로 반복
        ↓
strategy.analyze() → BUY / SELL / HOLD 시그널 생성
        ↓
BUY 시그널 + 포지션 없음 → 잔액 95% 매수
SELL 시그널 + 포지션 보유 → 전량 매도
        ↓
최종 손익, 승률, Buy & Hold 대비 성과 출력
```

> 처음 50 캔들은 지표 계산을 위한 **워밍업 기간**이므로 거래가 발생하지 않습니다.

---

## 2. 백테스팅 실행

### 기본 실행 (권장)

```bat
run_strategy_test.bat
```

또는 직접 실행:

```bash
venv\Scripts\activate
python tests/test_strategy.py
```

### 실행 조건

- `venv/` 가상환경이 설치되어 있어야 합니다 (`setup.bat` 실행)
- `.env` 파일에 Binance API 키가 설정되어 있어야 합니다 (Testnet)

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
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

💰 Initial Balance: $10,000.00
📅 Period: 2026-02-17 ~ 2026-03-27

🔄 Running backtest...
  🟢 BUY  | 2026-02-20 14:00 | $82,310.00 | Amount: 0.115312
  🔴 SELL | 2026-02-23 08:00 | $85,100.00  ← 매도 확정가
  🟢 BUY  | 2026-03-01 22:00 | $79,450.00 | Amount: 0.127020
  🔴 SELL | 2026-03-07 16:00 | $83,200.00
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
   Initial Balance: $10,000.00
   Final Balance:   $11,340.52
   Total Profit:    $1,340.52
   Return:          +13.41%    ← 전략 수익률

📈 Trade Analysis:
   Average Profit: $167.57     ← 거래당 평균 손익
   Best Trade:     $521.30     ← 最고 수익 거래
   Worst Trade:    -$183.20    ← 最대 손실 거래

🔄 Strategy vs Buy & Hold:
   Strategy Return:   +13.41%
   Buy & Hold Return: +8.23%
   Outperformance:    +5.18%   ← 양수면 전략이 단순 보유보다 우수
```

#### 지표 해석 요령

| 지표 | 좋은 기준 | 설명 |
|------|-----------|------|
| **Win Rate** | 50% 이상 | 절반 이상 거래에서 수익 |
| **Return** | Buy & Hold 이상 | 단순 보유 대비 초과 수익 |
| **Best/Worst Trade 비율** | Best가 Worst보다 2배 이상 | 리스크 대비 보상 (Risk/Reward) |
| **Total Trades** | 충분한 표본 필요 | 거래 횟수가 너무 적으면 결과 신뢰도 낮음 |

---

## 4. 파라미터 변경

`tests/test_strategy.py` 파일 상단의 `main()` 함수에서 수정합니다.

```python
# tests/test_strategy.py — main() 함수 내부

SYMBOL          = 'BTC/USDT'   # 백테스트 종목 (예: 'ETH/USDT', 'XRP/USDT')
TIMEFRAME       = '1h'          # 시간 프레임 (1m/5m/15m/1h/4h/1d)
LIMIT           = 200           # 가져올 캔들 수 (최소 100 권장)
INITIAL_BALANCE = 10000         # 초기 자본 (USDT)
```

#### 시간 프레임별 데이터 기간 (LIMIT=200 기준)

| TIMEFRAME | 데이터 기간 | 적합한 용도 |
|-----------|------------|------------|
| `1m`      | 약 3.3시간 | 초단기 스캘핑 전략 검증 |
| `5m`      | 약 16.7시간 | 단기 전략 |
| `15m`     | 약 2.1일 | 단기~중기 |
| `1h`      | 약 8.3일 | **기본값** — 일반 전략 검증 |
| `4h`      | 약 33.3일 | 중기 추세 전략 |
| `1d`      | 약 6.7개월 | 장기 전략, 큰 그림 확인 |

> 더 긴 기간을 보려면 `LIMIT`을 늘리세요. Binance는 최대 1000개까지 지원합니다 (ccxt 기본값).

---

## 5. 전략별 백테스트

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
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

## 6. 구현 구조

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

## 7. 한계 및 주의사항

### 현재 백테스팅의 한계

| 항목 | 현재 구현 | 실제 거래 |
|------|-----------|----------|
| 수수료 | 미반영 | Binance 0.1% / trade |
| 슬리피지 | 미반영 | 시장 주문 시 발생 |
| 포지션 크기 | 잔액의 95% 고정 | 리스크 관리에 따라 가변 |
| 거래 타입 | 시장가 가정 | 지정가/시장가 선택 가능 |
| 데이터 | Testnet (최신 200 캔들) | 장기 과거 데이터 |

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
