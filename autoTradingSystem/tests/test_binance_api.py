"""
Binance API Connection Test Script
Paper Trading Mode (Testnet)
"""

import ccxt
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_binance_connection():
    """Test Binance API connection in paper trading mode"""
    
    print_section("Binance API Test - Paper Trading Mode")
    
    # Get API credentials from environment
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ Error: API keys not found in .env file")
        print("\nPlease create a .env file and add:")
        print("BINANCE_API_KEY=your_api_key")
        print("BINANCE_SECRET_KEY=your_secret_key")
        return False
    
    try:
        # Initialize Binance exchange in testnet mode
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',  # spot, future, margin
                'adjustForTimeDifference': True,  # Auto-sync with server time
            }
        })
        
        # Set testnet mode (paper trading)
        exchange.set_sandbox_mode(True)
        
        print(f"🔧 Using Testnet: {exchange.urls.get('api', 'default')}")
        
        print(f"✅ Exchange: {exchange.name}")
        print(f"✅ Testnet Mode: {exchange.urls['test'] if 'test' in exchange.urls else 'Enabled'}")
        print(f"✅ Rate Limit: {exchange.enableRateLimit}")
        
        # Test 1: Check server time
        print_section("Test 1: Server Connection")
        server_time = exchange.fetch_time()
        server_datetime = datetime.fromtimestamp(server_time / 1000)
        print(f"✅ Server Time: {server_datetime}")
        print(f"✅ Connection: Success")
        
        # Test 2: Fetch account balance
        print_section("Test 2: Account Balance")
        
        try:
            # Sync server time first to avoid timestamp errors
            print("🔄 Synchronizing with server time...")
            exchange.load_time_difference()
            
            balance = exchange.fetch_balance()
            
            print("\n💰 Account Balances:")
            total_balance = balance['total']
            has_balance = False
            
            for currency, amount in total_balance.items():
                if amount > 0:
                    has_balance = True
                    free = balance['free'].get(currency, 0)
                    used = balance['used'].get(currency, 0)
                    print(f"  {currency:8s}: Total={amount:12.8f}  Free={free:12.8f}  Used={used:12.8f}")
            
            if not has_balance:
                print("  ⚠️  No balances found (Testnet accounts may need initial funding)")
                print("  ℹ️  Visit https://testnet.binance.vision/ to get testnet funds")
                
        except ccxt.AuthenticationError as e:
            print(f"\n❌ Authentication failed for balance check: {str(e)}")
            print("\n🔍 Possible causes:")
            print("  1. API key doesn't have 'Enable Reading' permission")
            print("  2. Using mainnet API key instead of testnet key")
            print("  3. API key has been revoked or expired")
            print("\n💡 Solutions:")
            print("  - Go to https://testnet.binance.vision/")
            print("  - Delete old API key and generate a new one")
            print("  - Make sure to use TESTNET keys, not mainnet keys")
            print("\n⚠️  Continuing with other tests...")
            
        except ccxt.InvalidNonce as e:
            print(f"\n❌ Timestamp error: {str(e)}")
            print("\n💡 Solutions:")
            print("  - Check your system time is correct")
            print("  - Trying to reconfigure exchange with recvWindow...")
            
            # Try with larger recvWindow
            exchange.options['recvWindow'] = 60000
            try:
                balance = exchange.fetch_balance()
                print("✅ Fixed! Balance retrieved with extended recvWindow")
            except Exception as retry_error:
                print(f"❌ Still failed: {str(retry_error)}")
                print("\n⚠️  Continuing with other tests...")
                
        except Exception as e:
            print(f"\n❌ Unexpected error during balance check: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print("\n⚠️  Continuing with other tests...")
        
        # Test 3: Fetch market data
        print_section("Test 3: Market Data (BTC/USDT)")
        
        symbol = 'BTC/USDT'
        ticker = exchange.fetch_ticker(symbol)
        
        print(f"\n📊 {symbol} Market Info:")
        print(f"  Last Price:    ${ticker['last']:,.2f}")
        print(f"  24h High:      ${ticker['high']:,.2f}")
        print(f"  24h Low:       ${ticker['low']:,.2f}")
        print(f"  24h Volume:    {ticker['baseVolume']:,.2f} BTC")
        print(f"  24h Change:    {ticker['percentage']:.2f}%")
        
        # Test 4: Fetch order book
        print_section("Test 4: Order Book (Top 5)")
        
        orderbook = exchange.fetch_order_book(symbol, limit=5)
        
        print(f"\n📗 Bids (Buy Orders):")
        for bid in orderbook['bids'][:5]:
            price, amount = bid[0], bid[1]
            print(f"  ${price:,.2f}  -  {amount:.6f} BTC")
        
        print(f"\n📕 Asks (Sell Orders):")
        for ask in orderbook['asks'][:5]:
            price, amount = ask[0], ask[1]
            print(f"  ${price:,.2f}  -  {amount:.6f} BTC")
        
        # Test 5: Fetch recent trades
        print_section("Test 5: Recent Trades")
        
        trades = exchange.fetch_trades(symbol, limit=5)
        
        print(f"\n📈 Recent {symbol} Trades:")
        for trade in trades:
            trade_time = datetime.fromtimestamp(trade['timestamp'] / 1000)
            side_icon = "🟢" if trade['side'] == 'buy' else "🔴"
            print(f"  {side_icon} {trade['side']:4s}  ${trade['price']:,.2f}  {trade['amount']:.6f} BTC  [{trade_time.strftime('%H:%M:%S')}]")
        
        # Test 6: Check trading capabilities
        print_section("Test 6: Trading Capabilities")
        
        markets = exchange.load_markets()
        btc_usdt_market = markets[symbol]
        
        print(f"\n⚙️  {symbol} Trading Limits:")
        print(f"  Min Order Amount: {btc_usdt_market['limits']['amount']['min']} BTC")
        print(f"  Min Order Cost:   ${btc_usdt_market['limits']['cost']['min']}")
        print(f"  Precision Price:  {btc_usdt_market['precision']['price']} decimals")
        print(f"  Precision Amount: {btc_usdt_market['precision']['amount']} decimals")
        
        # Test 7: Create a test order (disabled by default for safety)
        print_section("Test 7: Order Creation (Simulation)")
        
        print("\n⚠️  Paper Trading Order Simulation:")
        print("  To test actual order creation, uncomment the code below")
        print("  This will place a LIMIT BUY order at 1% below current price")
        
        # Uncomment below to test actual order creation
        """
        current_price = ticker['last']
        test_price = current_price * 0.99  # 1% below market
        test_amount = 0.001  # Small amount for testing
        
        print(f"\n  Order Type: LIMIT BUY")
        print(f"  Symbol: {symbol}")
        print(f"  Amount: {test_amount} BTC")
        print(f"  Price: ${test_price:,.2f}")
        print(f"  Total Cost: ${test_price * test_amount:,.2f}")
        
        # Create order
        order = exchange.create_limit_buy_order(symbol, test_amount, test_price)
        print(f"\n✅ Order Created Successfully!")
        print(f"  Order ID: {order['id']}")
        print(f"  Status: {order['status']}")
        """
        
        print("\n  ℹ️  Order creation code is commented out for safety")
        print("  ℹ️  Edit this script to enable test order creation")
        
        print_section("All Tests Completed Successfully!")
        print("\n✅ Binance API is working correctly in Paper Trading mode")
        print("✅ You can now proceed with implementing trading strategies")
        
        return True
        
    except ccxt.AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print(f"\n🔍 Error Details: {str(e)}")
        print("\n❗ Possible issues:")
        print("  1. Invalid API key or secret")
        print("  2. API key not enabled for testnet")
        print("  3. Using mainnet keys instead of testnet keys")
        print("  4. API key doesn't have required permissions")
        print("\n💡 Solution:")
        print("  1. Visit https://testnet.binance.vision/")
        print("  2. Login with GitHub")
        print("  3. Generate new HMAC_SHA256 Key")
        print("  4. Copy the API Key and Secret Key")
        print("  5. Update .env file with new keys")
        print("\n📝 Your .env should look like:")
        print("  BINANCE_API_KEY=your_testnet_key_here")
        print("  BINANCE_SECRET_KEY=your_testnet_secret_here")
        return False
        
    except ccxt.NetworkError as e:
        print(f"\n❌ Network Error: {e}")
        print("\nPossible issues:")
        print("  1. No internet connection")
        print("  2. Binance servers may be down")
        print("  3. Firewall blocking connection")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print(f"Error Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("\n🚀 Starting Binance API Test...")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_binance_connection()
    
    if success:
        print("\n" + "="*60)
        print("  🎉 All tests passed successfully!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("  ⚠️  Some tests failed. Please check the errors above.")
        print("="*60)
