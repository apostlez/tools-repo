"""
Risk Management Module
리스크 관리 모듈

주요 기능:
- 포지션 사이즈 계산
- 손절매 (Stop Loss) 설정
- 익절 (Take Profit) 설정
- 최대 손실 한도 관리
- 포지션 수 제한
"""

from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging


class RiskManager:
    """리스크 관리 클래스"""
    
    def __init__(self, config: Dict):
        """
        Args:
            config: 리스크 관리 설정
                - max_position_size: 최대 포지션 크기 (전체 자본 대비 %)
                - stop_loss_pct: 손절매 비율 (%)
                - take_profit_pct: 익절 비율 (%)
                - max_daily_loss: 일일 최대 손실 (%)
                - max_positions: 최대 동시 포지션 수
                - risk_reward_ratio: 리스크/보상 비율 (최소)
        """
        self.max_position_size = config.get('max_position_size', 0.1)  # 10%
        self.stop_loss_pct = config.get('stop_loss_pct', 0.05)  # 5%
        self.take_profit_pct = config.get('take_profit_pct', 0.10)  # 10%
        self.max_daily_loss = config.get('max_daily_loss', 0.03)  # 3%
        self.max_positions = config.get('max_positions', 3)
        self.risk_reward_ratio = config.get('risk_reward_ratio', 2.0)  # 최소 2:1
        
        # 일일 손실 추적
        self.daily_loss_tracker: Dict[str, float] = {}  # date -> total_loss
        self.daily_reset_date = datetime.now().date()
        
        self.logger = logging.getLogger(__name__)
    
    def calculate_position_size(self, 
                                balance: float, 
                                entry_price: float,
                                signal_strength: float = 1.0) -> float:
        """
        포지션 사이즈 계산
        
        Args:
            balance: 사용 가능한 잔액
            entry_price: 진입 가격
            signal_strength: 시그널 강도 (0.0 ~ 1.0)
            
        Returns:
            매수할 수량
        """
        # 기본 포지션 크기 (전체 자본의 일정 %)
        position_value = balance * self.max_position_size
        
        # 시그널 강도에 따라 조정 (강도가 낮으면 포지션 크기 감소)
        position_value *= signal_strength
        
        # 수량 계산
        amount = position_value / entry_price
        
        self.logger.info(
            f"Position size calculated: ${position_value:.2f} = {amount:.6f} units "
            f"(balance: ${balance:.2f}, strength: {signal_strength:.2f})"
        )
        
        return amount
    
    def calculate_stop_loss(self, entry_price: float, is_long: bool = True) -> float:
        """
        손절매 가격 계산
        
        Args:
            entry_price: 진입 가격
            is_long: 롱 포지션 여부 (False면 숏)
            
        Returns:
            손절매 가격
        """
        if is_long:
            # 롱 포지션: 진입가보다 낮은 가격
            stop_loss = entry_price * (1 - self.stop_loss_pct)
        else:
            # 숏 포지션: 진입가보다 높은 가격
            stop_loss = entry_price * (1 + self.stop_loss_pct)
        
        self.logger.info(
            f"Stop loss calculated: ${stop_loss:.2f} "
            f"({'LONG' if is_long else 'SHORT'}, entry: ${entry_price:.2f}, "
            f"{self.stop_loss_pct*100:.1f}%)"
        )
        
        return stop_loss
    
    def calculate_take_profit(self, entry_price: float, is_long: bool = True) -> float:
        """
        익절 가격 계산
        
        Args:
            entry_price: 진입 가격
            is_long: 롱 포지션 여부
            
        Returns:
            익절 가격
        """
        if is_long:
            # 롱 포지션: 진입가보다 높은 가격
            take_profit = entry_price * (1 + self.take_profit_pct)
        else:
            # 숏 포지션: 진입가보다 낮은 가격
            take_profit = entry_price * (1 - self.take_profit_pct)
        
        self.logger.info(
            f"Take profit calculated: ${take_profit:.2f} "
            f"({'LONG' if is_long else 'SHORT'}, entry: ${entry_price:.2f}, "
            f"{self.take_profit_pct*100:.1f}%)"
        )
        
        return take_profit
    
    def should_stop_loss(self, entry_price: float, current_price: float, is_long: bool = True) -> bool:
        """
        손절매 실행 여부 확인
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
            is_long: 롱 포지션 여부
            
        Returns:
            손절매 실행 여부
        """
        stop_loss_price = self.calculate_stop_loss(entry_price, is_long)
        
        if is_long:
            should_stop = current_price <= stop_loss_price
        else:
            should_stop = current_price >= stop_loss_price
        
        if should_stop:
            loss_pct = abs((current_price - entry_price) / entry_price * 100)
            self.logger.warning(
                f"⛔ Stop loss triggered! "
                f"Entry: ${entry_price:.2f}, Current: ${current_price:.2f}, "
                f"Loss: {loss_pct:.2f}%"
            )
        
        return should_stop
    
    def should_take_profit(self, entry_price: float, current_price: float, is_long: bool = True) -> bool:
        """
        익절 실행 여부 확인
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
            is_long: 롱 포지션 여부
            
        Returns:
            익절 실행 여부
        """
        take_profit_price = self.calculate_take_profit(entry_price, is_long)
        
        if is_long:
            should_take = current_price >= take_profit_price
        else:
            should_take = current_price <= take_profit_price
        
        if should_take:
            profit_pct = abs((current_price - entry_price) / entry_price * 100)
            self.logger.info(
                f"✅ Take profit triggered! "
                f"Entry: ${entry_price:.2f}, Current: ${current_price:.2f}, "
                f"Profit: {profit_pct:.2f}%"
            )
        
        return should_take
    
    def can_open_position(self, current_positions: int, daily_loss: float) -> Tuple[bool, str]:
        """
        새 포지션 오픈 가능 여부 확인
        
        Args:
            current_positions: 현재 보유 포지션 수
            daily_loss: 오늘 누적 손실 (%)
            
        Returns:
            (가능 여부, 이유)
        """
        # 일일 리셋 확인
        self._reset_daily_tracker()
        
        # 최대 포지션 수 확인
        if current_positions >= self.max_positions:
            return False, f"Max positions reached ({current_positions}/{self.max_positions})"
        
        # 일일 최대 손실 확인
        if daily_loss >= self.max_daily_loss:
            return False, f"Daily loss limit reached ({daily_loss*100:.2f}% >= {self.max_daily_loss*100:.2f}%)"
        
        return True, "OK"
    
    def record_trade(self, profit: float, entry_balance: float):
        """
        거래 기록 (일일 손실 추적)
        
        Args:
            profit: 거래 손익 ($)
            entry_balance: 거래 시작 시 잔액
        """
        self._reset_daily_tracker()
        
        today = str(datetime.now().date())
        
        if today not in self.daily_loss_tracker:
            self.daily_loss_tracker[today] = 0.0
        
        # 손실인 경우만 기록 (수익은 제한하지 않음)
        if profit < 0:
            loss_pct = abs(profit) / entry_balance
            self.daily_loss_tracker[today] += loss_pct
            
            self.logger.info(
                f"Trade recorded: Loss {loss_pct*100:.2f}%, "
                f"Daily total: {self.daily_loss_tracker[today]*100:.2f}%"
            )
    
    def get_daily_loss(self) -> float:
        """
        오늘의 누적 손실률 조회
        
        Returns:
            누적 손실률 (0.0 ~ 1.0)
        """
        self._reset_daily_tracker()
        today = str(datetime.now().date())
        return self.daily_loss_tracker.get(today, 0.0)
    
    def _reset_daily_tracker(self):
        """일일 손실 추적기 리셋 (자정 지나면)"""
        current_date = datetime.now().date()
        
        if current_date != self.daily_reset_date:
            self.logger.info("Daily loss tracker reset")
            self.daily_loss_tracker.clear()
            self.daily_reset_date = current_date
    
    def validate_risk_reward(self, entry_price: float, 
                            stop_loss: float, 
                            take_profit: float) -> Tuple[bool, float]:
        """
        리스크/보상 비율 검증
        
        Args:
            entry_price: 진입 가격
            stop_loss: 손절매 가격
            take_profit: 익절 가격
            
        Returns:
            (유효 여부, 실제 비율)
        """
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        
        if risk == 0:
            return False, 0.0
        
        ratio = reward / risk
        is_valid = ratio >= self.risk_reward_ratio
        
        if not is_valid:
            self.logger.warning(
                f"Risk/Reward ratio too low: {ratio:.2f} < {self.risk_reward_ratio:.2f}"
            )
        
        return is_valid, ratio
    
    def get_trailing_stop_loss(self, 
                               entry_price: float,
                               highest_price: float,
                               is_long: bool = True,
                               trailing_pct: float = 0.03) -> float:
        """
        트레일링 스탑 계산
        
        Args:
            entry_price: 진입 가격
            highest_price: 최고가 (롱) 또는 최저가 (숏)
            is_long: 롱 포지션 여부
            trailing_pct: 트레일링 비율 (기본 3%)
            
        Returns:
            트레일링 스탑 가격
        """
        if is_long:
            # 롱: 최고가에서 일정 % 하락 시 매도
            trailing_stop = highest_price * (1 - trailing_pct)
            # 기본 손절매보다 높으면 사용
            regular_stop = self.calculate_stop_loss(entry_price, is_long)
            return max(trailing_stop, regular_stop)
        else:
            # 숏: 최저가에서 일정 % 상승 시 매수
            trailing_stop = highest_price * (1 + trailing_pct)
            regular_stop = self.calculate_stop_loss(entry_price, is_long)
            return min(trailing_stop, regular_stop)
    
    def get_config(self) -> Dict:
        """현재 리스크 관리 설정 반환"""
        return {
            'max_position_size': self.max_position_size,
            'stop_loss_pct': self.stop_loss_pct,
            'take_profit_pct': self.take_profit_pct,
            'max_daily_loss': self.max_daily_loss,
            'max_positions': self.max_positions,
            'risk_reward_ratio': self.risk_reward_ratio,
            'current_daily_loss': self.get_daily_loss()
        }
    
    def __repr__(self):
        return (f"RiskManager(pos_size={self.max_position_size*100:.0f}%, "
                f"stop_loss={self.stop_loss_pct*100:.0f}%, "
                f"take_profit={self.take_profit_pct*100:.0f}%)")


