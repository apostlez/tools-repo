# Plan: 자동 트레이딩 시스템 개발

주식과 코인 자동매매를 위한 standalone 프로그램 개발 계획입니다. Python을 권장하며(더 성숙한 트레이딩 생태계), 알고리즘 기반 매매 전략 실행, 리스크 관리, 백테스팅 기능을 포함합니다.

## Steps

### 1. 개발 환경 구축
- Python 프로젝트 생성 (venv 가상환경)
- 필수 라이브러리 설치
  - `ccxt` for 거래소 API
  - `pandas` for 데이터 분석
  - `python-dotenv` for 설정 관리

### 2. 거래소/브로커 연동
- API 키 발급
  - 주식: Alpaca/KIS (한국투자증권)
  - 코인: Binance/Upbit
- `.env` 파일에 안전하게 저장
- ccxt로 거래소 연결 및 테스트 (먼저 sandbox/paper trading 모드 사용)

### 3. 매매 전략 엔진 구현
- 기술적 지표 계산 모듈 (RSI, MACD, 이동평균)
- 매수/매도 시그널 생성 로직
- 알고리즘 입력 인터페이스 설계 (JSON/YAML 설정 파일 또는 Python 클래스)

### 4. 주문 실행 시스템
- 시장가/지정가 주문 함수
- 포지션 관리 (현재 보유 자산 추적)
- 주문 상태 확인 및 로깅
- 에러 처리 및 재시도 로직

### 5. 리스크 관리
- 손절매/익절 자동 설정
- 포지션 사이즈 계산 (자산 대비 %)
- 일일 최대 손실 한도
- 동시 포지션 수 제한

### 6. 백테스팅 및 모니터링
- 과거 데이터로 전략 검증
- 실시간 로깅 (거래 내역, 수익률)
- 알림 시스템 (텔레그램/이메일)
- 데이터베이스 연동 (SQLite/PostgreSQL)

## Further Considerations

### 1. 국내 vs 해외 거래소
- 한국 주식(한국투자증권 API), 업비트(코인) 사용할지
- 아니면 Alpaca(미국 주식), Binance(글로벌 코인) 사용할지 선택 필요

### 2. 실시간 vs 주기적 실행
- 24/7 실시간 모니터링 프로세스로 운영할지
- cron/스케줄러로 정기 실행할지 결정

### 3. 보안 및 테스트
- 반드시 paper trading으로 충분히 테스트 후 실제 자금 투입
- API 키는 읽기 전용 또는 출금 불가 권한으로 제한 권장

## 기술 스택 상세 분석

### Python 권장 이유
1. **Superior trading ecosystem** - Libraries like `ccxt` (crypto), `alpaca-trade-api`, `yfinance`, `pandas-ta`
2. **Data analysis** - NumPy, Pandas for strategy backtesting
3. **ML/AI integration** - scikit-learn, TensorFlow for algorithmic strategies
4. **Established patterns** - More mature trading frameworks (QuantConnect, Backtrader)

### Node.js 대안
- 현재 workspace에 Node.js 환경 구축되어 있음
- Real-time WebSocket support (good for live data)
- Libraries: `ccxt` (also available), `alpaca-trade-api-node`, `technicalindicators`
- **단점**: Less mature ecosystem for quantitative trading

## 핵심 기술 요구사항

### Core Components
1. **Exchange/Broker APIs**
   - Stocks: Alpaca, Interactive Brokers, TD Ameritrade, 한국투자증권
   - Crypto: Binance, Coinbase Pro, Kraken, Upbit
   - Library: `ccxt` (supports 100+ exchanges)

2. **Data Management**
   - Real-time market data feeds
   - Historical data storage (database)
   - Price/volume caching

3. **Strategy Engine**
   - Technical indicators (RSI, MACD, Bollinger Bands)
   - Backtesting framework
   - Paper trading mode
   - Order execution logic

4. **Risk Management**
   - Position sizing
   - Stop-loss/take-profit
   - Portfolio balancing
   - Maximum loss limits

5. **Infrastructure**
   - Secure credential storage (environment variables)
   - Logging and monitoring
   - Error handling and recovery
   - Rate limiting (API quotas)

### Security Considerations
- Never commit API keys to git
- Use `.env` files with `.gitignore`
- Implement 2FA where supported
- Start with paper trading/sandbox environments
