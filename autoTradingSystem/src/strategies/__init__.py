"""
Strategies Package
"""

from .base_strategy import (
    BaseStrategy,
    Signal,
    SignalType,
    PortfolioManager
)

from .sample_strategies import (
    RSIStrategy,
    MACDStrategy,
    MovingAverageCrossStrategy
)

__all__ = [
    'BaseStrategy',
    'Signal',
    'SignalType',
    'PortfolioManager',
    'RSIStrategy',
    'MACDStrategy',
    'MovingAverageCrossStrategy'
]
