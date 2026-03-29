# Auto Trading System

자동 트레이딩 시스템 - 알고리즘 기반 주식 및 암호화폐 자동매매

## 프로젝트 구조

```
autoTradingSystem/
├── src/
│   ├── indicators/          # 기술적 지표 모듈
│   │   ├── __init__.py
│   │   └── technical_indicators.py
│   └── strategies/          # 매매 전략 모듈
│       ├── __init__.py
│       ├── base_strategy.py
│       ├── sample_strategies.py
│       └── custom_strategies.py  # RSIOBVStrategy, MACDRSIOBVStrategy
├── config/                  # 설정 파일
│   └── trading_config.py
├── docs/                    # 문서 및 가이드
│   ├── BOT_GUIDE.md
│   ├── README_API_TEST.md
│   ├── BACKTEST_GUIDE.md
│   ├── CONFIG_GUIDE.md
│   ├── strategies_guide.md
│   ├── MACD_RSI_OBV_analysis.md  # MACDRSIOBVStrategy 분석 결과
│   ├── plan-autoTradingSystem.prompt.md
│   └── test_result.md
├── tests/                   # 테스트 스크립트
│   ├── test_binance_api.py
│   ├── test_upbit_api.py
│   ├── test_strategy.py
│   ├── debug_api.py
│   ├── verify_macd_rsi_obv.py  # 7회 매수 검증
│   ├── debug_no_buy.py          # 구간별 미발생 원인 분석
│   └── analyze_signals.py       # 파라미터 탐색
├── logs/                    # 로그 파일
├── .env                     # 환경 변수 (API 키)
├── .env.example             # 환경 변수 템플릿
├── .gitignore
├── requirements.txt         # 필수 라이브러리
├── setup.bat               # 환경 설정 스크립트
├── main.py                 # 트레이딩 봇 진입점
├── find_surging_coins.py   # 실시간 급등 종목 감지 🚀
├── run_binance_test.bat    # Binance API 테스트 실행
├── run_upbit_test.bat      # Upbit API 테스트 실행
├── run_strategy_test.bat   # 전략 테스트 실행
├── run_surge_detector.bat  # 급등 종목 감지 실행
└── run_bot.bat             # 트레이딩 봇 실행
```

## 빠른 시작

### 1. 환경 설정

```bash
# setup.bat 실행 (가상환경 생성 및 패키지 설치)
setup.bat
```

### 2. API 키 설정

`.env` 파일 생성 및 API 키 입력:

```env
# Binance Testnet API (Paper Trading)
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
```

**Testnet API 키 발급**: https://testnet.binance.vision/

### 3. API 연결 테스트

```bash
# Binance API 테스트
run_binance_test.bat

# Upbit API 테스트
run_upbit_test.bat

# 문제 발생 시 디버그
python tests\debug_api.py
```

**자세한 테스트 가이드**: [docs/README_API_TEST.md](docs/README_API_TEST.md)

### 4. 전략 테스트 및 백테스팅

```bash
# 전략 시그널 분석 + RSI 전략 백테스팅
run_strategy_test.bat
```

**자세한 가이드**: [docs/BACKTEST_GUIDE.md](docs/BACKTEST_GUIDE.md)

### 5. 급등 종목 감지 🚀

```bash
# 실시간 가격 급등 종목 모니터링
run_surge_detector.bat

# 또는
python find_surging_coins.py
```

**설정 옵션** (스크립트 내부 수정):
- `THRESHOLD`: 급등 기준 (기본값: 3.0%)
- `INTERVAL`: 체크 간격 (기본값: 60초)
- `MIN_VOLUME`: 최소 거래량 필터 (기본값: $100,000)

**출력 예시**:
```
🚀 급등 종목 감지: 3개
----------------------------------------------------------------------
🔥 XRP/USDT     | 가격: $    2.0950 | 상승률: + 5.23% | 거래량: $  1,234,567
🔥 BTC/USDT     | 가격: $98,432.10  | 상승률: + 4.15% | 거래량: $ 45,678,901
🔥 ETH/USDT     | 가격: $ 3,456.78  | 상승률: + 3.87% | 거래량: $ 23,456,789
```

