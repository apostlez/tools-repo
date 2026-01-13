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


class OBVStrategy(BaseStrategy):
    """
    OBV (On-Balance Volume) 기반 매매 전략
    
    전략 로직:
    - 가격 상승 + OBV 상승 (확인된 상승 트렌드) → 매수 시그널
    - 가격 하락 + OBV 하락 (확인된 하락 트렌드) → 매도 시그널
    - OBV와 가격의 다이버전스 감지
    """
    
    def __init__(self, obv_ma_period: int = 20, divergence_lookback: int = 5):
        """
        Args:
            obv_ma_period: OBV 이동평균 기간 (기본값: 20)
            divergence_lookback: 다이버전스 감지 기간 (기본값: 5)
        """
        super().__init__(
            name="OBV Strategy",
            parameters={
                'obv_ma_period': obv_ma_period,
                'divergence_lookback': divergence_lookback
            }
        )
    
    def get_required_indicators(self):
        """필요한 지표 목록"""
        return ['obv']
    
    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """OBV 분석"""
        if not self.validate_data(df):
            return Signal(SignalType.HOLD, df['close'].iloc[-1], datetime.now(), symbol, 0.0, "Invalid data")
        
        obv_ma_period = self.get_parameter('obv_ma_period')
        divergence_lookback = self.get_parameter('divergence_lookback')
        
        # OBV 이동평균 계산
        df['obv_ma'] = df['obv'].rolling(window=obv_ma_period).mean()
        
        current_price = df['close'].iloc[-1]
        current_obv = df['obv'].iloc[-1]
        current_obv_ma = df['obv_ma'].iloc[-1]
        previous_obv_ma = df['obv_ma'].iloc[-2]
        
        # 최근 가격 및 OBV 변화 추세
        price_change = df['close'].iloc[-1] - df['close'].iloc[-divergence_lookback]
        obv_change = df['obv'].iloc[-1] - df['obv'].iloc[-divergence_lookback]
        
        # 시그널 판단
        if pd.isna(current_obv) or pd.isna(current_obv_ma):
            signal_type = SignalType.HOLD
            strength = 0.0
            reason = "OBV not available"
        elif price_change > 0 and obv_change > 0 and current_obv > current_obv_ma and current_obv_ma > previous_obv_ma:
            # 가격과 OBV 모두 상승 트렌드 - 강한 매수 시그널
            signal_type = SignalType.BUY
            obv_trend_strength = abs(current_obv - current_obv_ma) / abs(current_obv_ma) if current_obv_ma != 0 else 0
            strength = min(obv_trend_strength, 1.0)
            reason = f"Price & OBV uptrend confirmed (OBV: {current_obv:.0f}, MA: {current_obv_ma:.0f})"
        elif price_change < 0 and obv_change < 0 and current_obv < current_obv_ma and current_obv_ma < previous_obv_ma:
            # 가격과 OBV 모두 하락 트렌드 - 강한 매도 시그널
            signal_type = SignalType.SELL
            obv_trend_strength = abs(current_obv - current_obv_ma) / abs(current_obv_ma) if current_obv_ma != 0 else 0
            strength = min(obv_trend_strength, 1.0)
            reason = f"Price & OBV downtrend confirmed (OBV: {current_obv:.0f}, MA: {current_obv_ma:.0f})"
        elif price_change > 0 and obv_change < 0:
            # 약세 다이버전스: 가격 상승 but OBV 하락 - 매도 시그널
            signal_type = SignalType.SELL
            strength = 0.6
            reason = f"Bearish divergence: Price ↑ but OBV ↓ (OBV change: {obv_change:.0f})"
        elif price_change < 0 and obv_change > 0:
            # 강세 다이버전스: 가격 하락 but OBV 상승 - 매수 시그널
            signal_type = SignalType.BUY
            strength = 0.6
            reason = f"Bullish divergence: Price ↓ but OBV ↑ (OBV change: {obv_change:.0f})"
        else:
            signal_type = SignalType.HOLD
            strength = 0.0
            trend = "up" if current_obv > current_obv_ma else "down"
            reason = f"No clear signal (OBV trend: {trend}, current: {current_obv:.0f})"
        
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
