# API 테스트 가이드

## 목차
- [Binance API 테스트 (Testnet)](#binance-api-테스트-testnet)
- [Upbit API 테스트](#upbit-api-테스트)

---

## Binance API 테스트 (Testnet)

## 중요: Paper Trading (Testnet) 설정

Binance API를 안전하게 테스트하려면 **반드시 Testnet API 키**를 사용해야 합니다.

### 1. Binance Testnet API 키 발급

1. **Binance Testnet 사이트 접속**
   - Spot Trading Testnet: https://testnet.binance.vision/
   
2. **GitHub 계정으로 로그인**
   - "Login with GitHub" 클릭

3. **API 키 생성**
   - "Generate HMAC_SHA256 Key" 클릭
   - API Key와 Secret Key를 복사

4. **테스트 자금 받기**
   - 로그인 후 자동으로 테스트용 USDT, BTC 등이 지급됨
   - 필요시 "Get Test Funds" 버튼으로 추가 가능

### 2. .env 파일 설정

프로젝트 루트에 `.env` 파일을 생성하고 Testnet API 키를 입력:

```env
# Binance Testnet API (Paper Trading)
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_SECRET_KEY=your_testnet_secret_key_here
```

⚠️ **주의**: 
- `.env` 파일은 Git에 커밋되지 않습니다 (.gitignore에 포함됨)
- 실제 거래 API 키가 아닌 **Testnet 키**를 사용하세요
- Testnet 키는 실제 자산과 연결되지 않아 안전합니다

### 3. 테스트 실행

```bash
# 방법 1: 배치 파일 사용 (권장)
run_binance_test.bat

# 방법 2: 직접 실행
venv\Scripts\activate
python tests\test_binance_api.py
```

### 4. 테스트 항목

스크립트는 다음을 테스트합니다:

✅ **Test 1**: 서버 연결 및 시간 동기화
✅ **Test 2**: 계정 잔액 조회
✅ **Test 3**: 시장 데이터 조회 (BTC/USDT)
✅ **Test 4**: 오더북 조회
✅ **Test 5**: 최근 거래 내역
✅ **Test 6**: 거래 제한 및 설정 확인
✅ **Test 7**: 주문 생성 (시뮬레이션)

### 5. 실제 주문 테스트 (선택사항)

기본적으로 주문 생성 코드는 안전을 위해 비활성화되어 있습니다.

실제 테스트 주문을 생성하려면:
1. `tests/test_binance_api.py` 파일 열기
2. Test 7 섹션에서 주석 처리된 코드 찾기 (라인 156-172)
3. 주석 제거 (""" """ 삭제)
4. 다시 테스트 실행

⚠️ **안전 확인사항**:
- Testnet 모드인지 확인 (`exchange.set_sandbox_mode(True)`)
- 소액으로 테스트 (예: 0.001 BTC)
- 시장가보다 낮은 가격으로 지정가 주문 (체결되지 않음)

### 6. 문제 해결

**인증 오류 발생 시**:
- Testnet API 키를 사용하고 있는지 확인
- `.env` 파일의 키가 올바른지 확인
- API 키에 공백이나 특수문자가 없는지 확인

**잔액이 0으로 표시될 때**:
- Testnet 사이트에서 로그인하여 테스트 자금 받기
- https://testnet.binance.vision/ 접속

**네트워크 오류 발생 시**:
- 인터넷 연결 확인
- 방화벽 설정 확인
- VPN 사용 시 비활성화 후 재시도

### 7. 실제 거래로 전환 (프로덕션)

⚠️ **실제 자금을 사용하기 전에**:
1. 충분한 백테스팅 완료
2. Paper trading으로 최소 1주일 이상 테스트
3. 리스크 관리 전략 검증
4. 소액으로 시작

실제 거래 전환 방법:
1. Binance 메인 사이트에서 실제 API 키 발급
2. `.env` 파일의 API 키를 실제 키로 변경
3. `tests/test_binance_api.py`에서 `exchange.set_sandbox_mode(False)` 설정
4. 또는 해당 라인 제거

---

## 다음 단계

테스트가 성공했다면:
1. ✅ 매매 전략 구현 시작
2. ✅ 백테스팅 시스템 구축
3. ✅ 리스크 관리 모듈 개발
4. ✅ 자동 매매 봇 완성

더 자세한 내용은 `docs/plan-autoTradingSystem.prompt.md` 참조

---

## Upbit API 테스트

Upbit은 한국 원화(KRW) 기반의 암호화폐 거래소입니다.  
별도의 Testnet이 없으므로 **실제 계좌의 API 키**를 사용합니다.  
읽기 전용 권한으로 발급하면 실수로 주문이 나가는 위험이 없습니다.

### 1. Upbit API 키 발급

1. **Upbit 로그인 후 Open API 관리 페이지 접속**  
   - https://upbit.com/mypage/open_api_management

2. **Open API 키 생성**
   - "Open API 키 발급받기" 클릭
   - 2FA 인증 완료
   - 허용 IP 주소 입력 (보안을 위해 본인 IP만 허용 권장)
   - 권한 선택: **자산조회** 체크 (주문/출금은 필요 시에만 추가)

3. **Access Key / Secret Key 복사**  
   - Secret Key는 발급 시 **한 번만 표시**되므로 즉시 저장

### 2. .env 파일 설정

`.env` 파일에 발급받은 키를 입력:

```env
# Upbit (Korea)
UPBIT_ACCESS_KEY=your_access_key_here
UPBIT_SECRET_KEY=your_secret_key_here
```

⚠️ **주의**:
- `.env` 파일은 Git에 커밋되지 않습니다 (.gitignore에 포함됨)
- Secret Key는 절대 외부에 노출하지 마세요
- 출금 권한은 부여하지 않는 것을 권장합니다

### 3. 테스트 실행

```bash
# 방법 1: 배치 파일 사용 (권장)
run_upbit_test.bat

# 방법 2: 직접 실행
venv\Scripts\activate
python tests\test_upbit_api.py
```

### 4. 테스트 항목

| # | 항목 | 인증 필요 | 설명 |
|---|------|-----------|------|
| 1 | 서버 연결 확인 | ❌ Public | 전체/KRW 마켓 수 확인 |
| 2 | 시장 데이터 조회 | ❌ Public | XRP/KRW 현재가, 등락률 |
| 3 | 오더북 조회 | ❌ Public | 매수/매도 호가 Top 5 |
| 4 | 최근 체결 내역 | ❌ Public | 실시간 체결 5건 |
| 5 | 계좌 잔액 조회 | ✅ Private | 보유 자산 목록 |
| 6 | 캔들 데이터 조회 | ❌ Public | 1분봉 5개 |

**실제 테스트 결과 예시**:
```
✅ 연결 성공
✅ 전체 마켓 수: 703개  |  KRW 마켓 수: 243개

📊 XRP/KRW:  현재가 2,023 KRW  |  전일 대비 🔴 -1.51%

📕 매도 호가:  2,027 KRW  -  73,262 XRP
📗 매수 호가:  2,022 KRW  -  23,257 XRP

💰 보유 자산 (계좌 잔액 조회 시)
  KRW     : 보유=  500,000.00000000  잠금=       0.00000000
```

### 5. 문제 해결

**인증 실패 (HTTP 401) 발생 시**:
- `.env` 파일의 키 값에 공백이나 줄바꿈이 없는지 확인
- API 키가 만료되지 않았는지 확인
- 허용 IP 목록에 현재 사용 중인 IP가 포함되어 있는지 확인
- https://upbit.com/mypage/open_api_management 에서 키 재발급

**권한 없음 (HTTP 403) 발생 시**:
- API 키 발급 시 "자산조회" 권한을 체크했는지 확인

**네트워크 오류 발생 시**:
- 인터넷 연결 확인
- 방화벽 설정 확인 (api.upbit.com 포트 443)

### 6. 보안 주의사항

⚠️ **Upbit API는 Testnet이 없으므로 실제 계좌와 연결됩니다**:
1. **출금 권한 금지**: API 키에 절대 출금 권한을 부여하지 마세요
2. **IP 제한**: 허용 IP를 본인 서버/PC IP로 제한하세요
3. **최소 권한**: 필요한 권한만 부여 (조회만 필요하면 자산조회만 체크)
4. **키 보관**: Secret Key는 발급 직후 저장, 분실 시 재발급 필요

### 7. 실제 주문 연동 (선택사항)

주문 기능을 활성화하려면:
1. Upbit에서 API 키에 **주문 권한** 추가 (주문하기/취소하기)
2. `.env`에 `EXCHANGE_NAME=upbit` 설정
3. `trading_config.py` 및 `trading_bot.py` 에서 Upbit 거래소 초기화 확인

---

## 다음 단계
