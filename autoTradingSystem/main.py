"""
Main Trading Bot Runner
트레이딩 봇 실행 메인 스크립트
"""

import os
import sys
import ccxt
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.trading_bot import TradingBot
from src.risk_manager import RiskManager
from src.strategies import RSIStrategy, MACDStrategy, MovingAverageCrossStrategy, OBVStrategy, RSIOBVStrategy
from src.strategies.custom_strategies import MACDRSIOBVStrategy
from config.trading_config import (
    EXCHANGE_CONFIG,
    TRADING_CONFIG,
    STRATEGY_CONFIG,
    RISK_CONFIG,
    LOGGING_CONFIG
)


def setup_logging():
    """로깅 설정"""
    # Windows 콘솔 UTF-8 인코딩 설정
    import sys
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python 3.6 이하 버전
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    # 로그 디렉토리 생성
    os.makedirs('logs', exist_ok=True)
    
    # 루트 로거 설정
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # 콘솔 핸들러 (UTF-8 인코딩 지원)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # 파일 핸들러 (날짜별 로테이팅, UTF-8 인코딩)
    # - when='midnight': 자정마다 새 파일로 롤오버
    # - backupCount: 보관 일수 (오래된 파일 자동 삭제)
    # - suffix: 롤오버된 파일명에 날짜 접미사 추가 (예: trading_bot.log.2026-04-03)
    file_handler = TimedRotatingFileHandler(
        LOGGING_CONFIG['file'],
        when='midnight',
        interval=1,
        backupCount=LOGGING_CONFIG['backup_days'],
        encoding='utf-8',
        utc=False
    )
    file_handler.suffix = '%Y-%m-%d'
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        LOGGING_CONFIG['format'],
        datefmt=LOGGING_CONFIG['date_format']
    )
    file_handler.setFormatter(file_formatter)
    
    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def create_exchange():
    """거래소 객체 생성 (EXCHANGE_NAME 설정에 따라 Upbit 또는 Binance 사용)"""
    load_dotenv()

    exchange_name = EXCHANGE_CONFIG['name'].lower()
    logging.info(f"🏦 Exchange: {exchange_name.upper()}")

    if exchange_name == 'upbit':
        return _create_upbit_exchange()
    else:
        # 기본값: Binance (백업)
        return _create_binance_exchange()


def _create_upbit_exchange():
    """Upbit 거래소 객체 생성"""
    access_key = os.getenv('UPBIT_ACCESS_KEY')
    secret_key = os.getenv('UPBIT_SECRET_KEY')

    if not access_key or not secret_key:
        raise ValueError(
            "Upbit API keys not found in .env file. "
            "Please set UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY."
        )

    exchange = ccxt.upbit({
        'apiKey': access_key,
        'secret': secret_key,
        'enableRateLimit': True,
    })

    # Upbit은 testnet을 지원하지 않음
    if EXCHANGE_CONFIG['testnet']:
        logging.warning("⚠️  Upbit does not support testnet. 실제 거래소에 연결됩니다.")
        logging.warning("⚠️  DRY_RUN=true 설정으로 실제 주문이 차단되는지 확인하세요.")
    logging.info("🔧 Using Upbit Exchange")
    return exchange


def _create_binance_exchange():
    """Binance 거래소 객체 생성 (백업용)"""
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')

    if not api_key or not secret_key:
        raise ValueError(
            "Binance API keys not found in .env file. "
            "Please set BINANCE_API_KEY and BINANCE_SECRET_KEY."
        )

    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
            'adjustForTimeDifference': True,
        }
    })

    # Testnet 설정
    if EXCHANGE_CONFIG['testnet']:
        exchange.set_sandbox_mode(True)
        logging.info("🔧 Using Binance Testnet (Paper Trading)")
    else:
        logging.warning("⚠️  LIVE TRADING MODE - Real money at risk!")

    logging.info("🔧 Using Binance Exchange")
    return exchange


def create_strategy():
    """전략 객체 생성"""
    strategy_name = STRATEGY_CONFIG['name']
    
    if strategy_name == 'RSIStrategy':
        params = STRATEGY_CONFIG['rsi']
        strategy = RSIStrategy(
            oversold=params['oversold'],
            overbought=params['overbought'],
            rsi_period=params['rsi_period']
        )
    elif strategy_name == 'MACDStrategy':
        strategy = MACDStrategy()
    elif strategy_name == 'MovingAverageCrossStrategy':
        params = STRATEGY_CONFIG['ma_cross']
        strategy = MovingAverageCrossStrategy(
            fast_period=params['fast_period'],
            slow_period=params['slow_period']
        )
    elif strategy_name == 'OBVStrategy':
        params = STRATEGY_CONFIG['obv']
        strategy = OBVStrategy(
            obv_ma_period=params['obv_ma_period'],
            divergence_lookback=params['divergence_lookback']
        )
    elif strategy_name == 'RSIOBVStrategy':
        params = STRATEGY_CONFIG['rsi_obv']
        strategy = RSIOBVStrategy(
            oversold=params['oversold'],
            overbought=params['overbought'],
            rsi_period=params['rsi_period'],
            obv_ma_period=params['obv_ma_period'],
            obv_weight=params['obv_weight']
        )
    elif strategy_name == 'MACDRSIOBVStrategy':
        params = STRATEGY_CONFIG['macd_rsi_obv']
        strategy = MACDRSIOBVStrategy(
            macd_fast=params['macd_fast'],
            macd_slow=params['macd_slow'],
            macd_signal=params['macd_signal'],
            rsi_period=params['rsi_period'],
            rsi_buy_threshold=params['rsi_buy_threshold'],
            rsi_sell_threshold=params['rsi_sell_threshold'],
            obv_ma_period=params['obv_ma_period'],
        )
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    
    logging.info(f"📊 Strategy: {strategy.name}")
    logging.info(f"   Parameters: {strategy.parameters}")
    
    return strategy


