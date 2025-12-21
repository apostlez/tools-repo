"""
RSI Strategy Implementation
RSI 지표를 사용한 매매 전략
"""

import pandas as pd
from datetime import datetime
from .base_strategy import BaseStrategy, Signal, SignalType


class RSIStrategy(BaseStrategy):
    """
    RSI 기반 매매 전략
    
    전략 로직:
    - RSI < oversold (기본값: 30) → 매수 시그널
    - RSI > overbought (기본값: 70) → 매도 시그널
    - 그 외 → 홀드
    """
    
    def __init__(self, 
                 oversold: int = 30,
                 overbought: int = 70,
                 rsi_period: int = 14):
        """
        Args:
            oversold: 과매도 기준 (기본값: 30)
            overbought: 과매수 기준 (기본값: 70)
            rsi_period: RSI 계산 기간 (기본값: 14)
        """
        super().__init__(
            name="RSI Strategy",
            parameters={
                'oversold': oversold,
                'overbought': overbought,
                'rsi_period': rsi_period
            }
        )
    
    def get_required_indicators(self):
        """필요한 지표 목록"""
        return ['rsi_14']
    
    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """
        RSI 지표를 분석하여 거래 시그널 생성
        
        Args:
            df: OHLCV + 지표 데이터
            symbol: 거래 심볼
            
        Returns:
            거래 시그널
        """
        if not self.validate_data(df):
            return Signal(
                SignalType.HOLD,
                df['close'].iloc[-1],
                datetime.now(),
                symbol,
                0.0,
                "Invalid data"
            )
        
        # 최근 데이터
        current_rsi = df['rsi_14'].iloc[-1]
        current_price = df['close'].iloc[-1]
        
        oversold = self.get_parameter('oversold')
        overbought = self.get_parameter('overbought')
        
        # 시그널 판단
        if pd.isna(current_rsi):
            signal_type = SignalType.HOLD
            strength = 0.0
            reason = "RSI not available"
        elif current_rsi < oversold:
            signal_type = SignalType.BUY
            strength = (oversold - current_rsi) / oversold  # RSI가 낮을수록 강한 매수 시그널
            reason = f"RSI oversold: {current_rsi:.2f} < {oversold}"
        elif current_rsi > overbought:
            signal_type = SignalType.SELL
            strength = (current_rsi - overbought) / (100 - overbought)  # RSI가 높을수록 강한 매도 시그널
            reason = f"RSI overbought: {current_rsi:.2f} > {overbought}"
        else:
            signal_type = SignalType.HOLD
            strength = 0.0
            reason = f"RSI neutral: {current_rsi:.2f}"
        
        signal = Signal(
            signal_type=signal_type,
            price=current_price,
            timestamp=df.index[-1] if isinstance(df.index[-1], datetime) else datetime.now(),
            symbol=symbol,
            strength=min(strength, 1.0),  # 최대 1.0
            reason=reason
        )
        
        self.add_signal(signal)
        return signal


class MACDStrategy(BaseStrategy):
    """
    MACD 기반 매매 전략
    
    전략 로직:
    - MACD 라인이 시그널 라인을 상향 돌파 → 매수 시그널
    - MACD 라인이 시그널 라인을 하향 돌파 → 매도 시그널
    """
    
    def __init__(self):
        super().__init__(
            name="MACD Strategy",
            parameters={
                'fast_period': 12,
                'slow_period': 26,
                'signal_period': 9
            }
        )
    
    def get_required_indicators(self):
        """필요한 지표 목록"""
        return ['macd', 'macd_signal', 'macd_histogram']
    
    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """MACD 크로스오버 분석"""
        if not self.validate_data(df):
            return Signal(SignalType.HOLD, df['close'].iloc[-1], datetime.now(), symbol, 0.0, "Invalid data")
        
        # 현재와 이전 히스토그램
        current_hist = df['macd_histogram'].iloc[-1]
        previous_hist = df['macd_histogram'].iloc[-2]
        current_price = df['close'].iloc[-1]
        
        # 크로스오버 감지
        if pd.isna(current_hist) or pd.isna(previous_hist):
            signal_type = SignalType.HOLD
            strength = 0.0
            reason = "MACD not available"
        elif previous_hist < 0 and current_hist > 0:
            # 골든 크로스 (상향 돌파)
            signal_type = SignalType.BUY
            strength = min(abs(current_hist) / df['close'].iloc[-1] * 100, 1.0)
            reason = f"MACD golden cross (hist: {current_hist:.4f})"
        elif previous_hist > 0 and current_hist < 0:
            # 데드 크로스 (하향 돌파)
            signal_type = SignalType.SELL
            strength = min(abs(current_hist) / df['close'].iloc[-1] * 100, 1.0)
            reason = f"MACD dead cross (hist: {current_hist:.4f})"
        else:
            signal_type = SignalType.HOLD
            strength = 0.0
            reason = f"No crossover (hist: {current_hist:.4f})"
        
        signal = Signal(
            signal_type=signal_type,
            price=current_price,
            timestamp=df.index[-1] if isinstance(df.index[-1], datetime) else datetime.now(),
            symbol=symbol,
            strength=strength,
            reason=reason
        )
        
        self.add_signal(signal)
        return signal


