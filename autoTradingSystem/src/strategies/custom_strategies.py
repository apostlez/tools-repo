"""
Custom Strategies
- RSIOBVStrategy      : RSI + OBV 복합 전략
- MACDRSIOBVStrategy  : MACD + RSI + OBV 3중 필터 전략
- BollingerScalpStrategy : 볼린저 밴드 스캘핑 전략 (횡보장 특화)
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
    │  [매수 시그널] MACD 필수 + RSI/OBV 중 1개 이상 충족             │
    │    조건 1. MACD Bullish: MACD >= Signal AND MACD 상승 중        │
    │           (단발 교차가 아닌 상승 모멘텀 지속 구간 전체 포착)     │
    │    조건 2. RSI < rsi_buy_threshold                              │
    │    조건 3. OBV_MA 상승 중                                       │
    │                                                                 │
    │    3/3 충족 → 강한 BUY  (strength = max(0.4, full))             │
    │    2/3 충족 → 약한 BUY  (strength = max(0.25, full × 0.4))     │
    │    ※ 조건 1(MACD Bullish)은 항상 필수                           │
    │                                                                 │
    │  [매도 시그널] 완화된 OR 조건                                    │
    │    강한 SELL: RSI > rsi_sell_threshold                          │
    │    약한 SELL: RSI > rsi_sell_threshold - 5 AND OBV_MA 하락      │
    │                                                                 │
    │  [파라미터 기본값]                                               │
    │    MACD: fast=8, slow=21, signal=5                              │
    │    RSI:  period=9, buy_threshold=55, sell_threshold=65          │
    │    OBV:  ma_period=10                                           │
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

    def _is_macd_bullish(self, macd_line: pd.Series, macd_sig: pd.Series) -> bool:
        """MACD 강세 구간 확인 — Golden Cross보다 넓은 지속 상태 조건.

        MACD >= Signal (위에 있음) AND MACD 값이 이전 봉 대비 상승 중.
        교차 순간(1봉)뿐 아니라 상승 모멘텀이 지속되는 동안 True를 반환합니다.
        """
        if len(macd_line) < 2:
            return False
        curr_macd = macd_line.iloc[-1]
        prev_macd = macd_line.iloc[-2]
        curr_sig  = macd_sig.iloc[-1]
        if pd.isna(curr_macd) or pd.isna(prev_macd):
            return False
        return curr_macd >= curr_sig and curr_macd > prev_macd

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
            n = len(df)
            indic = {k: v.iloc[:n] for k, v in self._precomputed.items()}
        else:
            indic = self._compute_indicators(df)
        macd_line = indic["macd_line"]
        macd_sig  = indic["macd_sig"]
        rsi       = indic["rsi"]
        obv_ma    = indic["obv_ma"]

        current_price    = df["close"].iloc[-1]
        current_rsi      = rsi.iloc[-1]
        timestamp        = df.index[-1] if isinstance(df.index[-1], datetime) else datetime.now()
        rsi_buy_thr      = self.get_parameter("rsi_buy_threshold")
        rsi_sell_thr     = self.get_parameter("rsi_sell_threshold")

        if pd.isna(current_rsi):
            signal = Signal(SignalType.HOLD, current_price, timestamp, symbol, 0.0, "RSI not available")
            self.add_signal(signal)
            return signal

        macd_bullish  = self._is_macd_bullish(macd_line, macd_sig)
        obv_rising    = self._is_obv_ma_rising(obv_ma)
        rsi_ok        = current_rsi < rsi_buy_thr

        current_macd     = macd_line.iloc[-1]
        current_macd_sig = macd_sig.iloc[-1]

        # 2/3 BUY 허용 시 RSI 하드캡: rsi_buy_threshold × 1.15 초과 시 매수 금지
        # (RSI가 이미 높은 상태에서 MACD+OBV만으로 진입하는 것을 차단)
        rsi_hard_cap = rsi_buy_thr * 1.15

        # ── 매수 조건: MACD 필수 + RSI/OBV 중 1개 이상 충족 ────────
        #  3/3: 강한 BUY  (strength floor 0.4)
        #  2/3: 약한 BUY  (strength floor 0.25, MACD 조건은 필수)
        #       단, RSI > rsi_hard_cap 이면 2/3 BUY 차단
        if macd_bullish:
            conditions_met = sum([macd_bullish, rsi_ok, obv_rising])
            # 2/3이면서 RSI 하드캡 초과 → 진입 차단
            if conditions_met == 2 and current_rsi > rsi_hard_cap:
                conditions_met = 1
            #if conditions_met >= 2:
            if conditions_met >= 3:
                macd_dist  = current_macd - current_macd_sig
                rsi_score  = max(0.0, (rsi_buy_thr - current_rsi) / rsi_buy_thr) if rsi_ok else 0.0
                macd_score = min(abs(macd_dist) / (current_price * 0.002 + 1e-9), 1.0)
                full_strength = min(1.0, (rsi_score + macd_score) / 2.0)

                if conditions_met == 3:
                    strength = max(0.4, full_strength)
                    cond_str = "3/3"
                else:
                    #strength = max(0.25, full_strength * 0.4)
                    strength = 0.0
                    cond_str = "2/3"

                skipped = []
                if not rsi_ok:
                    skipped.append(f"RSI={current_rsi:.1f}>={rsi_buy_thr}")
                if not obv_rising:
                    skipped.append("OBV_MA falling")
                skip_str = f" | skip: {', '.join(skipped)}" if skipped else ""

                reason = (
                    f"MACD Bullish ({current_macd:.3f}>={current_macd_sig:.3f}, rising) | "
                    f"RSI={current_rsi:.1f} | OBV_MA {'rising' if obv_rising else 'falling'} "
                    f"[{cond_str}]{skip_str} → BUY strength={strength:.3f}"
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

        # ── 매도 조건: RSI가 rsi_sell_thr 아래로 교차하는 순간 ──────
        #  이전 봉: RSI >= rsi_sell_thr  →  현재 봉: RSI < rsi_sell_thr
        #  (하락 교차 시점에만 발화 — 과매수 구간 이탈 확인 후 청산)
        prev_rsi = rsi.iloc[-2] if len(rsi) >= 2 else float('nan')
        rsi_cross_down = (
            not pd.isna(prev_rsi)
            and prev_rsi >= rsi_sell_thr
            and current_rsi < rsi_sell_thr
        )
        if rsi_cross_down and not macd_bullish:
            strength = min(1.0, (prev_rsi - rsi_sell_thr) / (100 - rsi_sell_thr))
            obv_rising    = self._is_obv_ma_rising(obv_ma * 2) # 매도 시 obv_ma_period 는 더 길게 관측
            reason = (
                f"RSI cross-down: {prev_rsi:.1f} → {current_rsi:.1f} (thr={rsi_sell_thr}) | "
                f"OBV_MA {'falling' if not obv_rising else 'rising'} → SELL strength={strength:.3f}"
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

        # ── HOLD ────────────────────────────────────────────────────
        obv_str = "rising" if obv_rising else "falling"
        reason  = (
            f"HOLD | MACD_Bullish={'YES' if macd_bullish else 'NO'} | "
            f"RSI={current_rsi:.1f} | OBV_MA {obv_str}"
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


class BollingerScalpStrategy(BaseStrategy):
    """
    볼린저 밴드 스캘핑 전략 — 횡보장(저변동성) 특화

    전략 로직:
    ┌─────────────────────────────────────────────────────────────────┐
    │  [매수 조건] 세 가지 모두 충족                                    │
    │    1. 현재가 < BB 하단 (밴드 하단 터치/돌파 → 과매도 구간)        │
    │    2. RSI < rsi_oversold (추가 과매도 확인)                      │
    │    3. BB 밴드폭 < bb_width_threshold (저변동성 확인)              │
    │       → 고변동성 장세(트렌드)에서는 역추세 매매 금지              │
    │                                                                 │
    │  [매도 조건] 어느 하나 충족                                       │
    │    1. 현재가 > BB 중심선(MA) (평균 회귀 완료)                     │
    │    2. RSI > rsi_overbought                                      │
    │                                                                 │
    │  [시그널 강도]                                                   │
    │    매수: (BB 하단 이탈 정도 + RSI 과매도 정도) 결합               │
    │    매도: 고정 0.8                                                │
    │                                                                 │
    │  [적합 시장 조건]                                                │
    │    - BB 밴드폭 0.05~0.3% 범위의 좁은 횡보장                      │
    │    - 1분봉 XRP/KRW 같이 빠른 평균회귀가 자주 발생하는 종목       │
    └─────────────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        bb_period: int = 20,
        bb_std_mult: float = 2.0,
        rsi_period: int = 9,
        rsi_oversold: float = 35.0,
        rsi_overbought: float = 65.0,
        bb_width_threshold: float = 0.003,
    ):
        super().__init__(
            name="BollingerScalp Strategy",
            parameters={
                "bb_period": bb_period,
                "bb_std_mult": bb_std_mult,
                "rsi_period": rsi_period,
                "rsi_oversold": rsi_oversold,
                "rsi_overbought": rsi_overbought,
                "bb_width_threshold": bb_width_threshold,
            },
        )

    def get_required_indicators(self) -> list:
        return ["bb_upper", "bb_lower", "bb_mid", "rsi_9"]

    def min_bars(self) -> int:
        return self.get_parameter("bb_period") + 2

    def _compute(self, df: pd.DataFrame) -> dict:
        period  = self.get_parameter("bb_period")
        mult    = self.get_parameter("bb_std_mult")
        rsi_p   = self.get_parameter("rsi_period")
        close   = df["close"]

        bb_ma    = close.rolling(window=period).mean()
        bb_std   = close.rolling(window=period).std()
        bb_upper = bb_ma + mult * bb_std
        bb_lower = bb_ma - mult * bb_std
        bb_width = (bb_upper - bb_lower) / bb_ma

        delta = close.diff()
        gain  = delta.where(delta > 0, 0).rolling(window=rsi_p).mean()
        loss  = (-delta.where(delta < 0, 0)).rolling(window=rsi_p).mean()
        rsi   = 100 - (100 / (1 + gain / loss))

        return {
            "bb_ma": bb_ma,
            "bb_upper": bb_upper,
            "bb_lower": bb_lower,
            "bb_width": bb_width,
            "rsi": rsi,
        }

    def analyze(self, df: pd.DataFrame, symbol: str) -> Signal:
        min_bars = self.min_bars()
        if len(df) < min_bars or "close" not in df.columns:
            return Signal(
                SignalType.HOLD,
                df["close"].iloc[-1] if "close" in df.columns else 0,
                datetime.now(), symbol, 0.0, "Insufficient data",
            )

        ind       = self._compute(df)
        price     = df["close"].iloc[-1]
        timestamp = df.index[-1] if isinstance(df.index[-1], datetime) else datetime.now()

        bb_ma    = ind["bb_ma"].iloc[-1]
        bb_upper = ind["bb_upper"].iloc[-1]
        bb_lower = ind["bb_lower"].iloc[-1]
        bb_width = ind["bb_width"].iloc[-1]
        rsi      = ind["rsi"].iloc[-1]

        if any(pd.isna(v) for v in [bb_ma, bb_upper, bb_lower, bb_width, rsi]):
            return Signal(SignalType.HOLD, price, timestamp, symbol, 0.0, "Indicator NaN")

        oversold   = self.get_parameter("rsi_oversold")
        overbought = self.get_parameter("rsi_overbought")
        width_thr  = self.get_parameter("bb_width_threshold")
        is_ranging = bb_width < width_thr

        # ── 매도: BB 중심선 복귀 또는 RSI 과매수 ──────────────────
        if price > bb_ma or rsi > overbought:
            reason = (
                f"BB mid revert: {price:,.2f} > {bb_ma:,.2f}"
                if price > bb_ma else
                f"RSI overbought: {rsi:.1f} > {overbought}"
            )
            signal = Signal(SignalType.SELL, price, timestamp, symbol, 0.8, reason)
            self.add_signal(signal)
            return signal

        # ── 매수: BB 하단 + RSI 과매도 + 횡보장 ─────────────────
        if price < bb_lower and rsi < oversold and is_ranging:
            bb_dev   = (bb_lower - price) / (bb_upper - bb_lower + 1e-9)
            rsi_dev  = (oversold - rsi) / oversold
            strength = float(np.clip(0.5 * bb_dev + 0.5 * rsi_dev, 0.1, 1.0))
            reason   = (
                f"BB lower break: {price:,.2f} < {bb_lower:,.2f} | "
                f"RSI oversold: {rsi:.1f} | BB_width={bb_width*100:.3f}%"
            )
            signal = Signal(SignalType.BUY, price, timestamp, symbol, strength, reason)
            self.add_signal(signal)
            return signal

        # ── HOLD ─────────────────────────────────────────────────
        reason = (
            f"HOLD | ranging={is_ranging} rsi={rsi:.1f} "
            f"price={price:,.2f} bb_lo={bb_lower:,.2f} bw={bb_width*100:.3f}%"
        )
        signal = Signal(SignalType.HOLD, price, timestamp, symbol, 0.0, reason)
        self.add_signal(signal)
        return signal