def create_risk_manager():
    """리스크 관리자 생성"""
    risk_manager = RiskManager(RISK_CONFIG)
    
    logging.info(f"🛡️  Risk Manager: {risk_manager}")
    logging.info(f"   Config: {risk_manager.get_config()}")
    
    return risk_manager


def print_configuration():
    """설정 출력"""
    print("\n" + "="*70)
    print("  AUTO TRADING SYSTEM - Configuration")
    print("="*70)
    
    print("\n📊 Trading Configuration:")
    print(f"   Symbol: {TRADING_CONFIG['symbol']}")
    print(f"   Timeframe: {TRADING_CONFIG['timeframe']}")
    print(f"   Update Interval: {TRADING_CONFIG['update_interval']}s")
    print(f"   Initial Balance: ${TRADING_CONFIG['initial_balance']:,.2f}")
    print(f"   Mode: {'DRY RUN (Simulation)' if TRADING_CONFIG['dry_run'] else '⚠️  LIVE TRADING'}")
    
    print("\n🎯 Strategy:")
    print(f"   Name: {STRATEGY_CONFIG['name']}")
    if STRATEGY_CONFIG['name'] == 'RSIStrategy':
        print(f"   Parameters: {STRATEGY_CONFIG['rsi']}")
    elif STRATEGY_CONFIG['name'] == 'MACDStrategy':
        print(f"   Parameters: {STRATEGY_CONFIG['macd']}")
    elif STRATEGY_CONFIG['name'] == 'MovingAverageCrossStrategy':
        print(f"   Parameters: {STRATEGY_CONFIG['ma_cross']}")
    elif STRATEGY_CONFIG['name'] == 'OBVStrategy':
        print(f"   Parameters: {STRATEGY_CONFIG['obv']}")
    elif STRATEGY_CONFIG['name'] == 'RSIOBVStrategy':
        print(f"   Parameters: {STRATEGY_CONFIG['rsi_obv']}")
    elif STRATEGY_CONFIG['name'] == 'MACDRSIOBVStrategy':
        print(f"   Parameters: {STRATEGY_CONFIG['macd_rsi_obv']}")
    
    print("\n🛡️  Risk Management:")
    print(f"   Max Position Size: {RISK_CONFIG['max_position_size']*100:.0f}%")
    print(f"   Stop Loss: {RISK_CONFIG['stop_loss_pct']*100:.0f}%")
    print(f"   Take Profit: {RISK_CONFIG['take_profit_pct']*100:.0f}%")
    print(f"   Max Daily Loss: {RISK_CONFIG['max_daily_loss']*100:.0f}%")
    print(f"   Max Positions: {RISK_CONFIG['max_positions']}")
    print(f"   Risk/Reward Ratio: {RISK_CONFIG['risk_reward_ratio']:.1f}:1")
    
    print("\n🔧 Exchange:")
    print(f"   Name: {EXCHANGE_CONFIG['name'].upper()}")
    if EXCHANGE_CONFIG['name'].lower() == 'upbit':
        print(f"   Testnet: N/A (Upbit은 testnet 미지원)")
        print(f"   ※ Upbit 심볼 형식 예시: XRP/KRW, BTC/KRW")
    else:
        print(f"   Testnet: {EXCHANGE_CONFIG['testnet']}")
        print(f"   ※ Binance 심볼 형식 예시: XRP/USDT, BTC/USDT")
    
    print("\n" + "="*70)


def main():
    """메인 함수"""
    print("\n" + "🤖 " + "="*66 + " 🤖")
    print("       AUTO TRADING SYSTEM - Algorithmic Trading Bot")
    print("🤖 " + "="*66 + " 🤖\n")
    
    # 로깅 설정
    logger = setup_logging()
    logger.info("="*70)
    logger.info("Auto Trading System Starting...")
    logger.info("="*70)
    
    # 설정 출력
    print_configuration()
    
    # 사용자 확인 (LIVE 모드인 경우)
    if not TRADING_CONFIG['dry_run']:
        print("\n⚠️  WARNING: LIVE TRADING MODE")
        print("This will use REAL MONEY on your account!")
        response = input("\nAre you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    try:
        # 컴포넌트 생성
        logger.info("\n🔧 Initializing components...")
        exchange = create_exchange()
        strategy = create_strategy()
        risk_manager = create_risk_manager()
        
        # 트레이딩 봇 생성
        bot = TradingBot(
            exchange=exchange,
            strategy=strategy,
            risk_manager=risk_manager,
            config=TRADING_CONFIG
        )
        
        # 봇 실행
        print("\n✅ All components initialized successfully!")
        print("\nPress Ctrl+C to stop the bot\n")
        
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Bot stopped by user")
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}", exc_info=True)
    finally:
        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()
