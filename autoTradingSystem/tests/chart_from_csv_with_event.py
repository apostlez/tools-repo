"""
CSV + Backtest Events 캔들스틱 차트 생성기

test_strategy.py 실행 후 생성된 JSON 의 trade_events 를
캔들스틱 차트 위에 BUY/SELL 마커로 표시합니다.

사용법:
    python chart_from_csv_with_event.py [csv_path] [json_path]

    csv_path  : 생략 시 logs/ 폴더의 최신 raw_*.csv 자동 선택
    json_path : 생략 시 logs/ 폴더의 최신 backtest_*.json 자동 선택
"""

import sys
import os
import glob
import json
import matplotlib
matplotlib.use('Agg')

# ─────────────────────────────────────────────
# 전역 설정 — 여기서만 수정하면 차트 전체에 반영됩니다
# ─────────────────────────────────────────────
RSI_PERIOD: int = 4 # 14   # RSI 계산 기간
RSI_BUY_THRESHOLD: float = 62.0   # 55→62: 매수 구간 확대
RSI_SELL_THRESHOLD: float = 80.0  # 74→80: XRP 1분봉 RSI(9)는 추세 시 80까지 자주 도달

MACD_FAST:  int = 8 # 12   # MACD 빠른 EMA 기간
MACD_SLOW:  int = 12 # 26   # MACD 느린 EMA 기간
MACD_SIGNAL: int = 3 # 9   # MACD 시그널 EMA 기간
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from datetime import datetime


# ─────────────────────────────────────────────
# 스타일 (chart_from_csv.py 와 동일)
# ─────────────────────────────────────────────
STYLE = {
    "fig_bg":      "#1a1a2e",
    "ax_bg":       "#16213e",
    "title":       "#e0e0e0",
    "label":       "#b0b0b0",
    "grid":        "#2e2e4e",
    "spine":       "#2e2e4e",
    "up":          "#26a69a",
    "down":        "#ef5350",
    "volume_up":   "#26a69a80",
    "volume_down": "#ef535080",
    "ma20":        "#ff9f43",
    "ma60":        "#54a0ff",
    "rsi":         "#a29bfe",
    "rsi_ob":      "#e17055",
    "rsi_os":      "#00cec9",
    "macd":        "#74b9ff",
    "signal":      "#fd79a8",
    "hist_pos":    "#26a69a",
    "hist_neg":    "#ef5350",
    # 이벤트 마커
    "buy_marker":  "#00e676",   # 밝은 초록
    "sell_win":    "#26a69a",   # 이익 매도: 청록
    "sell_loss":   "#ff5252",   # 손실 매도: 빨강
}


# ─────────────────────────────────────────────
# 헬퍼 함수 (chart_from_csv.py 에서 복사)
# ─────────────────────────────────────────────

def style_ax(ax, title=""):
    ax.set_facecolor(STYLE["ax_bg"])
    for spine in ax.spines.values():
        spine.set_color(STYLE["spine"])
    ax.tick_params(colors=STYLE["label"], labelsize=8)
    ax.xaxis.label.set_color(STYLE["label"])
    ax.yaxis.label.set_color(STYLE["label"])
    ax.grid(color=STYLE["grid"], linestyle="--", linewidth=0.4, alpha=0.6)
    if title:
        ax.set_title(title, color=STYLE["title"], fontsize=10, fontweight="bold", pad=6)


