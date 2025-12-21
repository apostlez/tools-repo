"""
Technical Indicators Module
기술적 지표 계산 모듈

주요 지표:
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Stochastic Oscillator
"""

import pandas as pd
import numpy as np
from typing import Union, Tuple


class TechnicalIndicators:
    """기술적 지표 계산 클래스"""
    
    @staticmethod
    def sma(data: pd.Series, period: int = 20) -> pd.Series:
        """
        Simple Moving Average (단순 이동평균)
        
        Args:
            data: 가격 데이터 (Series)
            period: 기간 (기본값: 20)
            
        Returns:
            SMA 값
        """
        return data.rolling(window=period).mean()
    
    @staticmethod
    def ema(data: pd.Series, period: int = 20) -> pd.Series:
        """
        Exponential Moving Average (지수 이동평균)
        
        Args:
            data: 가격 데이터 (Series)
            period: 기간 (기본값: 20)
            
        Returns:
            EMA 값
        """
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index (상대강도지수)
        
        Args:
            data: 가격 데이터 (Series)
            period: 기간 (기본값: 14)
            
        Returns:
            RSI 값 (0-100)
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def macd(data: pd.Series, 
             fast_period: int = 12, 
             slow_period: int = 26, 
             signal_period: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD (Moving Average Convergence Divergence)
        
        Args:
            data: 가격 데이터 (Series)
            fast_period: 빠른 EMA 기간 (기본값: 12)
            slow_period: 느린 EMA 기간 (기본값: 26)
            signal_period: 시그널 라인 기간 (기본값: 9)
            
        Returns:
            (MACD 라인, 시그널 라인, 히스토그램)
        """
        fast_ema = TechnicalIndicators.ema(data, fast_period)
        slow_ema = TechnicalIndicators.ema(data, slow_period)
        
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(data: pd.Series, 
                       period: int = 20, 
                       std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Bollinger Bands (볼린저 밴드)
        
        Args:
            data: 가격 데이터 (Series)
            period: 기간 (기본값: 20)
            std_dev: 표준편차 배수 (기본값: 2.0)
            
        Returns:
            (상단 밴드, 중간 밴드, 하단 밴드)
        """
        middle_band = TechnicalIndicators.sma(data, period)
        std = data.rolling(window=period).std()
        
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def stochastic_oscillator(high: pd.Series, 
                             low: pd.Series, 
                             close: pd.Series,
                             k_period: int = 14,
                             d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        Stochastic Oscillator (스토캐스틱)
        
        Args:
            high: 고가 데이터
            low: 저가 데이터
            close: 종가 데이터
            k_period: %K 기간 (기본값: 14)
            d_period: %D 기간 (기본값: 3)
            
        Returns:
            (%K, %D)
        """
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d = k.rolling(window=d_period).mean()
        
        return k, d
    
    @staticmethod
    def atr(high: pd.Series, 
            low: pd.Series, 
            close: pd.Series,
            period: int = 14) -> pd.Series:
        """
        Average True Range (평균 진폭)
        
        Args:
            high: 고가 데이터
            low: 저가 데이터
            close: 종가 데이터
            period: 기간 (기본값: 14)
            
        Returns:
            ATR 값
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        On-Balance Volume (거래량 지표)
        
        Args:
            close: 종가 데이터
            volume: 거래량 데이터
            
        Returns:
            OBV 값
        """
        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        return obv
    
    @staticmethod
    def vwap(high: pd.Series, 
             low: pd.Series, 
             close: pd.Series,
             volume: pd.Series) -> pd.Series:
        """
        Volume Weighted Average Price (거래량 가중 평균 가격)
        
        Args:
            high: 고가 데이터
            low: 저가 데이터
            close: 종가 데이터
            volume: 거래량 데이터
            
        Returns:
            VWAP 값
        """
        typical_price = (high + low + close) / 3
        vwap = (typical_price * volume).cumsum() / volume.cumsum()
        
        return vwap


def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    모든 주요 지표를 계산하여 DataFrame에 추가
    
    Args:
        df: OHLCV 데이터프레임 (컬럼: open, high, low, close, volume)
        
    Returns:
        지표가 추가된 DataFrame
    """
    indicators = TechnicalIndicators()
    
    # 이동평균
    df['sma_20'] = indicators.sma(df['close'], 20)
    df['sma_50'] = indicators.sma(df['close'], 50)
    df['sma_200'] = indicators.sma(df['close'], 200)
    df['ema_12'] = indicators.ema(df['close'], 12)
    df['ema_26'] = indicators.ema(df['close'], 26)
    
    # RSI
    df['rsi_14'] = indicators.rsi(df['close'], 14)
    
    # MACD
    macd, signal, histogram = indicators.macd(df['close'])
    df['macd'] = macd
    df['macd_signal'] = signal
    df['macd_histogram'] = histogram
    
    # Bollinger Bands
    upper, middle, lower = indicators.bollinger_bands(df['close'])
    df['bb_upper'] = upper
    df['bb_middle'] = middle
    df['bb_lower'] = lower
    
    # Stochastic
    k, d = indicators.stochastic_oscillator(df['high'], df['low'], df['close'])
    df['stoch_k'] = k
    df['stoch_d'] = d
    
    # ATR
    df['atr'] = indicators.atr(df['high'], df['low'], df['close'])
    
    # OBV
    df['obv'] = indicators.obv(df['close'], df['volume'])
    
    # VWAP
    df['vwap'] = indicators.vwap(df['high'], df['low'], df['close'], df['volume'])
    
    return df


if __name__ == "__main__":
    # 테스트 코드
    print("Technical Indicators Module")
    print("=" * 50)
    
    # 샘플 데이터 생성
    dates = pd.date_range('2024-01-01', periods=100)
    sample_data = pd.DataFrame({
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 102,
        'low': np.random.randn(100).cumsum() + 98,
        'close': np.random.randn(100).cumsum() + 100,
        'volume': np.random.randint(1000, 10000, 100)
    }, index=dates)
    
    # 지표 계산
    sample_data = calculate_all_indicators(sample_data)
    
    print("\n계산된 지표 목록:")
    print(sample_data.columns.tolist())
    
    print("\n최근 5개 데이터:")
    print(sample_data[['close', 'sma_20', 'rsi_14', 'macd']].tail())
    
    print("\n✅ 지표 계산 모듈 정상 작동")
