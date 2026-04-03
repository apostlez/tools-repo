# Changelog

All notable changes to this project will be documented in this file.

---

## [0.3.0] - 2026-04-04

### Added
- **BollingerScalpStrategy** (`src/strategies/custom_strategies.py`) — 횡보장 특화 볼린저 밴드 스캘핑 전략
  - 매수: BB 하단 돌파 + RSI 과매도 + BB 밴드폭 < 임계값(횡보장 확인) 세 조건 동시 충족
  - 매도: BB 중심선(MA) 회귀 또는 RSI 과매수
  - 시그널 강도: BB 이탈 정도 + RSI 과매도 정도를 결합한 복합 계산
  - 고변동성 트렌드 장세에서 역추세 진입 자동 차단 (`bb_width_threshold`)
  - `.env` 환경변수로 모든 파라미터 제어 가능 (`BB_SCALP_*`)

- **파라미터 최적화 스크립트** (`tests/analyze_raw_data.py`)
  - raw CSV 데이터 로드 및 통계 분석 (ATR, 볼린저 밴드폭, 수익률 분포)
  - MACDRSIOBVStrategy / RSIOBVStrategy 그리드 서치 최적화
  - 실제 봇과 동일한 조건(SL/TP/수수료/포지션 사이즈)으로 백테스트

### Changed
- `config/trading_config.py` — `STRATEGY_CONFIG`에 `bollinger_scalp` 파라미터 블록 추가
- `main.py` — `BollingerScalpStrategy` 선택 및 설정 출력 지원
- `tests/test_strategy.py` — 전략 목록에 `BollingerScalpStrategy` 추가 (백테스트 자동 포함)

---



### Fixed
- **SELL 실패 시 무한 재시도 버그 수정** (`src/trading_bot.py`)
  - SELL 주문 실패 후 내부 포지션이 삭제되지 않아 매 iteration마다 take profit이 재트리거되던 문제 해결
  - `_sync_position_from_exchange()` 메서드 추가: SELL 실패 시 거래소 실제 잔고를 조회하여 내부 포지션 상태를 동기화
    - 실제 잔고 ≈ 0 → orphan 포지션 즉시 제거
    - 실제 잔고 < tracked amount (부분 체결/외부 매도) → `amount`, `cost`를 실제 잔고 비율로 조정
    - 실제 잔고 ≥ tracked amount → 상태 유지

- **중복 로그 버그 수정** (`src/risk_manager.py`)
  - `should_stop_loss` / `should_take_profit` / `get_trailing_stop_loss`가 내부에서 `calculate_*` public 메서드를 호출해 포지션 보유 중 매 iteration마다 로그가 2~3회 중복 출력되던 문제 해결
  - `_compute_stop_loss()` / `_compute_take_profit()` private 헬퍼 추가 (로그 없음)
  - 내부 로직은 private 헬퍼를 사용하고, public `calculate_*` API는 `open_position` 시에만 호출

### Added
- **네트워크 재시도 처리** (`src/trading_bot.py`, `tests/test_strategy.py`)
  - 지수 백오프(exponential backoff) 재시도 로직 추가: 5s → 10s → 20s (기본 3회)
  - 재시도 대상: `ccxt.NetworkError`, `RequestTimeout`, `ExchangeNotAvailable`, `DDoSProtection`
  - `TradingBot._call_with_retry()` 메서드 추가, `fetch_ohlcv` / `fetch_balance` 호출에 적용
  - `test_strategy.py`에 `_fetch_with_retry()` 독립 함수 추가, 데이터 fetch 배치 루프에 적용

### Changed
- **날짜별 로그 로테이션** (`main.py`, `config/trading_config.py`)
  - `RotatingFileHandler`(크기 기반) → `TimedRotatingFileHandler`(날짜 기반)로 교체
  - 자정마다 새 파일로 롤오버, 파일명 suffix: `trading_bot.log.YYYY-MM-DD`
  - `LOGGING_CONFIG`에서 `max_bytes` / `backup_count` → `backup_days`(기본 30일)로 변경
  - `.env`에서 `LOG_BACKUP_DAYS` 환경 변수로 보관 일수 제어 가능

- **알림 시스템 로드맵에서 제거** (`docs/BOT_GUIDE.md`, `docs/plan-autoTradingSystem.prompt.md`, `docs/strategies_guide.md`, `README.md`)
  - 텔레그램/이메일 알림 관련 항목을 개발 예정 로드맵 및 문서에서 삭제

---

## [0.1.0] - 2026-03-28

### Added
- 초기 프로젝트 구성
- 거래소 연동: Binance Testnet, Upbit
- 기술적 지표 모듈: SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, ATR, OBV, VWAP
- 매매 전략: `RSIStrategy`, `MACDStrategy`, `MovingAverageCrossStrategy`, `OBVStrategy`, `RSIOBVStrategy`, `MACDRSIOBVStrategy`
- 백테스팅 시스템 (PortfolioManager, CSV 기반 오프라인 백테스트 지원)
- 실시간 트레이딩 봇 (`src/trading_bot.py`)
- 리스크 관리 모듈 (`src/risk_manager.py`): 손절매, 익절, 트레일링 스탑, 일일 최대 손실 한도
- 급등 종목 감지 시스템 (`find_surging_coins.py`)
