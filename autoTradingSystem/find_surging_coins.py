"""
실시간 가격 급등 종목 감지 스크립트
Real-time Surging Coins Detector
"""

import ccxt
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from collections import defaultdict

# Load environment variables
load_dotenv()


class SurgingCoinsDetector:
    """가격 급등 종목을 실시간으로 감지하는 클래스"""
    
    def __init__(self, threshold=3.0, interval=60, min_volume=100000):
        """
        Args:
            threshold (float): 급등 감지 기준 (%, 기본값 3.0%)
            interval (int): 체크 간격 (초, 기본값 60초)
            min_volume (float): 최소 거래량 필터 (USDT, 기본값 100,000)
        """
        self.threshold = threshold
        self.interval = interval
        self.min_volume = min_volume
        self.previous_prices = {}
        self.surge_history = defaultdict(list)
        
        # Initialize exchange
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,
            }
        })
        
        # Set testnet mode (paper trading)
        # Comment out the next line to use mainnet
        self.exchange.set_sandbox_mode(True)
        
        print(f"🔧 Exchange: {self.exchange.name}")
        print(f"🔧 Mode: {'Testnet' if self.exchange.urls.get('test') else 'Mainnet'}")
        print(f"📊 Threshold: {self.threshold}%")
        print(f"⏱️  Check Interval: {self.interval} seconds")
        print(f"💰 Min Volume: ${self.min_volume:,.0f}")
        print("="*70)
    
    def get_usdt_pairs(self, tickers):
        """USDT 페어만 필터링"""
        return {
            symbol: ticker 
            for symbol, ticker in tickers.items() 
            if symbol.endswith('/USDT') and ticker.get('quoteVolume', 0) >= self.min_volume
        }
    
    def detect_surge(self):
        """가격 급등 감지"""
        try:
            # Fetch all tickers
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 가격 데이터 조회 중...")
            tickers = self.exchange.fetch_tickers()
            
            # Filter USDT pairs with sufficient volume
            usdt_pairs = self.get_usdt_pairs(tickers)
            print(f"📌 모니터링 중인 페어: {len(usdt_pairs)}개")
            
            surging_coins = []
            
            for symbol, ticker in usdt_pairs.items():
                current_price = ticker.get('last')
                volume = ticker.get('quoteVolume', 0)
                
                if not current_price:
                    continue
                
                # Calculate price change if we have previous data
                if symbol in self.previous_prices:
                    previous_price = self.previous_prices[symbol]
                    change_pct = ((current_price - previous_price) / previous_price) * 100
                    
                    # Check if surge threshold is met
                    if change_pct >= self.threshold:
                        surge_info = {
                            'symbol': symbol,
                            'price': current_price,
                            'previous_price': previous_price,
                            'change_pct': change_pct,
                            'volume': volume,
                            'timestamp': datetime.now()
                        }
                        surging_coins.append(surge_info)
                        self.surge_history[symbol].append(surge_info)
                
                # Update price history
                self.previous_prices[symbol] = current_price
            
            # Display results
            if surging_coins:
                print(f"\n🚀 급등 종목 감지: {len(surging_coins)}개")
                print("-" * 70)
                
                # Sort by change percentage
                surging_coins.sort(key=lambda x: x['change_pct'], reverse=True)
                
                for coin in surging_coins:
                    print(f"🔥 {coin['symbol']:<12} | "
                          f"가격: ${coin['price']:>10.4f} | "
                          f"상승률: +{coin['change_pct']:>6.2f}% | "
                          f"거래량: ${coin['volume']:>12,.0f}")
                
                print("-" * 70)
            else:
                print(f"✅ 급등 종목 없음 (기준: {self.threshold}% 이상)")
            
            return surging_coins
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def run(self, duration=None):
        """
        실시간 모니터링 시작
        
        Args:
            duration (int): 실행 시간 (초). None이면 무한 실행
        """
        print(f"\n🎯 가격 급등 모니터링 시작!")
        print(f"⏱️  체크 간격: {self.interval}초")
        if duration:
            print(f"⏱️  실행 시간: {duration}초")
        print("Press Ctrl+C to stop\n")
        
        start_time = time.time()
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n{'='*70}")
                print(f"Iteration #{iteration}")
                print(f"{'='*70}")
                
                # Detect surging coins
                surging_coins = self.detect_surge()
                
                # Check if duration limit is reached
                if duration and (time.time() - start_time) >= duration:
                    print(f"\n⏰ 실행 시간 종료 ({duration}초)")
                    break
                
                # Wait for next iteration
                print(f"\n⏳ {self.interval}초 후 다음 체크...")
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """급등 감지 요약 출력"""
        print("\n" + "="*70)
        print("📊 급등 감지 요약")
        print("="*70)
        
        if not self.surge_history:
            print("급등한 종목이 없습니다.")
            return
        
        # Sort by number of surges
        sorted_coins = sorted(
            self.surge_history.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        print(f"\n총 {len(sorted_coins)}개 종목에서 급등 감지됨:\n")
        
        for symbol, surges in sorted_coins[:20]:  # Top 20
            surge_count = len(surges)
            max_change = max(s['change_pct'] for s in surges)
            avg_change = sum(s['change_pct'] for s in surges) / surge_count
            latest_price = surges[-1]['price']
            
            print(f"  {symbol:<12} | "
                  f"급등 횟수: {surge_count:>2}회 | "
                  f"최대: +{max_change:>6.2f}% | "
                  f"평균: +{avg_change:>6.2f}% | "
                  f"현재가: ${latest_price:>10.4f}")
        
        print("="*70)


def main():
    """메인 실행 함수"""
    print("="*70)
    print("  🚀 Binance 실시간 가격 급등 종목 감지기")
    print("="*70)
    
    # 설정값 (필요시 수정)
    THRESHOLD = 3.0        # 급등 기준 (%)
    INTERVAL = 60          # 체크 간격 (초)
    MIN_VOLUME = 100000    # 최소 거래량 ($USDT)
    DURATION = None        # 실행 시간 (초), None = 무한
    
    # Detector 생성 및 실행
    detector = SurgingCoinsDetector(
        threshold=THRESHOLD,
        interval=INTERVAL,
        min_volume=MIN_VOLUME
    )
    
    detector.run(duration=DURATION)


if __name__ == "__main__":
    main()
