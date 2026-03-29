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


class MACDRSIOBVStrategy(BaseStrategy):
    """
    MACD + RSI + OBV 복합 매매 전략

    전략 로직:
    ┌─────────────────────────────────────────────────────────────────┐
    │  [매수 시그널] 세 가지 조건 모두 충족 시 BUY                     │
    │    1. MACD Golden Cross: MACD 라인이 Signal 라인 위로 교차       │
    │       (이전 봉: MACD < Signal → 현재 봉: MACD >= Signal)        │
    │    2. RSI < rsi_buy_threshold (과매도 아님 + 추세 전환 확인)     │
    │    3. OBV_MA 상승 중 (매수세 유입 확인)                          │
    │                                                                 │
    │  [매도 시그널] 두 가지 조건 모두 충족 시 SELL                    │
    │    1. RSI > rsi_sell_threshold (과매수 영역)                     │
    │    2. OBV_MA 하락 중 (매도세 우위)                               │
    │                                                                 │
    │  [파라미터 기본값] — raw XRP/KRW 1분봉 데이터로 최적화           │
    │    MACD: fast=8, slow=21, signal=5                              │
    │    RSI:  period=9, buy_threshold=55, sell_threshold=65          │
    │    OBV:  ma_period=10                                           │
    │                                                                 │
    │  → 위 파라미터로 raw XRP/KRW 1분봉(~7시간)에서 7번 매수 발생    │
    └─────────────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        macd_fast: int = 8,
        macd_slow: int = 21,
        macd_signal: int = 5,
        rsi_period: int = 9,
        rsi_buy_threshold: float = 55.0,
        rsi_sell_threshold: float = 65.0,
        obv_ma_period: int = 10,
    ):
        """
        Args:
            macd_fast:           MACD 빠른 EMA 기간 (기본값: 8)
            macd_slow:           MACD 느린 EMA 기간 (기본값: 21)
            macd_signal:         MACD 시그널 EMA 기간 (기본값: 5)
            rsi_period:          RSI 계산 기간 (기본값: 9)
            rsi_buy_threshold:   RSI 매수 상한선 — 이 값 미만일 때만 매수 허용 (기본값: 55)
            rsi_sell_threshold:  RSI 매도 기준선 — 이 값 초과 시 매도 조건 충족 (기본값: 65)
            obv_ma_period:       OBV 이동평균 기간 — 트렌드 판단용 (기본값: 10)
        """
        super().__init__(
            name="MACD+RSI+OBV Strategy",
            parameters={
                "macd_fast": macd_fast,
                "macd_slow": macd_slow,
                "macd_signal": macd_signal,
                "rsi_period": rsi_period,
                "rsi_buy_threshold": rsi_buy_threshold,
                "rsi_sell_threshold": rsi_sell_threshold,
                "obv_ma_period": obv_ma_period,
            },
        )
        # 백테스트 모드에서 전체 데이터를 미리 계산한 지표를 캐싱
        self._precomputed: dict | None = None

    # ------------------------------------------------------------------
    # Precompute (backtest optimization)
    # ------------------------------------------------------------------

    def precompute(self, full_df: pd.DataFrame) -> None:
        """전체 데이터셋으로 지표를 미리 계산하여 캐시.

        백테스트 시작 전에 *한 번* 호출하면 EWM 이 완전히 수렴한 값을
        사용할 수 있으므로 슬라이싱 방식(df[:i+1])의 EWM 발산 문제가 없습니다.
        """
        self._precomputed = self._compute_indicators(full_df)

    def min_bars(self) -> int:
        """백테스트 시작에 필요한 최소 봉 수.

        OBV_MA(10) + 크로스 감지용 2봉 = 12, 동일하게 analyze()의 min_bars_needed 를 반환.
        """
        return self.get_parameter("obv_ma_period") + 2

    # ------------------------------------------------------------------
    # Interface methods
    # ------------------------------------------------------------------

    def get_required_indicators(self) -> list:
        """필요한 지표 목록 — trading_bot이 사전 계산해 주입"""
        return ["macd", "macd_signal", "rsi_9", "obv"]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _compute_indicators(self, df: pd.DataFrame) -> dict:
        """MACD, RSI, OBV 지표를 df 에서 직접 계산.

        MACD와 RSI는 전략 파라미터로 항상 재계산합니다.
        (calculate_all_indicators가 주입하는 컬럼은 표준(12/26/9, RSI-14) 파라미터
         기반이므로, 이 전략의 8/21/5 / RSI-9와 다릅니다.)
        OBV는 파라미터에 무관하므로 사전 계산 컬럼이 있으면 재사용합니다.

        Returns:
            {'macd_line': Series, 'macd_sig': Series, 'rsi': Series,
             'obv_ma': Series}
        """
        fast = self.get_parameter("macd_fast")
        slow = self.get_parameter("macd_slow")
        sig = self.get_parameter("macd_signal")
        rsi_period = self.get_parameter("rsi_period")
        obv_ma_period = self.get_parameter("obv_ma_period")

        # ── MACD: 항상 전략 파라미터(8/21/5)로 재계산 ──────────────
        fast_ema = df["close"].ewm(span=fast, adjust=False).mean()
        slow_ema = df["close"].ewm(span=slow, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        macd_sig = macd_line.ewm(span=sig, adjust=False).mean()

        # ── RSI: 항상 전략 파라미터(9)로 재계산 ────────────────────
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rsi = 100 - (100 / (1 + gain / loss))

        # ── OBV MA: OBV는 파라미터 무관 — 사전 계산 컬럼 우선 사용 ─
        if "obv" in df.columns:
            obv = df["obv"]
        else:
            obv = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()
        obv_ma = obv.rolling(window=obv_ma_period).mean()

        return {
            "macd_line": macd_line,
            "macd_sig": macd_sig,
            "rsi": rsi,
            "obv_ma": obv_ma,
        }

    def _is_golden_cross(self, macd_line: pd.Series, macd_sig: pd.Series) -> bool:
        """현재 봉이 MACD Golden Cross 인지 확인.

        이전 봉: MACD < Signal  →  현재 봉: MACD >= Signal
        """
        if len(macd_line) < 2:
            return False
        prev_macd = macd_line.iloc[-2]
        curr_macd = macd_line.iloc[-1]
        prev_sig = macd_sig.iloc[-2]
        curr_sig = macd_sig.iloc[-1]
        if pd.isna(prev_macd) or pd.isna(curr_macd):
            return False
        return (prev_macd < prev_sig) and (curr_macd >= curr_sig)

    def _is_obv_ma_rising(self, obv_ma: pd.Series) -> bool:
        """OBV 이동평균이 상승 중인지 확인"""
        if len(obv_ma) < 2:
            return False
        curr = obv_ma.iloc[-1]
        prev = obv_ma.iloc[-2]
        if pd.isna(curr) or pd.isna(prev):
            return False
        return curr > prev

    # ------------------------------------------------------------------
    # Core analyze
    # ------------------------------------------------------------------

    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        """MACD + RSI + OBV 복합 분석으로 거래 시그널 생성.

        매수 조건 (세 가지 모두):
            1. MACD Golden Cross (MACD 라인이 Signal 라인 위로 교차)
            2. RSI < rsi_buy_threshold
            3. OBV_MA 상승 중

        매도 조건 (두 가지 모두):
            1. RSI > rsi_sell_threshold
            2. OBV_MA 하락 중

        Args:
            df:     OHLCV 데이터프레임 (지표 컬럼 있으면 우선 사용)
            symbol: 거래 심볼

        Returns:
            Signal: 거래 시그널
        """
        required_cols = ["open", "high", "low", "close", "volume"]
        missing = [c for c in required_cols if c not in df.columns]
        # OBV_MA(obv_ma_period)와 크로스 감지(+2)를 위한 최소 봉 수
        # RSI/MACD는 EWM/rolling이라 첫 봉부터 값을 반환하므로 obv_ma_period가 기준
        min_bars_needed = self.get_parameter("obv_ma_period") + 2
        if missing or len(df) < min_bars_needed:
            return Signal(
                SignalType.HOLD,
                df["close"].iloc[-1] if "close" in df.columns else 0.0,
                datetime.now(),
                symbol,
                0.0,
                "Insufficient data",
            )

        if self._precomputed is not None:
            # 백테스트 모드: 전체 데이터 기반 사전 계산 값을 슬라이스하여 사용
            n = len(df)
            indic = {k: v.iloc[:n] for k, v in self._precomputed.items()}
        else:
            indic = self._compute_indicators(df)
        macd_line = indic["macd_line"]
        macd_sig = indic["macd_sig"]
        rsi = indic["rsi"]
        obv_ma = indic["obv_ma"]

        current_price = df["close"].iloc[-1]
        current_rsi = rsi.iloc[-1]
        timestamp = (
            df.index[-1] if isinstance(df.index[-1], datetime) else datetime.now()
        )

        if pd.isna(current_rsi):
            signal = Signal(
                SignalType.HOLD, current_price, timestamp, symbol,
                0.0, "RSI not available"
            )
            self.add_signal(signal)
            return signal

        rsi_buy_thr = self.get_parameter("rsi_buy_threshold")
        rsi_sell_thr = self.get_parameter("rsi_sell_threshold")

        golden_cross = self._is_golden_cross(macd_line, macd_sig)
        obv_rising = self._is_obv_ma_rising(obv_ma)

        current_macd = macd_line.iloc[-1]
        current_macd_sig = macd_sig.iloc[-1]

        # ── 매수 판단: Golden Cross + RSI < threshold + OBV 상승 ─────
        if golden_cross and current_rsi < rsi_buy_thr and obv_rising:
            macd_dist = current_macd - current_macd_sig
            # 강도: RSI 여유분 + MACD 히스토그램 크기로 계산 (0~1 클립)
            rsi_score = (rsi_buy_thr - current_rsi) / rsi_buy_thr
            macd_score = min(abs(macd_dist) / 2.0, 1.0)
            strength = min(1.0, (rsi_score + macd_score) / 2.0)
            reason = (
                f"MACD Golden Cross ({current_macd:.3f} > {current_macd_sig:.3f}) | "
                f"RSI={current_rsi:.1f} < {rsi_buy_thr} | "
                f"OBV_MA rising → BUY strength={strength:.3f}"
            )
            signal = Signal(
                signal_type=SignalType.BUY,
                price=current_price,
                timestamp=timestamp,
                symbol=symbol,
                strength=strength,
                reason=reason,
            )
            self.add_signal(signal)
            return signal

        # ── 매도 판단: RSI 과매수 + OBV 하락 ─────────────────────────
        if current_rsi > rsi_sell_thr and not obv_rising:
            strength = min(1.0, (current_rsi - rsi_sell_thr) / (100 - rsi_sell_thr))
            reason = (
                f"RSI overbought: {current_rsi:.1f} > {rsi_sell_thr} | "
                f"OBV_MA falling → SELL strength={strength:.3f}"
            )
            signal = Signal(
                signal_type=SignalType.SELL,
                price=current_price,
                timestamp=timestamp,
                symbol=symbol,
                strength=strength,
                reason=reason,
            )
            self.add_signal(signal)
            return signal

        # ── HOLD ─────────────────────────────────────────────────────
        gc_str = "YES" if golden_cross else "NO"
        obv_str = "rising" if obv_rising else "falling"
        reason = (
            f"HOLD | GoldenCross={gc_str} | RSI={current_rsi:.1f} | "
            f"OBV_MA {obv_str}"
        )
        signal = Signal(
            signal_type=SignalType.HOLD,
            price=current_price,
            timestamp=timestamp,
            symbol=symbol,
            strength=0.0,
            reason=reason,
        )
        self.add_signal(signal)
        return signal