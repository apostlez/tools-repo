"""
Custom Strategy: RSI + OBV
RSI 기본 시그널에 OBV 방향성으로 강도 가중치를 적용하는 복합 전략
"""

import pandas as pd
import numpy as np
from datetime import datetime

from .base_strategy import BaseStrategy, Signal, SignalType


class RSIOBVStrategy(BaseStrategy):
    """
    RSI + OBV 복합 매매 전략

    전략 로직:
    ┌─────────────────────────────────────────────────────────────────┐
    │  1단계: RSI 기본 시그널 판단                                     │
    │     RSI < oversold  →  매수 시그널 (기본 강도 계산)              │
    │     RSI > overbought →  매도 시그널 (기본 강도 계산)             │
    │     그 외           →  HOLD                                     │
    │                                                                 │
    │  2단계: OBV 트렌드로 강도 가중치 계산                            │
    │     OBV 이동평균 변화율 → tanh 정규화 → obv_factor (-1 ~ +1)    │
    │                                                                 │
    │  3단계: 가중치 적용                                              │
    │     BUY  강도 = rsi_strength × (1 + obv_weight × obv_factor)   │
    │     SELL 강도 = rsi_strength × (1 - obv_weight × obv_factor)   │
    │                                                                 │
    │  결과 해석:                                                      │
    │     BUY  + OBV 상승 → 강도 증폭  (강세 확인)                    │
    │     BUY  + OBV 하락 → 강도 감소  (신뢰도 낮은 반등)             │
    │     SELL + OBV 하락 → 강도 증폭  (약세 확인)                    │
    │     SELL + OBV 상승 → 강도 감소  (신뢰도 낮은 하락)             │
    └─────────────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        oversold: int = 30,
        overbought: int = 70,
        rsi_period: int = 14,
        obv_ma_period: int = 20,
        obv_weight: float = 0.5,
    ):
        """
        Args:
            oversold:      RSI 과매도 기준 (기본값: 30)
            overbought:    RSI 과매수 기준 (기본값: 70)
            rsi_period:    RSI 계산 기간  (기본값: 14)
            obv_ma_period: OBV 이동평균 기간 — OBV 트렌드 판단용 (기본값: 20)
            obv_weight:    OBV 가중치 최대값 (기본값: 0.5, 범위: 0.0 ~ 1.0)
                           최종 강도 = rsi_strength × (1 ± obv_weight × obv_factor)
        """
        super().__init__(
            name="RSI+OBV Strategy",
            parameters={
                "oversold": oversold,
                "overbought": overbought,
                "rsi_period": rsi_period,
                "obv_ma_period": obv_ma_period,
                "obv_weight": obv_weight,
            },
        )

    # ------------------------------------------------------------------
    # Interface methods
    # ------------------------------------------------------------------

    def get_required_indicators(self) -> list:
        """필요한 지표 목록"""
        return ["rsi_14", "obv"]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _calc_obv_factor(self, df: pd.DataFrame) -> float:
        """OBV 이동평균 기반 트렌드 팩터 계산.

        OBV 이동평균의 1봉 변화율을 tanh 로 정규화하여 -1 ~ +1 범위로 반환.
        양수: OBV 이동평균 상승 (매수 우호적)
        음수: OBV 이동평균 하락 (매도 우호적)

        Returns:
            float: -1.0 ~ +1.0
        """
        obv_ma_period = self.get_parameter("obv_ma_period")
        obv_ma = df["obv"].rolling(window=obv_ma_period).mean()

        current_obv_ma = obv_ma.iloc[-1]
        previous_obv_ma = obv_ma.iloc[-2]

        if pd.isna(current_obv_ma) or pd.isna(previous_obv_ma) or previous_obv_ma == 0:
            return 0.0

        # 변화율: 작은 변화에도 민감하게 반응하도록 10배 스케일 후 tanh 적용
        change_rate = (current_obv_ma - previous_obv_ma) / abs(previous_obv_ma)
        obv_factor = float(np.tanh(change_rate * 10))

        return obv_factor

    # ------------------------------------------------------------------
    # Core analyze
    # ------------------------------------------------------------------

    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """RSI + OBV 복합 분석으로 거래 시그널 생성.

        Args:
            df:     OHLCV + 지표 데이터 (rsi_14, obv 컬럼 필요)
            symbol: 거래 심볼

        Returns:
            Signal: 거래 시그널 (type, strength, reason 포함)
        """
        if not self.validate_data(df):
            return Signal(
                SignalType.HOLD,
                df["close"].iloc[-1],
                datetime.now(),
                symbol,
                0.0,
                "Invalid data",
            )

        current_rsi = df["rsi_14"].iloc[-1]
        current_price = df["close"].iloc[-1]
        timestamp = (
            df.index[-1]
            if isinstance(df.index[-1], datetime)
            else datetime.now()
        )

        oversold = self.get_parameter("oversold")
        overbought = self.get_parameter("overbought")
        obv_weight = self.get_parameter("obv_weight")

        # ── 1단계: RSI 기본 시그널 ──────────────────────────────────────
        if pd.isna(current_rsi):
            signal = Signal(
                SignalType.HOLD, current_price, timestamp, symbol,
                0.0, "RSI not available"
            )
            self.add_signal(signal)
            return signal

        if current_rsi < oversold:
            signal_type = SignalType.BUY
            # RSI가 낮을수록 기본 강도 증가
            rsi_strength = (oversold - current_rsi) / oversold
            rsi_reason = f"RSI oversold: {current_rsi:.2f} < {oversold}"
        elif current_rsi > overbought:
            signal_type = SignalType.SELL
            # RSI가 높을수록 기본 강도 증가
            rsi_strength = (current_rsi - overbought) / (100 - overbought)
            rsi_reason = f"RSI overbought: {current_rsi:.2f} > {overbought}"
        else:
            signal = Signal(
                SignalType.HOLD, current_price, timestamp,
                symbol, 0.0, f"RSI neutral: {current_rsi:.2f}"
            )
            self.add_signal(signal)
            return signal

        # ── 2단계: OBV 트렌드 팩터 (-1.0 ~ +1.0) ─────────────────────
        obv_factor = self._calc_obv_factor(df)

        # ── 3단계: 가중치 적용 ────────────────────────────────────────
        #  BUY:  obv_factor > 0 (OBV 상승) → 배수 > 1  (강도 증폭)
        #        obv_factor < 0 (OBV 하락) → 배수 < 1  (강도 감소)
        #  SELL: obv_factor < 0 (OBV 하락) → 배수 > 1  (강도 증폭)
        #        obv_factor > 0 (OBV 상승) → 배수 < 1  (강도 감소)
        if signal_type == SignalType.BUY:
            multiplier = 1.0 + obv_weight * obv_factor
            obv_desc = (
                "rising ↑" if obv_factor > 0.05
                else ("falling ↓" if obv_factor < -0.05 else "neutral →")
            )
        else:  # SELL
            multiplier = 1.0 - obv_weight * obv_factor
            obv_desc = (
                "falling ↓" if obv_factor < -0.05
                else ("rising ↑" if obv_factor > 0.05 else "neutral →")
            )

        final_strength = max(0.0, min(1.0, rsi_strength * multiplier))

        reason = (
            f"{rsi_reason} | OBV {obv_desc} "
            f"(factor={obv_factor:+.3f}, ×{multiplier:.3f}) "
            f"→ strength={final_strength:.3f}"
        )

        signal = Signal(
            signal_type=signal_type,
            price=current_price,
            timestamp=timestamp,
            symbol=symbol,
            strength=final_strength,
            reason=reason,
        )

        self.add_signal(signal)
        return signal