def calc_rsi(close: pd.Series, period: int = RSI_PERIOD) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def calc_macd(close: pd.Series, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist


def draw_candlesticks(ax, df):
    for i, row in df.iterrows():
        color = STYLE["up"] if row["close"] >= row["open"] else STYLE["down"]
        ax.plot([row["x"], row["x"]], [row["low"], row["high"]],
                color=color, linewidth=0.8, zorder=1)
        body_low  = min(row["open"], row["close"])
        body_high = max(row["open"], row["close"])
        body_height = max(body_high - body_low, 0.5)
        rect = mpatches.FancyBboxPatch(
            (row["x"] - 0.35, body_low), 0.7, body_height,
            boxstyle="square,pad=0",
            facecolor=color, edgecolor=color, linewidth=0, zorder=2
        )
        ax.add_patch(rect)


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["x"] = range(len(df))
    return df


def format_x_labels(ax, df, max_labels: int = 10):
    step = max(1, len(df) // max_labels)
    ticks = list(range(0, len(df), step))
    labels = [df.loc[i, "timestamp"].strftime("%m/%d\n%H:%M") for i in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=7, color=STYLE["label"])


# ─────────────────────────────────────────────
# 이벤트 → x 인덱스 매핑
# ─────────────────────────────────────────────

def find_x_for_ts(df: pd.DataFrame, ts_str: str) -> int:
    """이벤트 타임스탬프에서 CSV df의 가장 가까운 x 인덱스를 반환."""
    ts = pd.Timestamp(ts_str)
    diffs = (df["timestamp"] - ts).abs()
    closest_row = diffs.idxmin()
    return int(df.loc[closest_row, "x"])


def find_price_at_x(df: pd.DataFrame, x: int) -> float:
    """x 인덱스의 close 가격을 반환."""
    row = df[df["x"] == x]
    if row.empty:
        return float("nan")
    return float(row["close"].iloc[0])


# ─────────────────────────────────────────────
# 차트 생성
# ─────────────────────────────────────────────

def generate_event_chart(csv_path: str, strategy_name: str,
                         events: list, strategy_stats: dict) -> str:
    """
    BUY/SELL 이벤트가 표시된 캔들스틱 차트를 생성하고 저장합니다.

    Args:
        csv_path:       OHLCV CSV 파일 경로
        strategy_name:  전략 이름 (차트 제목 및 파일명에 사용)
        events:         trade_events 리스트
                        [{'type': 'BUY'|'SELL', 'timestamp': ..., 'price': ...,
                          'profit_pct': ...}, ...]
        strategy_stats: JSON 의 strategies[name] 딕셔너리
                        {trades, wins, losses, return_pct, profit, vs_bh}

    Returns:
        저장된 PNG 경로
    """
    # ── 데이터 로드 ───────────────────────────────────────
    df = load_csv(csv_path)
    n = len(df)

    # 심볼 / 날짜 범위
    basename      = os.path.basename(csv_path)
    symbol_raw    = basename.replace("raw_", "").replace(".csv", "")
    parts         = symbol_raw.split("_")
    symbol_label  = f"{parts[0]}/{parts[1]} ({parts[2]})" if len(parts) >= 3 else symbol_raw
    date_range    = (
        f"{df['timestamp'].iloc[0].strftime('%Y-%m-%d %H:%M')} ~ "
        f"{df['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M')}"
    )

    # ── 지표 계산 ─────────────────────────────────────────
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()
    df["rsi"]  = calc_rsi(df["close"], RSI_PERIOD)
    df["macd"], df["signal_line"], df["hist"] = calc_macd(df["close"])

    # ── 이벤트 파싱 ───────────────────────────────────────
    buy_pts  = []   # (x, price)
    sell_pts = []   # (x, price, profit_pct)
    pairs    = []   # (buy_x, buy_price, sell_x, sell_price, profit_pct)
    pending_buy = None

    for ev in events:
        x = find_x_for_ts(df, ev["timestamp"])
        price = float(ev["price"])
        if ev["type"] == "BUY":
            buy_pts.append((x, price))
            pending_buy = (x, price)
        elif ev["type"] == "SELL":
            pct = float(ev.get("profit_pct", 0.0))
            sell_pts.append((x, price, pct))
            if pending_buy is not None:
                pairs.append((pending_buy[0], pending_buy[1], x, price, pct))
                pending_buy = None

    # ── Figure 레이아웃 ───────────────────────────────────
    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor(STYLE["fig_bg"])

    gs = gridspec.GridSpec(
        4, 1, figure=fig,
        height_ratios=[5, 1.5, 1.5, 1.5],
        hspace=0.04,
        left=0.07, right=0.97,
        top=0.93, bottom=0.06,
    )

    ax_candle = fig.add_subplot(gs[0])
    ax_vol    = fig.add_subplot(gs[1], sharex=ax_candle)
    ax_rsi    = fig.add_subplot(gs[2], sharex=ax_candle)
    ax_macd   = fig.add_subplot(gs[3], sharex=ax_candle)

    title = f"{symbol_label}  |  {strategy_name}  |  {date_range}"
    style_ax(ax_candle, title)

    # ── 캔들스틱 ─────────────────────────────────────────
    draw_candlesticks(ax_candle, df)

    # 이동평균선
    if n >= 20:
        ax_candle.plot(df["x"], df["ma20"], color=STYLE["ma20"],
                       linewidth=1.0, label="MA20", zorder=3)
    if n >= 60:
        ax_candle.plot(df["x"], df["ma60"], color=STYLE["ma60"],
                       linewidth=1.0, label="MA60", zorder=3)

    ax_candle.set_xlim(-1, n)
    ax_candle.set_ylabel("Price (KRW)", color=STYLE["label"], fontsize=9)
    ax_candle.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    plt.setp(ax_candle.get_xticklabels(), visible=False)

    # 현재가 수평선
    last_close = df["close"].iloc[-1]
    ax_candle.axhline(last_close, color="#ffeaa7", linewidth=0.7,
                      linestyle="--", alpha=0.8, zorder=4)
    ax_candle.text(n - 0.5, last_close, f"  {last_close:,.0f}",
                   color="#ffeaa7", fontsize=8, va="center", ha="left", clip_on=False)

    # ── BUY/SELL 이벤트 오버레이 ─────────────────────────
    # 매수/매도 연결선 (홀딩 기간)
    for bx, bp, sx, sp, pct in pairs:
        color = STYLE["sell_win"] if pct >= 0 else STYLE["sell_loss"]
        ax_candle.plot([bx, sx], [bp, sp], "--", color=color,
                       linewidth=1.0, alpha=0.55, zorder=5)
        ax_rsi.axvspan(bx, sx, alpha=0.08, color=color, zorder=0)

    # BUY 마커 (▲ 봉 하단 아래)
    if buy_pts:
        x_arr = df["x"].values
        low_arr = df["low"].values
        price_range = df["high"].max() - df["low"].min()
        offset = price_range * 0.012

        for bx, bp in buy_pts:
            # 해당 봉의 low 아래에 마커 배치
            idx = int(bx)
            marker_y = low_arr[idx] - offset if idx < len(low_arr) else bp - offset
            ax_candle.scatter([bx], [marker_y], marker="^",
                              color=STYLE["buy_marker"], s=130, zorder=7, linewidths=0)
            ax_candle.annotate(
                f"{bp:,.0f}",
                (bx, marker_y),
                textcoords="offset points", xytext=(0, -13),
                ha="center", fontsize=7, color=STYLE["buy_marker"],
                fontweight="bold",
            )

    # SELL 마커 (▼ 봉 상단 위)
    if sell_pts:
        high_arr = df["high"].values
        price_range = df["high"].max() - df["low"].min()
        offset = price_range * 0.012

        for sx, sp, pct in sell_pts:
            idx = int(sx)
            marker_y = high_arr[idx] + offset if idx < len(high_arr) else sp + offset
            color = STYLE["sell_win"] if pct >= 0 else STYLE["sell_loss"]
            ax_candle.scatter([sx], [marker_y], marker="v",
                              color=color, s=130, zorder=7, linewidths=0)
            ax_candle.annotate(
                f"{sp:,.0f}\n{pct:+.2f}%",
                (sx, marker_y),
                textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=7, color=color,
                fontweight="bold",
            )

    # RSI 패널에도 BUY/SELL 수직선 추가
    for bx, _ in buy_pts:
        ax_rsi.axvline(bx, color=STYLE["buy_marker"], linewidth=0.8, alpha=0.6, linestyle=":")
    for sx, _, _ in sell_pts:
        ax_rsi.axvline(sx, color=STYLE["sell_loss"], linewidth=0.8, alpha=0.6, linestyle=":")

    # 레전드 (MA + 이벤트)
    legend_handles = []
    if n >= 20:
        legend_handles.append(mpatches.Patch(color=STYLE["ma20"], label="MA20"))
    if n >= 60:
        legend_handles.append(mpatches.Patch(color=STYLE["ma60"], label="MA60"))
    if buy_pts:
        legend_handles.append(plt.scatter([], [], marker="^", color=STYLE["buy_marker"],
                                          s=80, label="BUY"))
    if sell_pts:
        legend_handles.append(plt.scatter([], [], marker="v",
                                          color=STYLE["sell_win"], s=80, label="SELL(+)"))
        legend_handles.append(plt.scatter([], [], marker="v",
                                          color=STYLE["sell_loss"], s=80, label="SELL(-)"))

    ax_candle.legend(
        handles=legend_handles,
        loc="upper left", fontsize=8,
        facecolor=STYLE["ax_bg"], edgecolor=STYLE["spine"],
        labelcolor=STYLE["label"],
    )

    # 성과 요약 박스
    trades  = strategy_stats.get("trades", 0)
    wins    = strategy_stats.get("wins", 0)
    wr      = strategy_stats.get("win_rate", 0.0)
    ret     = strategy_stats.get("return_pct", 0.0)
    vs_bh   = strategy_stats.get("vs_bh", 0.0)
    profit  = strategy_stats.get("profit", 0.0)
    info_lines = [
        f"Trades : {trades}",
        f"Wins   : {wins}  ({wr:.1f}%)",
        f"Return : {ret:+.2f}%",
        f"Profit : {profit:+,.0f} KRW",
        f"vs B&H : {vs_bh:+.2f}%",
    ]
    ax_candle.text(
        0.995, 0.98, "\n".join(info_lines),
        transform=ax_candle.transAxes,
        fontsize=8, color=STYLE["label"],
        va="top", ha="right",
        bbox=dict(facecolor=STYLE["ax_bg"], edgecolor=STYLE["spine"],
                  alpha=0.85, boxstyle="round,pad=0.4"),
        linespacing=1.6, family="monospace",
    )

    # ── 거래량 ───────────────────────────────────────────
    style_ax(ax_vol)
    colors_vol = [
        STYLE["volume_up"] if df.loc[i, "close"] >= df.loc[i, "open"]
        else STYLE["volume_down"]
        for i in range(n)
    ]
    ax_vol.bar(df["x"], df["volume"], color=colors_vol, width=0.8, zorder=2)
    ax_vol.set_ylabel("Volume", color=STYLE["label"], fontsize=8)
    ax_vol.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: f"{v/1000:.0f}K" if v >= 1000 else f"{v:.0f}")
    )
    plt.setp(ax_vol.get_xticklabels(), visible=False)

    # ── RSI ──────────────────────────────────────────────
    style_ax(ax_rsi, f"RSI ({RSI_PERIOD})")
    ax_rsi.plot(df["x"], df["rsi"], color=STYLE["rsi"], linewidth=1.0, zorder=3)
    ax_rsi.axhline(RSI_SELL_THRESHOLD, color=STYLE["rsi_ob"], linewidth=0.8, linestyle="--", alpha=0.8)
    ax_rsi.axhline(RSI_BUY_THRESHOLD, color=STYLE["rsi_os"], linewidth=0.8, linestyle="--", alpha=0.8)
    ax_rsi.fill_between(df["x"], df["rsi"], RSI_SELL_THRESHOLD,
                        where=df["rsi"] >= RSI_SELL_THRESHOLD, alpha=0.2,
                        color=STYLE["rsi_ob"], interpolate=True)
    ax_rsi.fill_between(df["x"], df["rsi"], RSI_BUY_THRESHOLD,
                        where=df["rsi"] <= RSI_BUY_THRESHOLD, alpha=0.2,
                        color=STYLE["rsi_os"], interpolate=True)
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_yticks([RSI_BUY_THRESHOLD, 50, RSI_SELL_THRESHOLD])
    ax_rsi.set_ylabel("RSI", color=STYLE["label"], fontsize=8)
    ax_rsi.text(n - 1, df["rsi"].iloc[-1],
                f"  {df['rsi'].iloc[-1]:.1f}", color=STYLE["rsi"], fontsize=7, va="center")
    plt.setp(ax_rsi.get_xticklabels(), visible=False)

    # ── MACD ─────────────────────────────────────────────
    style_ax(ax_macd, f"MACD ({MACD_FAST}, {MACD_SLOW}, {MACD_SIGNAL})")
    ax_macd.plot(df["x"], df["macd"],        color=STYLE["macd"],   linewidth=1.0, label="MACD")
    ax_macd.plot(df["x"], df["signal_line"], color=STYLE["signal"], linewidth=1.0, label="Signal")
    hist_colors = [STYLE["hist_pos"] if v >= 0 else STYLE["hist_neg"] for v in df["hist"]]
    ax_macd.bar(df["x"], df["hist"], color=hist_colors, width=0.8, alpha=0.6, label="Hist")
    ax_macd.axhline(0, color=STYLE["spine"], linewidth=0.6)
    ax_macd.set_ylabel("MACD", color=STYLE["label"], fontsize=8)
    ax_macd.legend(
        loc="upper left", fontsize=7,
        facecolor=STYLE["ax_bg"], edgecolor=STYLE["spine"],
        labelcolor=STYLE["label"],
    )

    # MACD 패널에도 BUY/SELL 수직선
    for bx, _ in buy_pts:
        ax_macd.axvline(bx, color=STYLE["buy_marker"], linewidth=0.8, alpha=0.6, linestyle=":")
    for sx, _, _ in sell_pts:
        ax_macd.axvline(sx, color=STYLE["sell_loss"], linewidth=0.8, alpha=0.6, linestyle=":")

    format_x_labels(ax_macd, df)

    # ── 저장 ─────────────────────────────────────────────
    slug = strategy_name.replace(" ", "_").replace("+", "").replace("/", "")
    out_name = os.path.splitext(csv_path)[0] + f"_{slug}_events.png"
    fig.savefig(out_name, dpi=150, bbox_inches="tight", facecolor=STYLE["fig_bg"])
    plt.close(fig)
    print(f"[✓] 이벤트 차트 저장: {out_name}")
    return out_name


