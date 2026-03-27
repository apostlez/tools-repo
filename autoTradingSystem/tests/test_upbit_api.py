"""
Upbit API Connection Test Script
Upbit REST API v1 기반 테스트
"""

import os
import jwt
import uuid
import hashlib
import hmac
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

UPBIT_BASE_URL = "https://api.upbit.com/v1"


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def get_auth_header(access_key: str, secret_key: str, query: dict = None) -> dict:
    """JWT 인증 헤더 생성"""
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    if query:
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'

    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
    return {'Authorization': f'Bearer {jwt_token}'}


def test_upbit_connection():
    """Test Upbit API connection"""

    print_section("Upbit API Test")

    access_key = os.getenv('UPBIT_ACCESS_KEY')
    secret_key = os.getenv('UPBIT_SECRET_KEY')

    if not access_key or not secret_key:
        print("❌ Error: Upbit API keys not found in .env file")
        print("\nPlease add the following to your .env file:")
        print("UPBIT_ACCESS_KEY=your_access_key")
        print("UPBIT_SECRET_KEY=your_secret_key")
        return False

    print(f"✅ UPBIT_ACCESS_KEY: {access_key[:8]}...")
    print(f"✅ UPBIT_SECRET_KEY: {'*' * 16}")

    # ----------------------------------------------------------------
    # Test 1: Public API - Server health (no auth required)
    # ----------------------------------------------------------------
    print_section("Test 1: 서버 연결 확인 (Public)")

    try:
        resp = requests.get(f"{UPBIT_BASE_URL}/market/all", params={"isDetails": False}, timeout=10)
        resp.raise_for_status()
        markets = resp.json()
        krw_markets = [m for m in markets if m['market'].startswith('KRW-')]
        print(f"✅ 연결 성공")
        print(f"✅ 전체 마켓 수: {len(markets)}개")
        print(f"✅ KRW 마켓 수: {len(krw_markets)}개")
    except requests.RequestException as e:
        print(f"❌ 서버 연결 실패: {e}")
        return False

    # ----------------------------------------------------------------
    # Test 2: XRP/KRW ticker
    # ----------------------------------------------------------------
    print_section("Test 2: 시장 데이터 조회 (XRP/KRW)")

    try:
        resp = requests.get(
            f"{UPBIT_BASE_URL}/ticker",
            params={"markets": "KRW-XRP"},
            timeout=10
        )
        resp.raise_for_status()
        ticker = resp.json()[0]

        print(f"\n📊 XRP/KRW 마켓 정보:")
        print(f"  현재가:       {ticker['trade_price']:,.0f} KRW")
        print(f"  24h 고가:     {ticker['high_price']:,.0f} KRW")
        print(f"  24h 저가:     {ticker['low_price']:,.0f} KRW")
        print(f"  거래량(24h):  {ticker['acc_trade_volume_24h']:,.2f} XRP")
        print(f"  거래대금(24h):{ticker['acc_trade_price_24h']:,.0f} KRW")
        change_pct = ticker['signed_change_rate'] * 100
        change_icon = "🟢" if change_pct >= 0 else "🔴"
        print(f"  전일 대비:   {change_icon} {change_pct:+.2f}%")
    except requests.RequestException as e:
        print(f"❌ 마켓 데이터 조회 실패: {e}")

    # ----------------------------------------------------------------
    # Test 3: Orderbook (Public)
    # ----------------------------------------------------------------
    print_section("Test 3: 오더북 조회 (XRP/KRW, Top 5)")

    try:
        resp = requests.get(
            f"{UPBIT_BASE_URL}/orderbook",
            params={"markets": "KRW-XRP"},
            timeout=10
        )
        resp.raise_for_status()
        ob = resp.json()[0]
        units = ob['orderbook_units']

        print(f"\n📕 매도 호가 (Ask):")
        for u in reversed(units[:5]):
            print(f"  {u['ask_price']:>12,.0f} KRW  -  {u['ask_size']:>10.4f} XRP")

        print(f"\n📗 매수 호가 (Bid):")
        for u in units[:5]:
            print(f"  {u['bid_price']:>12,.0f} KRW  -  {u['bid_size']:>10.4f} XRP")
    except requests.RequestException as e:
        print(f"❌ 오더북 조회 실패: {e}")

    # ----------------------------------------------------------------
    # Test 4: Recent trades (Public)
    # ----------------------------------------------------------------
    print_section("Test 4: 최근 체결 내역 (XRP/KRW, 5건)")

    try:
        resp = requests.get(
            f"{UPBIT_BASE_URL}/trades/ticks",
            params={"market": "KRW-XRP", "count": 5},
            timeout=10
        )
        resp.raise_for_status()
        trades = resp.json()

        print(f"\n📈 최근 체결 내역:")
        for t in trades:
            side_icon = "🟢" if t['ask_bid'] == 'BID' else "🔴"
            label = "매수" if t['ask_bid'] == 'BID' else "매도"
            trade_time = t.get('trade_time_utc') or t.get('trade_time') or t.get('timestamp', '')
            print(f"  {side_icon} {label}  {t['trade_price']:>12,.0f} KRW  "
                  f"{t['trade_volume']:>10.4f} XRP  [{trade_time}]")
    except requests.RequestException as e:
        print(f"❌ 체결 내역 조회 실패: {e}")

    # ----------------------------------------------------------------
    # Test 5: Account balance (Private - requires valid key)
    # ----------------------------------------------------------------
    print_section("Test 5: 계좌 잔액 조회 (Private)")

    try:
        headers = get_auth_header(access_key, secret_key)
        resp = requests.get(f"{UPBIT_BASE_URL}/accounts", headers=headers, timeout=10)

        if resp.status_code == 401:
            data = resp.json()
            print(f"❌ 인증 실패 (HTTP 401)")
            print(f"   오류 코드: {data.get('error', {}).get('name', 'unknown')}")
            print(f"   메시지:   {data.get('error', {}).get('message', '')}")
            print("\n💡 해결 방법:")
            print("   - Upbit 개인 API 키가 올바른지 확인하세요")
            print("   - https://upbit.com/mypage/open_api_management 에서 키를 재발급하세요")
            print("   - IP 허용 목록을 확인하세요")
        elif resp.status_code == 403:
            print(f"❌ 권한 없음 (HTTP 403): API 키의 조회 권한을 확인하세요")
        else:
            resp.raise_for_status()
            accounts = resp.json()

            if not accounts:
                print("  ⚠️  잔액 없음 (보유 자산이 없거나 빈 계좌)")
            else:
                print(f"\n💰 보유 자산:")
                for acc in accounts:
                    balance = float(acc['balance'])
                    locked = float(acc['locked'])
                    if balance > 0 or locked > 0:
                        currency = acc['currency']
                        avg_price = float(acc.get('avg_buy_price', 0))
                        print(f"  {currency:8s}: 보유={balance:>16.8f}  "
                              f"잠금={locked:>12.8f}  "
                              f"평균매수가={avg_price:>12,.2f}")
            print("✅ 인증 성공")

    except requests.RequestException as e:
        print(f"❌ 잔액 조회 실패: {e}")

    # ----------------------------------------------------------------
    # Test 6: Candle data (Public)
    # ----------------------------------------------------------------
    print_section("Test 6: 캔들 데이터 조회 (XRP/KRW, 1분봉 5개)")

    try:
        resp = requests.get(
            f"{UPBIT_BASE_URL}/candles/minutes/1",
            params={"market": "KRW-XRP", "count": 5},
            timeout=10
        )
        resp.raise_for_status()
        candles = resp.json()

        print(f"\n🕯️  최근 1분봉 (XRP/KRW):")
        print(f"  {'시간':<20} {'시가':>10} {'고가':>10} {'저가':>10} {'종가':>10}")
        print(f"  {'-'*62}")
        for c in candles:
            print(f"  {c['candle_date_time_kst']:<20} "
                  f"{c['opening_price']:>10,.2f} "
                  f"{c['high_price']:>10,.2f} "
                  f"{c['low_price']:>10,.2f} "
                  f"{c['trade_price']:>10,.2f}")
    except requests.RequestException as e:
        print(f"❌ 캔들 데이터 조회 실패: {e}")

    print_section("모든 테스트 완료")
    print("\n✅ Upbit Public API는 정상 동작합니다")
    print("✅ Private API(계좌 조회) 결과는 Test 5를 확인하세요")
    return True


if __name__ == "__main__":
    print("\n🚀 Upbit API 테스트 시작...")
    print(f"📅 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    success = test_upbit_connection()

    if success:
        print("\n" + "="*60)
        print("  🎉 테스트가 완료되었습니다!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("  ❌ 설정을 확인하고 다시 시도하세요")
        print("="*60)
