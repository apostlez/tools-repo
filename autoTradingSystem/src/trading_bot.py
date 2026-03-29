"""
Auto Trading Bot
실시간 자동 매매 봇

주요 기능:
- 실시간 시장 데이터 모니터링
- 전략 기반 자동 매매 시그널 생성
- 리스크 관리 적용
- 자동 주문 실행
- 포지션 모니터링 및 관리
"""

import ccxt
import pandas as pd
import time
import logging
from datetime import datetime
from typing import Dict, Optional, List
from dotenv import load_dotenv
import os
import sys

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.indicators import calculate_all_indicators
from src.strategies import BaseStrategy, SignalType
from src.risk_manager import RiskManager


class TradingBot:
    """자동 매매 봇 클래스"""
    
    def __init__(self, 
                 exchange: ccxt.Exchange,
                 strategy: BaseStrategy,
                 risk_manager: RiskManager,
                 config: Dict):
        """
        Args:
            exchange: 거래소 객체 (ccxt)
            strategy: 매매 전략
            risk_manager: 리스크 관리자
            config: 봇 설정
                - symbol: 거래 심볼
                - timeframe: 시간 프레임
                - update_interval: 업데이트 주기 (초)
                - initial_balance: 초기 자본
                - dry_run: 시뮬레이션 모드 (실제 주문 안함)
        """
        self.exchange = exchange
        self.strategy = strategy
        self.risk_manager = risk_manager
        
        self.symbol = config['symbol']
        self.timeframe = config['timeframe']
        self.update_interval = config.get('update_interval', 60)
        self.initial_balance = config.get('initial_balance', 10000)
        self.dry_run = config.get('dry_run', True)
        self.quote_currency = self.symbol.split('/')[1]  # 'XRP/KRW' → 'KRW'
        
        # 상태 관리
        self.is_running = False
        self.positions: Dict = {}  # symbol -> position info
        self.balance = self.initial_balance
        self.trade_history: List[Dict] = []
        
        # 로거 설정
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"TradingBot initialized: {self.symbol} ({self.timeframe})")
        self.logger.info(f"Strategy: {self.strategy.name}")
        self.logger.info(f"Dry run: {self.dry_run}")
    
    def fetch_ohlcv(self, limit: int = 200) -> pd.DataFrame:
        """
        OHLCV 데이터 가져오기
        
        Args:
            limit: 데이터 개수
            
        Returns:
            OHLCV DataFrame
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to fetch OHLCV: {e}")
            raise
    
    def get_balance(self) -> float:
        """
        현재 잔액 조회
        
        Returns:
            사용 가능한 Quote 통화 잔액 (예: KRW, USDT)
        """
        if self.dry_run:
            return self.balance
        
        try:
            quote_currency = self.symbol.split('/')[1]  # 'XRP/KRW' → 'KRW'
            balance = self.exchange.fetch_balance()
            return balance['free'].get(quote_currency, 0.0)
        except Exception as e:
            self.logger.error(f"Failed to fetch balance: {e}")
            return 0.0
    
    def has_position(self, symbol: str) -> bool:
        """포지션 보유 여부 확인"""
        return symbol in self.positions and self.positions[symbol] is not None
    
    def open_position(self, signal, current_price: float):
        """
        포지션 오픈 (매수)
        
        Args:
            signal: 거래 시그널
            current_price: 현재 가격
        """
        # 리스크 체크
        can_open, reason = self.risk_manager.can_open_position(
            len(self.positions),
            self.risk_manager.get_daily_loss()
        )
        
        if not can_open:
            self.logger.warning(f"Cannot open position: {reason}")
            return
        
        # 포지션 사이즈 계산
        balance = self.get_balance()
        amount = self.risk_manager.calculate_position_size(
            balance, 
            current_price,
            signal.strength
        )
        
        # 손절매/익절 가격 계산
        stop_loss = self.risk_manager.calculate_stop_loss(current_price)
        take_profit = self.risk_manager.calculate_take_profit(current_price)
        
        # 리스크/보상 비율 검증
        is_valid, rr_ratio = self.risk_manager.validate_risk_reward(
            current_price, stop_loss, take_profit
        )
        
        if not is_valid:
            self.logger.warning(f"Risk/Reward ratio too low: {rr_ratio:.2f}")
            return
        
        # 주문 실행
        if not self.dry_run:
            try:
                order = self.exchange.create_market_buy_order(self.symbol, amount)
                self.logger.info(f"✅ BUY order executed: {order}")
            except Exception as e:
                self.logger.error(f"❌ Failed to execute BUY order: {e}")
                return
        else:
            self.logger.info(f"🔵 [DRY RUN] BUY {amount:.6f} {self.symbol} @ {current_price:,.2f} {self.quote_currency}")
        
        # 포지션 정보 저장
        cost = amount * current_price
        self.positions[self.symbol] = {
            'entry_price': current_price,
            'amount': amount,
            'cost': cost,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'highest_price': current_price,  # 트레일링 스탑용
            'entry_time': datetime.now(),
            'signal_reason': signal.reason
        }
        
        # 잔액 업데이트 (드라이런)
        if self.dry_run:
            self.balance -= cost
        
        # 거래 기록
        self.trade_history.append({
            'type': 'BUY',
            'symbol': self.symbol,
            'price': current_price,
            'amount': amount,
            'cost': cost,
            'timestamp': datetime.now(),
            'reason': signal.reason
        })
        
        self.logger.info(
            f"🟢 Position opened: {amount:.6f} {self.symbol} @ {current_price:,.2f} {self.quote_currency}\n"
            f"   Stop Loss: {stop_loss:,.2f} {self.quote_currency}, Take Profit: {take_profit:,.2f} {self.quote_currency}\n"
            f"   Balance: {self.get_balance():,.2f} {self.quote_currency}"
        )
    
    def close_position(self, symbol: str, current_price: float, reason: str = "Signal"):
        """
        포지션 종료 (매도)
        
        Args:
            symbol: 거래 심볼
            current_price: 현재 가격
            reason: 종료 이유
        """
        if not self.has_position(symbol):
            self.logger.warning(f"No position to close for {symbol}")
            return
        
        position = self.positions[symbol]
        amount = position['amount']
        entry_price = position['entry_price']
        
        # 주문 실행
        if not self.dry_run:
            try:
                order = self.exchange.create_market_sell_order(symbol, amount)
                self.logger.info(f"✅ SELL order executed: {order}")
            except Exception as e:
                self.logger.error(f"❌ Failed to execute SELL order: {e}")
                return
        else:
            self.logger.info(f"🔵 [DRY RUN] SELL {amount:.6f} {symbol} @ {current_price:,.2f} {self.quote_currency}")
        
        # 손익 계산
        revenue = amount * current_price
        profit = revenue - position['cost']
        profit_pct = (profit / position['cost']) * 100
        
        # 잔액 업데이트 (드라이런)
        if self.dry_run:
            self.balance += revenue
        
        # 거래 기록
        self.trade_history.append({
            'type': 'SELL',
            'symbol': symbol,
            'price': current_price,
            'amount': amount,
            'revenue': revenue,
            'profit': profit,
            'profit_pct': profit_pct,
            'timestamp': datetime.now(),
            'reason': reason,
            'holding_time': (datetime.now() - position['entry_time']).total_seconds() / 3600
        })
        
        # 리스크 관리자에 거래 기록
        self.risk_manager.record_trade(profit, position['cost'])
        
        # 포지션 제거
        del self.positions[symbol]
        
        emoji = "🟢" if profit > 0 else "🔴"
        self.logger.info(
            f"{emoji} Position closed: {amount:.6f} {symbol} @ {current_price:,.2f} {self.quote_currency}\n"
            f"   Entry: {entry_price:,.2f} {self.quote_currency}, Profit: {profit:,.2f} {self.quote_currency} ({profit_pct:+.2f}%)\n"
            f"   Reason: {reason}\n"
            f"   Balance: {self.get_balance():,.2f} {self.quote_currency}"
        )
    
    def check_position_exit(self, symbol: str, current_price: float, highest_price: float):
        """
        포지션 청산 조건 확인
        
        Args:
            symbol: 거래 심볼
            current_price: 현재 가격
            highest_price: 보유 중 최고가
        """
        if not self.has_position(symbol):
            return
        
        position = self.positions[symbol]
        entry_price = position['entry_price']
        
        # 최고가 업데이트
        if highest_price > position['highest_price']:
            position['highest_price'] = highest_price
        
        # 1. 손절매 체크
        if self.risk_manager.should_stop_loss(entry_price, current_price):
            self.close_position(symbol, current_price, "Stop Loss")
            return
        
        # 2. 익절 체크
        if self.risk_manager.should_take_profit(entry_price, current_price):
            self.close_position(symbol, current_price, "Take Profit")
            return
        
        # 3. 트레일링 스탑 체크 (옵션)
        trailing_stop = self.risk_manager.get_trailing_stop_loss(
            entry_price, 
            position['highest_price']
        )
        
        if current_price <= trailing_stop and current_price > entry_price:
            self.close_position(symbol, current_price, "Trailing Stop")
            return
    
    def run_iteration(self):
        """단일 반복 실행 (한 번의 매매 사이클)"""
        try:
            # 1. 시장 데이터 가져오기
            df = self.fetch_ohlcv()
            
            # 2. 지표 계산
            df = calculate_all_indicators(df)
            
            current_price = df['close'].iloc[-1]
            highest_price = df['high'].iloc[-1]
            
            # 3. 전략 시그널 생성
            signal = self.strategy.analyze(df, self.symbol)
            
            self.logger.info(
                f"📊 {self.symbol}: {current_price:,.2f} {self.quote_currency} | "
                f"Signal: {signal.signal_type.value} ({signal.strength:.2%}) | "
                f"{signal.reason}"
            )
            
            # 4. 포지션 청산 조건 체크 (보유 중인 경우)
            if self.has_position(self.symbol):
                self.check_position_exit(self.symbol, current_price, highest_price)
            
            # 5. 매수 시그널 처리
            if signal.signal_type == SignalType.BUY and not self.has_position(self.symbol):
                self.open_position(signal, current_price)
            
            # 6. 매도 시그널 처리
            elif signal.signal_type == SignalType.SELL and self.has_position(self.symbol):
                self.close_position(self.symbol, current_price, "Sell Signal")
            
        except Exception as e:
            self.logger.error(f"Error in run_iteration: {e}", exc_info=True)
    
    def run(self):
        """봇 실행 (무한 루프)"""
        self.is_running = True
        self.logger.info("="*70)
        self.logger.info("🚀 Trading Bot Started")
        self.logger.info("="*70)
        self.logger.info(f"Symbol: {self.symbol}")
        self.logger.info(f"Timeframe: {self.timeframe}")
        self.logger.info(f"Strategy: {self.strategy.name}")
        self.logger.info(f"Update Interval: {self.update_interval}s")
        self.logger.info(f"   Initial Balance: {self.initial_balance:,.2f} {self.quote_currency}")
        self.logger.info(f"Mode: {'DRY RUN (Simulation)' if self.dry_run else 'LIVE TRADING ⚠️'}")
        self.logger.info("="*70)
        
        iteration_count = 0
        
        try:
            while self.is_running:
                iteration_count += 1
                self.logger.info(f"\n--- Iteration #{iteration_count} [{datetime.now()}] ---")
                
                self.run_iteration()
                
                # 성과 출력 (10회마다)
                if iteration_count % 10 == 0:
                    self.print_performance()
                
                # 대기
                self.logger.info(f"Waiting {self.update_interval}s until next update...")
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            self.logger.info("\n⏸️  Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}", exc_info=True)
        finally:
            self.stop()
    
    def stop(self):
        """봇 중지"""
        self.is_running = False
        
        # 남은 포지션 정리 (옵션)
        if self.positions:
            self.logger.info("\n🔄 Closing remaining positions...")
            for symbol in list(self.positions.keys()):
                try:
                    df = self.fetch_ohlcv()
                    current_price = df['close'].iloc[-1]
                    self.close_position(symbol, current_price, "Bot Stopped")
                except Exception as e:
                    self.logger.error(f"Failed to close position {symbol}: {e}")
        
        self.logger.info("\n" + "="*70)
        self.logger.info("📊 Final Performance Report")
        self.logger.info("="*70)
        self.print_performance()
        self.logger.info("="*70)
        self.logger.info("🛑 Trading Bot Stopped")
        self.logger.info("="*70)
    
    def print_performance(self):
        """성과 출력"""
        total_trades = len([t for t in self.trade_history if t['type'] == 'SELL'])
        
        if total_trades == 0:
            self.logger.info("📊 No completed trades yet")
            self.logger.info(f"   Current Balance: {self.get_balance():,.2f} {self.quote_currency}")
            self.logger.info(f"   Open Positions: {len(self.positions)}")
            return
        
        # 통계 계산
        sell_trades = [t for t in self.trade_history if t['type'] == 'SELL']
        profits = [t['profit'] for t in sell_trades]
        winning_trades = [p for p in profits if p > 0]
        
        total_profit = sum(profits)
        win_rate = len(winning_trades) / len(profits) * 100 if profits else 0
        
        current_balance = self.get_balance()
        total_return = ((current_balance - self.initial_balance) / self.initial_balance) * 100
        
        self.logger.info(f"\n📈 Performance Summary:")
        self.logger.info(f"   Total Trades: {total_trades}")
        self.logger.info(f"   Winning: {len(winning_trades)}, Losing: {len(profits) - len(winning_trades)}")
        self.logger.info(f"   Win Rate: {win_rate:.2f}%")
        self.logger.info(f"   Total Profit: {total_profit:,.2f} {self.quote_currency}")
        self.logger.info(f"   Initial Balance: {self.initial_balance:,.2f} {self.quote_currency}")
        self.logger.info(f"   Current Balance: {current_balance:,.2f} {self.quote_currency}")
        self.logger.info(f"   Total Return: {total_return:+.2f}%")
        self.logger.info(f"   Open Positions: {len(self.positions)}")
        
        if profits:
            self.logger.info(f"   Average Profit: {sum(profits)/len(profits):,.2f} {self.quote_currency}")
            self.logger.info(f"   Best Trade: {max(profits):,.2f} {self.quote_currency}")
            self.logger.info(f"   Worst Trade: {min(profits):,.2f} {self.quote_currency}")
