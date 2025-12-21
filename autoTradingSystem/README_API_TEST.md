# Binance API 테스트 가이드

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
run_test.bat

# 방법 2: 직접 실행
venv\Scripts\activate
python test_binance_api.py
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
1. `test_binance_api.py` 파일 열기
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
3. `test_binance_api.py`에서 `exchange.set_sandbox_mode(False)` 설정
4. 또는 해당 라인 제거

---

## 다음 단계

테스트가 성공했다면:
1. ✅ 매매 전략 구현 시작
2. ✅ 백테스팅 시스템 구축
3. ✅ 리스크 관리 모듈 개발
4. ✅ 자동 매매 봇 완성

더 자세한 내용은 `plan-autoTradingSystem.prompt.md` 참조