### 6. 자동 매매 봇 실행

```bash
# 트레이딩 봇 실행 (DRY RUN 모드)
run_bot.bat

# 또는
python main.py
```

**설정 수정**: [config/trading_config.py](config/trading_config.py)  
**자세한 가이드**: [docs/BOT_GUIDE.md](docs/BOT_GUIDE.md)

## 주요 기능

### ✅ 완료된 기능

1. **개발 환경 구축**
   - Python 가상환경 설정
   - 필수 라이브러리 설치 (ccxt, pandas, numpy 등)

2. **거래소 연동**
   - Binance Testnet API 연결
   - 시장 데이터 조회 (OHLCV)
   - 계좌 정보 조회

3. **기술적 지표 모듈** ([src/indicators/technical_indicators.py](src/indicators/technical_indicators.py))
   - SMA, EMA (이동평균)
   - RSI (상대강도지수)
   - MACD (이동평균 수렴확산)
   - Bollinger Bands (볼린저 밴드)
   - Stochastic Oscillator (스토캐스틱)
   - ATR, OBV, VWAP

4. **매매 전략 시스템** ([src/strategies/](src/strategies/))
   - BaseStrategy (전략 베이스 클래스)
   - RSIStrategy (RSI 기반 전략)
   - MACDStrategy (MACD 크로스오버 전략)
   - MovingAverageCrossStrategy (이동평균선 교차 전략)
   - OBVStrategy (거래량 기반 전략)
   - RSIOBVStrategy (RSI+OBV 복합 가중치 전략)
   - **MACDRSIOBVStrategy** (MACD 골든 크로스 + RSI + OBV 3중 필터 전략 ⭐ 최신)
     - 1분봉 최적화 파라미터 (MACD:8/21/5, RSI:9, OBV_MA:10)
     - XRP/KRW 7시간 데이터에서 정확히 7번 매수 시그널 검증
     - 상세 분석: [docs/MACD_RSI_OBV_analysis.md](docs/MACD_RSI_OBV_analysis.md)

5. **백테스팅**
   - 과거 데이터로 전략 검증 (최대 1000 캔들)
   - 전략별 시그널 분석 (RSI, MACD, MA Cross, OBV, RSI+OBV, **MACD+RSI+OBV**)
   - 성과 분석 (승률, 수익률, 거래 통계)
   - Buy & Hold 대비 성과 비교
   - CSV 파일 기반 오프라인 백테스트 지원 (`python tests/test_strategy.py <csv_path>`)
   - 자세한 내용: [docs/BACKTEST_GUIDE.md](docs/BACKTEST_GUIDE.md)

### ✅ 최근 완료

1. **실시간 트레이딩 시스템** ([src/trading_bot.py](src/trading_bot.py))
   - 실시간 시장 데이터 모니터링
   - 자동 주문 실행
   - 포지션 관리

2. **리스크 관리** ([src/risk_manager.py](src/risk_manager.py))
   - 손절매/익절 자동 설정
   - 포지션 사이즈 계산
   - 일일 최대 손실 한도
   - 동시 포지션 수 제한
   - 트레일링 스탑

3. **급등 종목 감지 시스템** ([find_surging_coins.py](find_surging_coins.py))
   - 실시간 가격 모니터링
   - 급등 종목 자동 감지 및 알림
   - 거래량 필터링
   - 급등 이력 추적 및 통계

### 🚧 개발 예정

3. **고급 전략**
   - 멀티 지표 조합 전략
   - 머신러닝 기반 전략
   - 차익거래 전략

4. **모니터링 및 알림**
   - 텔레그램 알림
   - 이메일 알림
   - 웹 대시보드

5. **데이터베이스 연동**
   - 거래 내역 저장
   - 성과 분석 및 리포트

## 매매 전략

### RSI Strategy
- **매수**: RSI < 30 (과매도)
- **매도**: RSI > 70 (과매수)
- **적합**: 횡보장, 변동성 큰 시장

### MACD Strategy
- **매수**: MACD 라인이 시그널 라인 상향 돌파
- **매도**: MACD 라인이 시그널 라인 하향 돌파
- **적합**: 트렌드 시장