class MovingAverageCrossStrategy(BaseStrategy):
    """
    이동평균선 크로스 전략
    
    전략 로직:
    - 단기 이동평균선이 장기 이동평균선을 상향 돌파 → 매수 (골든 크로스)
    - 단기 이동평균선이 장기 이동평균선을 하향 돌파 → 매도 (데드 크로스)
    """
    
    def __init__(self, fast_period: int = 20, slow_period: int = 50):
        """
        Args:
            fast_period: 단기 이동평균 기간 (기본값: 20)
            slow_period: 장기 이동평균 기간 (기본값: 50)
        """
        super().__init__(
            name="MA Cross Strategy",
            parameters={
                'fast_period': fast_period,
                'slow_period': slow_period
            }
        )
    
    def get_required_indicators(self):
        """필요한 지표 목록"""
        fast = self.get_parameter('fast_period')
        slow = self.get_parameter('slow_period')
        return [f'sma_{fast}', f'sma_{slow}']
    
    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """이동평균선 크로스오버 분석"""
        if not self.validate_data(df):
            return Signal(SignalType.HOLD, df['close'].iloc[-1], datetime.now(), symbol, 0.0, "Invalid data")
        
        fast_period = self.get_parameter('fast_period')
        slow_period = self.get_parameter('slow_period')
        
        fast_ma_col = f'sma_{fast_period}'
        slow_ma_col = f'sma_{slow_period}'
        
        current_fast = df[fast_ma_col].iloc[-1]
        current_slow = df[slow_ma_col].iloc[-1]
        previous_fast = df[fast_ma_col].iloc[-2]
        previous_slow = df[slow_ma_col].iloc[-2]
        current_price = df['close'].iloc[-1]
        
        # 크로스오버 감지
        if pd.isna(current_fast) or pd.isna(current_slow):
            signal_type = SignalType.HOLD
            strength = 0.0
            reason = "MA not available"
        elif previous_fast <= previous_slow and current_fast > current_slow:
            # 골든 크로스
            signal_type = SignalType.BUY
            strength = abs(current_fast - current_slow) / current_slow
            reason = f"Golden cross: SMA{fast_period} > SMA{slow_period}"
        elif previous_fast >= previous_slow and current_fast < current_slow:
            # 데드 크로스
            signal_type = SignalType.SELL
            strength = abs(current_fast - current_slow) / current_slow
            reason = f"Death cross: SMA{fast_period} < SMA{slow_period}"
        else:
            signal_type = SignalType.HOLD
            strength = 0.0
            diff_pct = ((current_fast - current_slow) / current_slow) * 100
            reason = f"No cross (diff: {diff_pct:.2f}%)"
        
        signal = Signal(
            signal_type=signal_type,
            price=current_price,
            timestamp=df.index[-1] if isinstance(df.index[-1], datetime) else datetime.now(),
            symbol=symbol,
            strength=min(strength, 1.0),
            reason=reason
        )
        
        self.add_signal(signal)
        return signal
