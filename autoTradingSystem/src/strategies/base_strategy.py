"""
Trading Strategy Base Class
모든 트레이딩 전략의 베이스 클래스
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from enum import Enum
import pandas as pd
from datetime import datetime


class SignalType(Enum):
    """거래 시그널 타입"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class Signal:
    """거래 시그널 클래스"""
    
    def __init__(self, 
                 signal_type: SignalType,
                 price: float,
                 timestamp: datetime,
                 symbol: str,
                 strength: float = 1.0,
                 reason: str = ""):
        """
        Args:
            signal_type: 시그널 타입 (BUY/SELL/HOLD)
            price: 시그널 발생 가격
            timestamp: 시그널 발생 시간
            symbol: 거래 심볼
            strength: 시그널 강도 (0.0 ~ 1.0)
            reason: 시그널 발생 이유
        """
        self.signal_type = signal_type
        self.price = price
        self.timestamp = timestamp
        self.symbol = symbol
        self.strength = strength
        self.reason = reason
    
    def __repr__(self):
        return (f"Signal({self.signal_type.value} {self.symbol} @ {self.price:.2f} "
                f"[{self.timestamp}] strength={self.strength:.2f})")
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'signal_type': self.signal_type.value,
            'price': self.price,
            'timestamp': self.timestamp.isoformat(),
            'symbol': self.symbol,
            'strength': self.strength,
            'reason': self.reason
        }


class BaseStrategy(ABC):
    """트레이딩 전략 베이스 클래스"""
    
    def __init__(self, name: str, parameters: Optional[Dict] = None):
        """
        Args:
            name: 전략 이름
            parameters: 전략 파라미터
        """
        self.name = name
        self.parameters = parameters or {}
        self.signals_history: List[Signal] = []
        
    @abstractmethod
    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """
        시장 데이터를 분석하여 거래 시그널 생성
        
        Args:
            df: OHLCV 데이터프레임 (지표 포함)
            symbol: 거래 심볼
            
        Returns:
            거래 시그널
        """
        pass
    
    @abstractmethod
    def get_required_indicators(self) -> List[str]:
        """
        전략에 필요한 지표 목록 반환
        
        Returns:
            지표 이름 리스트
        """
        pass
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        데이터 유효성 검증
        
        Args:
            df: 검증할 데이터프레임
            
        Returns:
            유효하면 True
        """
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        required_indicators = self.get_required_indicators()
        
        missing_columns = []
        for col in required_columns + required_indicators:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"⚠️ Missing columns: {missing_columns}")
            return False
        
        return True
    
    def add_signal(self, signal: Signal):
        """시그널을 히스토리에 추가"""
        self.signals_history.append(signal)
    
    def get_signals_history(self, limit: Optional[int] = None) -> List[Signal]:
        """
        시그널 히스토리 조회
        
        Args:
            limit: 조회할 최대 개수
            
        Returns:
            시그널 리스트
        """
        if limit:
            return self.signals_history[-limit:]
        return self.signals_history
    
    def get_parameter(self, key: str, default=None):
        """파라미터 값 조회"""
        return self.parameters.get(key, default)
    
    def set_parameter(self, key: str, value):
        """파라미터 값 설정"""
        self.parameters[key] = value
    
    def get_info(self) -> Dict:
        """전략 정보 반환"""
        return {
            'name': self.name,
            'parameters': self.parameters,
            'required_indicators': self.get_required_indicators(),
            'total_signals': len(self.signals_history)
        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', params={self.parameters})"


class PortfolioManager:
    """포트폴리오 관리 클래스"""
    
    def __init__(self, initial_balance: float):
        """
        Args:
            initial_balance: 초기 자본
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions: Dict[str, Dict] = {}  # symbol -> position info
        self.trade_history: List[Dict] = []
    
    def get_position(self, symbol: str) -> Optional[Dict]:
        """
        특정 심볼의 포지션 조회
        
        Args:
            symbol: 거래 심볼
            
        Returns:
            포지션 정보 또는 None
        """
        return self.positions.get(symbol)
    
    def has_position(self, symbol: str) -> bool:
        """포지션 보유 여부 확인"""
        return symbol in self.positions
    
    def open_position(self, 
                     symbol: str, 
                     amount: float, 
                     price: float,
                     timestamp: datetime):
        """
        포지션 오픈
        
        Args:
            symbol: 거래 심볼
            amount: 수량
            price: 가격
            timestamp: 시간
        """
        cost = amount * price
        
        if cost > self.balance:
            raise ValueError(f"Insufficient balance: {self.balance} < {cost}")
        
        self.positions[symbol] = {
            'amount': amount,
            'entry_price': price,
            'entry_time': timestamp,
            'cost': cost
        }
        
        self.balance -= cost
        
        self.trade_history.append({
            'type': 'BUY',
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'timestamp': timestamp,
            'balance': self.balance
        })
    
    def close_position(self, symbol: str, price: float, timestamp: datetime):
        """
        포지션 종료
        
        Args:
            symbol: 거래 심볼
            price: 종료 가격
            timestamp: 시간
        """
        if symbol not in self.positions:
            raise ValueError(f"No position for {symbol}")
        
        position = self.positions[symbol]
        amount = position['amount']
        revenue = amount * price
        
        profit = revenue - position['cost']
        profit_pct = (profit / position['cost']) * 100
        
        self.balance += revenue
        
        self.trade_history.append({
            'type': 'SELL',
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'timestamp': timestamp,
            'profit': profit,
            'profit_pct': profit_pct,
            'balance': self.balance
        })
        
        del self.positions[symbol]
    
    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """
        총 자산 가치 계산
        
        Args:
            current_prices: 현재 가격 딕셔너리 {symbol: price}
            
        Returns:
            총 자산 가치
        """
        positions_value = sum(
            pos['amount'] * current_prices.get(symbol, pos['entry_price'])
            for symbol, pos in self.positions.items()
        )
        
        return self.balance + positions_value
    
    def get_performance(self) -> Dict:
        """성과 통계 반환"""
        if not self.trade_history:
            return {'total_trades': 0}
        
        trades = [t for t in self.trade_history if t['type'] == 'SELL']
        
        if not trades:
            return {'total_trades': 0, 'open_positions': len(self.positions)}
        
        profits = [t['profit'] for t in trades]
        winning_trades = [p for p in profits if p > 0]
        
        return {
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(trades) - len(winning_trades),
            'win_rate': len(winning_trades) / len(trades) * 100 if trades else 0,
            'total_profit': sum(profits),
            'average_profit': sum(profits) / len(profits),
            'best_trade': max(profits),
            'worst_trade': min(profits),
            'current_balance': self.balance,
            'initial_balance': self.initial_balance,
            'return_pct': (self.balance - self.initial_balance) / self.initial_balance * 100
        }
