"""
Binance API 상세 디버그 스크립트
Account Balance 에러 진단 및 해결
"""

import ccxt
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

def debug_binance_api():
    """Binance API 연결 문제를 상세하게 진단"""
    
    print("="*70)
    print("  Binance API 디버그 도구")
    print("="*70)
    
    # Step 1: 환경 변수 확인
    print("\n[Step 1] 환경 변수 확인")
    print("-" * 70)
    
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ .env 파일에서 API 키를 찾을 수 없습니다!")
        print("\n해결방법:")
        print("1. 프로젝트 루트에 .env 파일 생성")
        print("2. 다음 내용 추가:")
        print("   BINANCE_API_KEY=your_key")
        print("   BINANCE_SECRET_KEY=your_secret")
        return
    
    print(f"✅ BINANCE_API_KEY: {api_key[:8]}...{api_key[-4:]} (길이: {len(api_key)})")
    print(f"✅ BINANCE_SECRET_KEY: {secret_key[:8]}...{secret_key[-4:]} (길이: {len(secret_key)})")
    
    # API 키 형식 검증
    if len(api_key) != 64:
        print(f"⚠️  경고: API Key 길이가 비정상적입니다 (정상: 64, 현재: {len(api_key)})")
    if len(secret_key) != 64:
        print(f"⚠️  경고: Secret Key 길이가 비정상적입니다 (정상: 64, 현재: {len(secret_key)})")
    
    # Step 2: 시스템 시간 확인
    print("\n[Step 2] 시스템 시간 확인")
    print("-" * 70)
    
    local_time = time.time() * 1000
    print(f"로컬 시간: {datetime.fromtimestamp(local_time/1000).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"타임스탬프: {int(local_time)}")
    
    # Step 3: Exchange 객체 생성 (여러 방법 시도)
    print("\n[Step 3] Exchange 객체 생성 테스트")
    print("-" * 70)
    
    configs = [
        {
            'name': 'Testnet (기본 설정)',
            'config': {
                'apiKey': api_key,
                'secret': secret_key,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True,
                }
            },
            'sandbox': True
        },
        {
            'name': 'Testnet (recvWindow 확장)',
            'config': {
                'apiKey': api_key,
                'secret': secret_key,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True,
                    'recvWindow': 60000,
                }
            },
            'sandbox': True
        },
        {
            'name': 'Mainnet (혹시 실제 키를 사용 중인 경우)',
            'config': {
                'apiKey': api_key,
                'secret': secret_key,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True,
                }
            },
            'sandbox': False
        }
    ]
    
    for idx, test_config in enumerate(configs, 1):
        print(f"\n테스트 {idx}: {test_config['name']}")
        print("-" * 70)
        
        try:
            exchange = ccxt.binance(test_config['config'])
            exchange.set_sandbox_mode(test_config['sandbox'])
            
            # API URL 확인
            api_url = exchange.urls.get('api', {})
            if isinstance(api_url, dict):
                api_url = api_url.get('public', 'unknown')
            print(f"📡 API URL: {api_url}")
            
            # 서버 시간 확인
            print("🔍 서버 연결 테스트...")
            server_time = exchange.fetch_time()
            server_dt = datetime.fromtimestamp(server_time / 1000)
            print(f"✅ 서버 시간: {server_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            time_diff = abs(local_time - server_time)
            print(f"⏱️  시간 차이: {time_diff:.0f}ms")
            
            if time_diff > 5000:
                print(f"⚠️  경고: 시간 차이가 큽니다 ({time_diff:.0f}ms)")
                print("   시스템 시간을 동기화하세요")
            
            # Balance 조회 시도
            print("\n🔍 Balance 조회 시도...")
            
            try:
                balance = exchange.fetch_balance()
                print("✅ ✅ ✅ Balance 조회 성공! ✅ ✅ ✅")
                print(f"\n이 설정을 사용하세요: {test_config['name']}")
                
                # 잔액 표시
                print("\n💰 계좌 잔액:")
                has_balance = False
                for currency, amount in balance['total'].items():
                    if amount > 0:
                        has_balance = True
                        free = balance['free'].get(currency, 0)
                        used = balance['used'].get(currency, 0)
                        print(f"  {currency:8s}: Total={amount:12.8f}  Free={free:12.8f}  Used={used:12.8f}")
                
                if not has_balance:
                    print("  ⚠️  잔액 없음 (테스트넷의 경우 자금 받기 필요)")
                    print("  👉 https://testnet.binance.vision/ 에서 테스트 자금 받기")
                
                return True
                
            except ccxt.AuthenticationError as auth_err:
                print(f"❌ 인증 실패: {auth_err}")
                error_msg = str(auth_err).lower()
                
                if 'api-key' in error_msg or 'invalid' in error_msg:
                    print("   원인: API 키가 잘못되었거나 만료됨")
                    print("   해결: https://testnet.binance.vision/ 에서 새 키 발급")
                elif 'signature' in error_msg:
                    print("   원인: 서명 오류 (Secret Key 문제)")
                    print("   해결: Secret Key 재확인")
                elif 'permission' in error_msg or 'unauthorized' in error_msg:
                    print("   원인: API 키 권한 부족")
                    print("   해결: 새 API 키 발급 시 'Enable Reading' 권한 확인")
                    
            except ccxt.InvalidNonce as nonce_err:
                print(f"❌ 타임스탬프 오류: {nonce_err}")
                print("   원인: 시스템 시간이 서버와 맞지 않음")
                print("   해결: Windows 시간 설정 → 자동 시간 설정 활성화")
                
            except Exception as e:
                print(f"❌ 기타 오류: {type(e).__name__}: {e}")
                
        except Exception as e:
            print(f"❌ Exchange 초기화 실패: {type(e).__name__}: {e}")
    
    # Step 4: 문제 해결 가이드
    print("\n" + "="*70)
    print("  문제 해결 가이드")
    print("="*70)
    
    print("\n1️⃣  API 키 재발급")
    print("   • https://testnet.binance.vision/ 접속")
    print("   • GitHub로 로그인")
    print("   • 기존 키 삭제 후 새로 생성")
    print("   • .env 파일 업데이트")
    
    print("\n2️⃣  Testnet vs Mainnet 확인")
    print("   • Testnet 키: https://testnet.binance.vision/")
    print("   • Mainnet 키: https://www.binance.com/")
    print("   • 두 개는 호환되지 않음!")
    
    print("\n3️⃣  시스템 시간 동기화")
    print("   • Windows: 설정 → 시간 및 언어 → 자동으로 시간 설정")
    print("   • 시간대가 올바른지 확인")
    
    print("\n4️⃣  방화벽/VPN 확인")
    print("   • VPN 사용 시 비활성화 후 재시도")
    print("   • 회사/학교 네트워크의 경우 관리자에게 문의")
    
    print("\n5️⃣  API 키 권한 확인")
    print("   • 최소 'Enable Reading' 권한 필요")
    print("   • 'Enable Spot & Margin Trading' 권한 (주문 생성 시 필요)")
    
    return False

if __name__ == "__main__":
    print("\n🚀 Binance API 디버그 시작...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    success = debug_binance_api()
    
    if not success:
        print("\n" + "="*70)
        print("  ⚠️  모든 설정에서 실패했습니다")
        print("="*70)
        print("\n위의 해결 가이드를 참고하여 문제를 해결하세요.")
        print("추가 도움이 필요하면 에러 메시지를 복사하여 문의하세요.")
    
    print("\n")