### MA Cross Strategy
- **매수**: 단기 MA가 장기 MA 상향 돌파
- **매도**: 단기 MA가 장기 MA 하향 돌파
- **적합**: 명확한 트렌드 시장

자세한 내용: [docs/strategies_guide.md](docs/strategies_guide.md)

## 사용 예제

### 전략 테스트

```python
from src.indicators import calculate_all_indicators
from src.strategies import RSIStrategy

# 시장 데이터 가져오기
df = fetch_market_data('BTC/USDT', '1h', 200)

# 지표 계산
df = calculate_all_indicators(df)

# 전략 생성 및 분석
strategy = RSIStrategy(oversold=30, overbought=70)
signal = strategy.analyze(df, 'BTC/USDT')

print(f"Signal: {signal.signal_type.value}")
print(f"Price: ${signal.price:,.2f}")
print(f"Reason: {signal.reason}")
```

### 커스텀 전략 만들기

```python
from src.strategies import BaseStrategy, Signal, SignalType

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("My Strategy", {'threshold': 50})
    
    def get_required_indicators(self):
        return ['rsi_14', 'sma_20']
    
    def analyze(self, df, symbol):
        rsi = df['rsi_14'].iloc[-1]
        price = df['close'].iloc[-1]
        
        if rsi < 30:
            return Signal(SignalType.BUY, price, datetime.now(), symbol, 0.8, "Oversold")
        elif rsi > 70:
            return Signal(SignalType.SELL, price, datetime.now(), symbol, 0.8, "Overbought")
        
        return Signal(SignalType.HOLD, price, datetime.now(), symbol, 0.0, "Neutral")
```

## 기술 스택

- **언어**: Python 3.12
- **거래소 API**: CCXT (암호화폐 거래소 통합 라이브러리)
- **데이터 분석**: Pandas, NumPy
- **기술적 지표**: pandas-ta, ta-lib
- **백테스팅**: Backtrader
- **환경 관리**: python-dotenv

## 안전 수칙

⚠️ **중요 보안 사항**:

1. **Paper Trading 우선**: 실제 자금 투입 전 충분한 테스트
2. `.env` 파일은 절대 Git에 커밋하지 않음
4. **권한 제한**: API 키는 최소 권한만 부여 (읽기, 트레이딩만)
5. **출금 비활성화**: API 키에서 출금 권한 제거
6. **리스크 관리**: 손절매 설정, 포지션 사이즈 제한

## 개발 로드맵

- [x] 개발 환경 구축
- [x] 거래소 API 연동 (Binance, Upbit)
- [x] 기술적 지표 모듈
- [x] 기본 매매 전략 구현
- [x] 백테스팅 시스템
- [x] 실시간 트레이딩 시스템
- [x] 리스크 관리 모듈
- [ ] 알림 시스템 (텔레그램, 이메일)
- [ ] 웹 대시보드
- [ ] 머신러닝 전략
- [ ] 다중 거래소 지원
- [ ] 한국 주식 API 연동 (한국투자증권)

## 문제 해결

### API 연결 오류
- `tests/debug_api.py` 실행하여 상세 진단
- Testnet API 키 재발급
- 시스템 시간 동기화 확인

### 백테스트 오류
- 충분한 데이터 확보 (최소 200 캔들)
- 필요한 지표가 계산되었는지 확인
- 전략 파라미터 검증

### 패키지 설치 오류
- Python 버전 확인 (3.12+)
- 가상환경 재생성: `setup.bat` 재실행
- 수동 설치: `pip install -r requirements.txt`

## 기여

이슈 리포트, 기능 제안, PR 환영합니다!

## 라이선스

MIT License

## 면책 조항

이 소프트웨어는 교육 목적으로 제공됩니다. 실제 거래에서 발생하는 손실에 대해 개발자는 책임지지 않습니다. 
자동 트레이딩은 높은 리스크를 수반하므로 충분한 테스트와 이해 후 사용하시기 바랍니다.

---

**Made with ❤️ for algorithmic trading enthusiasts**