# ─────────────────────────────────────────────
# 실행
# ─────────────────────────────────────────────

def _find_latest(pattern: str) -> str | None:
    """glob 패턴으로 가장 최근 파일 반환."""
    candidates = glob.glob(pattern)
    return max(candidates, key=os.path.getmtime) if candidates else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir   = os.path.join(os.path.dirname(script_dir), "logs")

    # ── CSV 경로 결정 ────────────────────────────────────
    if len(sys.argv) >= 2:
        csv_path = sys.argv[1]
    else:
        csv_path = _find_latest(os.path.join(logs_dir, "raw_*.csv"))
        if csv_path is None:
            print("[오류] CSV 파일을 찾을 수 없습니다.")
            print("사용법: python chart_from_csv_with_event.py <csv_path> [json_path]")
            sys.exit(1)
        print(f"[자동 선택 CSV] {csv_path}")

    # ── JSON 경로 결정 ───────────────────────────────────
    if len(sys.argv) >= 3:
        json_path = sys.argv[2]
    else:
        json_path = _find_latest(os.path.join(logs_dir, "backtest_*.json"))
        if json_path is None:
            print("[오류] backtest JSON 파일을 찾을 수 없습니다.")
            print("먼저 test_strategy.py 를 실행하세요.")
            sys.exit(1)
        print(f"[자동 선택 JSON] {json_path}")

    # ── JSON 로드 ────────────────────────────────────────
    with open(json_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    trade_events = result.get("trade_events", {})
    strategies   = result.get("strategies", {})

    if not trade_events:
        print("[경고] JSON 에 trade_events 가 없습니다. test_strategy.py 를 다시 실행하세요.")
        sys.exit(1)

    # ── 전략별 차트 생성 ─────────────────────────────────
    generated = []
    for strat_name, events in trade_events.items():
        if not events:
            print(f"[스킵] {strat_name}: 거래 이벤트 없음")
            continue
        stats = strategies.get(strat_name, {})
        out = generate_event_chart(csv_path, strat_name, events, stats)
        generated.append(out)

    if not generated:
        print("[경고] 생성된 차트가 없습니다. 거래가 발생한 전략이 없습니다.")
    else:
        print(f"\n총 {len(generated)}개 차트 생성 완료.")


if __name__ == "__main__":
    main()
