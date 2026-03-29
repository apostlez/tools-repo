"""
Trading Configuration
트레이딩 봇 설정 파일

Default 값을 정의하고, .env 파일이 있으면 해당 값으로 오버라이드합니다.
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


def get_env_bool(key: str, default: bool) -> bool:
    """환경변수를 bool로 변환"""
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('true', '1', 'yes', 'on')


def get_env_float(key: str, default: float) -> float:
    """환경변수를 float로 변환"""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def get_env_int(key: str, default: int) -> int:
    """환경변수를 int로 변환"""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


# ============================================
# Exchange Configuration
# ============================================
EXCHANGE_CONFIG = {
    'name': os.getenv('EXCHANGE_NAME', 'binance'),
    'testnet': get_env_bool('EXCHANGE_TESTNET', True),  # False로 변경 시 실제 거래 (⚠️ 주의!)
}

# ============================================
# Trading Pair Configuration
# ============================================
TRADING_CONFIG = {
#    'symbol': os.getenv('TRADING_SYMBOL', 'BTC/KRW'),  # 거래 쌍
    'symbol': os.getenv('TRADING_SYMBOL', 'XRP/KRW'),  # 거래 쌍
    'timeframe': os.getenv('TRADING_TIMEFRAME', '15m'),  # 시간 프레임 (1m, 5m, 15m, 1h, 4h, 1d)
    'update_interval': get_env_int('UPDATE_INTERVAL', 60),  # 업데이트 주기 (초)
    'initial_balance': get_env_float('INITIAL_BALANCE', 10000),  # 초기 자본 (KRW) - dry_run 모드에서만 사용
    'dry_run': get_env_bool('DRY_RUN', True),  # True: 시뮬레이션, False: 실제 거래 ⚠️
}

# ============================================
# Strategy Configuration
# ============================================
STRATEGY_CONFIG = {
    'name': os.getenv('STRATEGY_NAME', 'RSIOBVStrategy'),  # 'RSIStrategy', 'MACDStrategy', 'MovingAverageCrossStrategy', 'OBVStrategy'
    
    # RSI Strategy Parameters
    'rsi': {
        'oversold': get_env_int('RSI_OVERSOLD', 30),
        'overbought': get_env_int('RSI_OVERBOUGHT', 70),
        'rsi_period': get_env_int('RSI_PERIOD', 14)
    },
    
    # MACD Strategy Parameters
    'macd': {
        'fast_period': get_env_int('MACD_FAST_PERIOD', 12),
        'slow_period': get_env_int('MACD_SLOW_PERIOD', 26),
        'signal_period': get_env_int('MACD_SIGNAL_PERIOD', 9)
    },
    
    # MA Cross Strategy Parameters
    'ma_cross': {
        'fast_period': get_env_int('MA_FAST_PERIOD', 20),
        'slow_period': get_env_int('MA_SLOW_PERIOD', 50)
    },
    
    # OBV Strategy Parameters
    'obv': {
        'obv_ma_period': get_env_int('OBV_MA_PERIOD', 20), #  캔들 갯수의 이동평균 기간
        'divergence_lookback': get_env_int('OBV_DIVERGENCE_LOOKBACK', 5) # 다이버전스 확인용 과거 캔들 수
    },

    # RSI + OBV Strategy Parameters
    'rsi_obv': {
        'oversold': get_env_int('RSI_OVERSOLD', 30),
        'overbought': get_env_int('RSI_OVERBOUGHT', 70),
        'rsi_period': get_env_int('RSI_PERIOD', 14),
        'obv_ma_period': get_env_int('OBV_MA_PERIOD', 20),
        'obv_weight': get_env_float('OBV_WEIGHT', 0.5)
    },

    # MACD + RSI + OBV Strategy Parameters  ← 1분봉 최적화 파라미터
    # 분석 근거: docs/MACD_RSI_OBV_analysis.md
    'macd_rsi_obv': {
        'macd_fast':          get_env_int('MACD_RSI_OBV_FAST',      8),    # EMA fast (기본: 8)
        'macd_slow':          get_env_int('MACD_RSI_OBV_SLOW',     21),    # EMA slow (기본: 21)
        'macd_signal':        get_env_int('MACD_RSI_OBV_SIGNAL',    5),    # Signal EMA (기본: 5)
        'rsi_period':         get_env_int('MACD_RSI_OBV_RSI_P',     9),    # RSI 기간 (기본: 9)
        'rsi_buy_threshold':  get_env_float('MACD_RSI_OBV_BUY',  55.0),   # 매수 RSI 상한 (기본: 55)
        'rsi_sell_threshold': get_env_float('MACD_RSI_OBV_SELL', 65.0),   # 매도 RSI 기준 (기본: 65)
        'obv_ma_period':      get_env_int('MACD_RSI_OBV_OBV_MA',   10),   # OBV MA 기간 (기본: 10)
    }
}

# ============================================
# Risk Management Configuration
# ============================================
RISK_CONFIG = {
    'max_position_size': get_env_float('MAX_POSITION_SIZE', 0.1),  # 최대 포지션 크기 (전체 자본의 10%)
    'stop_loss_pct': get_env_float('STOP_LOSS_PERCENTAGE', 0.05),  # 손절매 비율 (5%)
    'take_profit_pct': get_env_float('TAKE_PROFIT_PERCENTAGE', 0.10),  # 익절 비율 (10%)
    'max_daily_loss': get_env_float('MAX_DAILY_LOSS', 0.03),  # 일일 최대 손실 (3%)
    'max_positions': get_env_int('MAX_POSITIONS', 3),  # 최대 동시 포지션 수
    'risk_reward_ratio': get_env_float('RISK_REWARD_RATIO', 2.0),  # 최소 리스크/보상 비율 (2:1)
    'trailing_stop_pct': get_env_float('TRAILING_STOP_PCT', 0.03),  # 트레일링 스탑 비율 (3%)
}

# ============================================
# Logging Configuration
# ============================================
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),  # DEBUG, INFO, WARNING, ERROR
    'file': os.getenv('LOG_FILE', 'logs/trading_bot.log'),
    'max_bytes': get_env_int('LOG_MAX_BYTES', 10 * 1024 * 1024),  # 10MB
    'backup_count': get_env_int('LOG_BACKUP_COUNT', 5),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# ============================================
# Notification Configuration (Optional)
# ============================================
NOTIFICATION_CONFIG = {
    'enabled': get_env_bool('NOTIFICATION_ENABLED', False),  # 알림 활성화 여부
    
    # Telegram
    'telegram': {
        'enabled': get_env_bool('TELEGRAM_ENABLED', False),
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
    },
    
    # Email
    'email': {
        'enabled': get_env_bool('EMAIL_ENABLED', False),
        'smtp_server': os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': get_env_int('EMAIL_SMTP_PORT', 587),
        'email_address': os.getenv('EMAIL_ADDRESS', ''),
        'email_password': os.getenv('EMAIL_PASSWORD', '')
    }
}

# ============================================
# Advanced Configuration
# ============================================
ADVANCED_CONFIG = {
    'enable_trailing_stop': get_env_bool('ENABLE_TRAILING_STOP', True),  # 트레일링 스탑 활성화
    'enable_partial_take_profit': get_env_bool('ENABLE_PARTIAL_TAKE_PROFIT', False),  # 부분 익절 (미구현)
    'partial_take_profit_pct': get_env_float('PARTIAL_TAKE_PROFIT_PCT', 0.5),  # 부분 익절 비율
    'min_order_size': get_env_float('MIN_ORDER_SIZE', 0.001),  # 최소 주문 크기 (BTC)
}
