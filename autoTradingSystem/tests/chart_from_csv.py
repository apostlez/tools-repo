"""
CSV 기반 캔들스틱 차트 생성기
사용법: python chart_from_csv.py [csv파일경로]
예시: python chart_from_csv.py raw_XRP_KRW_1m_2603290425.csv
"""

import sys
import os
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime


# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
STYLE = {
    "fig_bg":     "#1a1a2e",
    "ax_bg":      "#16213e",
    "title":      "#e0e0e0",
    "label":      "#b0b0b0",
    "grid":       "#2e2e4e",
    "spine":      "#2e2e4e",
    "up":         "#26a69a",   # 양봉 (초록)
    "down":       "#ef5350",   # 음봉 (빨강)
    "volume_up":  "#26a69a80",
    "volume_down":"#ef535080",
    "ma20":       "#ff9f43",
    "ma60":       "#54a0ff",
    "rsi":        "#a29bfe",
    "rsi_ob":     "#e17055",
    "rsi_os":     "#00cec9",
    "macd":       "#74b9ff",
    "signal":     "#fd79a8",
    "hist_pos":   "#26a69a",
    "hist_neg":   "#ef5350",
}


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


def calc_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def calc_macd(close: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist


def draw_candlesticks(ax, df):
    """캔들스틱 직접 그리기"""
    for i, row in df.iterrows():
        color = STYLE["up"] if row["close"] >= row["open"] else STYLE["down"]
        # 심지 (wick)
        ax.plot([row["x"], row["x"]], [row["low"], row["high"]],
                color=color, linewidth=0.8, zorder=1)
        # 몸통 (body)
        body_low = min(row["open"], row["close"])
        body_high = max(row["open"], row["close"])
        body_height = max(body_high - body_low, 0.5)  # 도지 캔들도 보이게
        rect = mpatches.FancyBboxPatch(
            (row["x"] - 0.35, body_low), 0.7, body_height,
            boxstyle="square,pad=0",
            facecolor=color, edgecolor=color, linewidth=0, zorder=2
        )
        ax.add_patch(rect)


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["x"] = range(len(df))  # x축 정수 인덱스 (캔들 간격 균일)
    return df


def format_x_labels(ax, df, max_labels: int = 10):
    """x축 레이블을 타임스탬프로 설정"""
    step = max(1, len(df) // max_labels)
    ticks = list(range(0, len(df), step))
    labels = [df.loc[i, "timestamp"].strftime("%m/%d\n%H:%M") for i in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=7, color=STYLE["label"])


def generate_chart(csv_path: str):
    # ── 데이터 로드 ──────────────────────────────────────
    df = load_csv(csv_path)
    n = len(df)

    # 파일명에서 심볼 추출
    basename = os.path.basename(csv_path)
    symbol = basename.replace("raw_", "").replace(".csv", "")
    # raw_XRP_KRW_1m_2603290425 → XRP/KRW (1m)
    parts = symbol.split("_")
    if len(parts) >= 3:
        symbol_label = f"{parts[0]}/{parts[1]} ({parts[2]})"
    else:
        symbol_label = symbol

    date_range = (
        f"{df['timestamp'].iloc[0].strftime('%Y-%m-%d %H:%M')} ~ "
        f"{df['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M')}"
    )

    # ── 지표 계산 ─────────────────────────────────────────
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()
    df["rsi"]  = calc_rsi(df["close"], 14)
    df["macd"], df["signal"], df["hist"] = calc_macd(df["close"])

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

    # ── 캔들스틱 ─────────────────────────────────────────
    style_ax(ax_candle, f"{symbol_label}  |  {date_range}")
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

    legend = ax_candle.legend(
        loc="upper left", fontsize=8,
        facecolor=STYLE["ax_bg"], edgecolor=STYLE["spine"],
        labelcolor=STYLE["label"]
    )

    # 현재가 수평선
    last_close = df["close"].iloc[-1]
    ax_candle.axhline(last_close, color="#ffeaa7", linewidth=0.7,
                      linestyle="--", alpha=0.8, zorder=4)
    ax_candle.text(
        n - 0.5, last_close,
        f"  {last_close:,.0f}",
        color="#ffeaa7", fontsize=8, va="center", ha="left",
        clip_on=False
    )

    # x축 레이블 숨기기 (공유 axes)
    plt.setp(ax_candle.get_xticklabels(), visible=False)

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
    style_ax(ax_rsi, "RSI (14)")
    ax_rsi.plot(df["x"], df["rsi"], color=STYLE["rsi"], linewidth=1.0)
    ax_rsi.axhline(70, color=STYLE["rsi_ob"], linewidth=0.8, linestyle="--", alpha=0.8)
    ax_rsi.axhline(30, color=STYLE["rsi_os"], linewidth=0.8, linestyle="--", alpha=0.8)
    ax_rsi.fill_between(df["x"], df["rsi"], 70,
                         where=df["rsi"] >= 70, alpha=0.2,
                         color=STYLE["rsi_ob"], interpolate=True)
    ax_rsi.fill_between(df["x"], df["rsi"], 30,
                         where=df["rsi"] <= 30, alpha=0.2,
                         color=STYLE["rsi_os"], interpolate=True)
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_yticks([30, 50, 70])
    ax_rsi.set_ylabel("RSI", color=STYLE["label"], fontsize=8)
    ax_rsi.text(n - 1, df["rsi"].iloc[-1],
                f"  {df['rsi'].iloc[-1]:.1f}", color=STYLE["rsi"], fontsize=7, va="center")
    plt.setp(ax_rsi.get_xticklabels(), visible=False)

    # ── MACD ─────────────────────────────────────────────
    style_ax(ax_macd, "MACD (12, 26, 9)")
    ax_macd.plot(df["x"], df["macd"],   color=STYLE["macd"],   linewidth=1.0, label="MACD")
    ax_macd.plot(df["x"], df["signal"], color=STYLE["signal"], linewidth=1.0, label="Signal")
    hist_colors = [STYLE["hist_pos"] if v >= 0 else STYLE["hist_neg"] for v in df["hist"]]
    ax_macd.bar(df["x"], df["hist"], color=hist_colors, width=0.8, alpha=0.6, label="Hist")
    ax_macd.axhline(0, color=STYLE["spine"], linewidth=0.6)
    ax_macd.set_ylabel("MACD", color=STYLE["label"], fontsize=8)
    legend2 = ax_macd.legend(
        loc="upper left", fontsize=7,
        facecolor=STYLE["ax_bg"], edgecolor=STYLE["spine"],
        labelcolor=STYLE["label"]
    )

    # x축 레이블
    format_x_labels(ax_macd, df)

    # ── 통계 정보 텍스트 ─────────────────────────────────
    price_change = df["close"].iloc[-1] - df["close"].iloc[0]
    price_change_pct = (price_change / df["close"].iloc[0]) * 100
    high = df["high"].max()
    low  = df["low"].min()
    total_vol = df["volume"].sum()

    info_lines = [
        f"Open : {df['open'].iloc[0]:,.0f}",
        f"Last : {df['close'].iloc[-1]:,.0f}",
        f"Chg  : {price_change:+,.0f} ({price_change_pct:+.2f}%)",
        f"High : {high:,.0f}",
        f"Low  : {low:,.0f}",
        f"Vol  : {total_vol:,.0f}",
        f"Bars : {n}",
    ]
    info_str = "\n".join(info_lines)
    ax_candle.text(
        0.995, 0.98, info_str,
        transform=ax_candle.transAxes,
        fontsize=8, color=STYLE["label"],
        va="top", ha="right",
        bbox=dict(facecolor=STYLE["ax_bg"], edgecolor=STYLE["spine"],
                  alpha=0.85, boxstyle="round,pad=0.4"),
        linespacing=1.6,
        family="monospace"
    )

    # ── 저장 ─────────────────────────────────────────────
    out_name = os.path.splitext(csv_path)[0] + "_chart.png"
    fig.savefig(out_name, dpi=150, bbox_inches="tight",
                facecolor=STYLE["fig_bg"])
    plt.close(fig)
    print(f"[✓] 차트 저장 완료: {out_name}")
    return out_name


# ─────────────────────────────────────────────
# 실행
# ─────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        target = sys.argv[1]
    else:
        # 인자 없으면 logs/ 폴더의 최신 raw_*.csv 자동 선택
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(os.path.dirname(script_dir), 'logs')
        candidates = glob.glob(os.path.join(logs_dir, "raw_*.csv"))
        if not candidates:
            print("[오류] CSV 파일을 찾을 수 없습니다.")
            print("사용법: python chart_from_csv.py <csv파일경로>")
            sys.exit(1)
        target = max(candidates, key=os.path.getmtime)
        print(f"[자동 선택] {target}")

    generate_chart(target)
