"""
Trading Configuration
트레이딩 봇 설정 파일
"""

# ============================================
# Exchange Configuration
# ============================================
EXCHANGE_CONFIG = {
    'name': 'binance',
    'testnet': True,  # False로 변경 시 실제 거래 (⚠️ 주의!)
}

# ============================================
# Trading Pair Configuration
# ============================================
TRADING_CONFIG = {
    'symbol': 'BTC/USDT',     # 거래 쌍
    'timeframe': '15m',        # 시간 프레임 (1m, 5m, 15m, 1h, 4h, 1d)
    'update_interval': 60,     # 업데이트 주기 (초)
    'initial_balance': 10000,  # 초기 자본 (USDT) - dry_run 모드에서만 사용
    'dry_run': True,           # True: 시뮬레이션, False: 실제 거래 ⚠️
}

# ============================================
# Strategy Configuration
# ============================================
STRATEGY_CONFIG = {
    'name': 'RSIStrategy',  # 'RSIStrategy', 'MACDStrategy', 'MovingAverageCrossStrategy'
    
    # RSI Strategy Parameters
    'rsi': {
        'oversold': 30,
        'overbought': 70,
        'rsi_period': 14
    },
    
    # MACD Strategy Parameters
    'macd': {
        'fast_period': 12,
        'slow_period': 26,
        'signal_period': 9
    },
    
    # MA Cross Strategy Parameters
    'ma_cross': {
        'fast_period': 20,
        'slow_period': 50
    }
}

# ============================================
# Risk Management Configuration
# ============================================
RISK_CONFIG = {
    'max_position_size': 0.1,    # 최대 포지션 크기 (전체 자본의 10%)
    'stop_loss_pct': 0.05,        # 손절매 비율 (5%)
    'take_profit_pct': 0.10,      # 익절 비율 (10%)
    'max_daily_loss': 0.03,       # 일일 최대 손실 (3%)
    'max_positions': 3,           # 최대 동시 포지션 수
    'risk_reward_ratio': 2.0,     # 최소 리스크/보상 비율 (2:1)
    'trailing_stop_pct': 0.03,    # 트레일링 스탑 비율 (3%)
}

# ============================================
# Logging Configuration
# ============================================
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'file': 'logs/trading_bot.log',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# ============================================
# Notification Configuration (Optional)
# ============================================
NOTIFICATION_CONFIG = {
    'enabled': False,  # 알림 활성화 여부
    
    # Telegram
    'telegram': {
        'enabled': False,
        'bot_token': '',
        'chat_id': ''
    },
    
    # Email
    'email': {
        'enabled': False,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email_address': '',
        'email_password': ''
    }
}

# ============================================
# Advanced Configuration
# ============================================
ADVANCED_CONFIG = {
    'enable_trailing_stop': True,   # 트레일링 스탑 활성화
    'enable_partial_take_profit': False,  # 부분 익절 (미구현)
    'partial_take_profit_pct': 0.5,  # 부분 익절 비율
    'min_order_size': 0.001,  # 최소 주문 크기 (BTC)
}