# 사용 예제
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 리스크 관리자 생성
    config = {
        'max_position_size': 0.1,   # 10%
        'stop_loss_pct': 0.05,       # 5%
        'take_profit_pct': 0.10,     # 10%
        'max_daily_loss': 0.03,      # 3%
        'max_positions': 3,
        'risk_reward_ratio': 2.0
    }
    
    risk_manager = RiskManager(config)
    
    print("="*60)
    print("Risk Manager Test")
    print("="*60)
    
    # 테스트 데이터
    balance = 10000
    entry_price = 50000
    current_price = 48000
    
    # 1. 포지션 사이즈 계산
    print("\n1. Position Size Calculation")
    amount = risk_manager.calculate_position_size(balance, entry_price, signal_strength=0.8)
    print(f"   Amount to buy: {amount:.6f} units")
    
    # 2. 손절매/익절 가격
    print("\n2. Stop Loss & Take Profit")
    stop_loss = risk_manager.calculate_stop_loss(entry_price)
    take_profit = risk_manager.calculate_take_profit(entry_price)
    print(f"   Entry: ${entry_price:,.2f}")
    print(f"   Stop Loss: ${stop_loss:,.2f}")
    print(f"   Take Profit: ${take_profit:,.2f}")
    
    # 3. 리스크/보상 비율
    print("\n3. Risk/Reward Validation")
    is_valid, ratio = risk_manager.validate_risk_reward(entry_price, stop_loss, take_profit)
    print(f"   Ratio: {ratio:.2f}")
    print(f"   Valid: {is_valid}")
    
    # 4. 손절매 체크
    print("\n4. Stop Loss Check")
    should_stop = risk_manager.should_stop_loss(entry_price, current_price)
    print(f"   Should stop: {should_stop}")
    
    # 5. 포지션 오픈 가능 여부
    print("\n5. Can Open Position")
    can_open, reason = risk_manager.can_open_position(2, 0.01)
    print(f"   Can open: {can_open}")
    print(f"   Reason: {reason}")
    
    print("\n" + "="*60)
    print("✅ Risk Manager working correctly")
