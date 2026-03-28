"""
Strategy Backtest Chart Generator
backtest_*.json 결과 파일 기반 차트 생성

사용법: python generate_chart.py [backtest_json_path]
       인자 없으면 같은 폴더의 최신 backtest_*.json 자동 선택
"""

import sys
import os
import glob
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# JSON 결과 파일 로드
# ─────────────────────────────────────────────
if len(sys.argv) >= 2:
    _json_path = sys.argv[1]
else:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _logs_dir = os.path.join(os.path.dirname(_script_dir), 'logs')
    _candidates = glob.glob(os.path.join(_logs_dir, "backtest_*.json"))
    if not _candidates:
        print("[Error] backtest_*.json not found. Run test_strategy.py first.")
        sys.exit(1)
    _json_path = max(_candidates, key=os.path.getmtime)
    print(f"[Auto] {_json_path}")

with open(_json_path, 'r', encoding='utf-8') as _f:
    _data = json.load(_f)

PERIOD              = _data['period']
SYMBOL              = _data['symbol']
INIT_BAL            = _data['initial_balance']
strategies          = _data['strategies']
BUY_AND_HOLD_RETURN = _data['buy_and_hold_return']
trade_pnl           = _data['trade_pnl']
current_indicators  = _data.get('current_indicators', {})

# ─────────────────────────────────────────────
# 색상 팔레트 (전략명 동적 할당)
# ─────────────────────────────────────────────
_PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
            "#CCB974", "#64B5CD", "#E377C2", "#7F7F7F", "#BCBD22"]
COLORS = {"B&H": "#937860", "pos": "#2ecc71", "neg": "#e74c3c", "neutral": "#95a5a6"}
for _i, _name in enumerate(strategies.keys()):
    COLORS[_name] = _PALETTE[_i % len(_PALETTE)]

strat_names = list(strategies.keys())
strat_colors = [COLORS[s] for s in strat_names]

# ─────────────────────────────────────────────
# Figure 레이아웃
# ─────────────────────────────────────────────
fig = plt.figure(figsize=(20, 22))
fig.patch.set_facecolor("#1a1a2e")

gs = gridspec.GridSpec(
    4, 3,
    figure=fig,
    hspace=0.52,
    wspace=0.38,
    left=0.06, right=0.97,
    top=0.93, bottom=0.04,
)

TITLE_COLOR   = "#e0e0e0"
LABEL_COLOR   = "#b0b0b0"
GRID_COLOR    = "#2e2e4e"
BG_AXES       = "#16213e"
SPINE_COLOR   = "#2e2e4e"

def style_ax(ax, title=""):
    ax.set_facecolor(BG_AXES)
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    ax.tick_params(colors=LABEL_COLOR, labelsize=9)
    ax.xaxis.label.set_color(LABEL_COLOR)
    ax.yaxis.label.set_color(LABEL_COLOR)
    ax.grid(color=GRID_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)
    if title:
        ax.set_title(title, color=TITLE_COLOR, fontsize=11, fontweight="bold", pad=8)

# ─────────────────────────────────────────────
# 상단 타이틀
# ─────────────────────────────────────────────
fig.text(0.5, 0.965, "Strategy Backtest Dashboard",
         ha='center', va='center', fontsize=18, fontweight='bold', color=TITLE_COLOR)
fig.text(0.5, 0.950, f"{SYMBOL}  |  {PERIOD}",
         ha='center', va='center', fontsize=11, color=LABEL_COLOR)

# ══════════════════════════════════════════════
# [Row 0, Col 0] 전략 수익률 비교 막대
# ══════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1, "Return (%) vs Buy & Hold")

returns = [strategies[s]["return_pct"] for s in strat_names]
bar_colors = [COLORS["pos"] if r >= 0 else COLORS["neg"] for r in returns]
bars = ax1.bar(strat_names, returns, color=bar_colors, alpha=0.85, width=0.6, zorder=3)
ax1.axhline(y=BUY_AND_HOLD_RETURN, color=COLORS["B&H"], linestyle="--",
            linewidth=1.8, label=f"B&H: +{BUY_AND_HOLD_RETURN:.2f}%", zorder=4)
ax1.axhline(y=0, color=LABEL_COLOR, linewidth=0.8, alpha=0.5, zorder=2)
for bar, val in zip(bars, returns):
    sign = "+" if val >= 0 else ""
    ax1.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + (0.02 if val >= 0 else -0.06),
             f"{sign}{val:.2f}%",
             ha='center', va='bottom', color=TITLE_COLOR, fontsize=9, fontweight='bold')
ax1.legend(fontsize=9, facecolor=BG_AXES, labelcolor=LABEL_COLOR, framealpha=0.7)
ax1.set_ylabel("Return (%)", fontsize=9)
ax1.set_ylim(min(returns) - 0.3, BUY_AND_HOLD_RETURN + 0.4)

# ══════════════════════════════════════════════
# [Row 0, Col 1] 승률 비교
# ══════════════════════════════════════════════
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2, "Win Rate (%)")

win_rates = [strategies[s]["wins"] / max(strategies[s]["trades"], 1) * 100 for s in strat_names]
bars2 = ax2.bar(strat_names, win_rates, color=strat_colors, alpha=0.85, width=0.6, zorder=3)
ax2.axhline(y=50, color=LABEL_COLOR, linestyle=":", linewidth=1, alpha=0.6)
for bar, val in zip(bars2, win_rates):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
             f"{val:.1f}%", ha='center', va='bottom', color=TITLE_COLOR, fontsize=9, fontweight='bold')
ax2.set_ylabel("Win Rate (%)", fontsize=9)
ax2.set_ylim(0, 120)

# ══════════════════════════════════════════════
# [Row 0, Col 2] 거래 횟수 / 승・패
# ══════════════════════════════════════════════
ax3 = fig.add_subplot(gs[0, 2])
style_ax(ax3, "Trade Count (Win / Loss)")

x = np.arange(len(strat_names))
w = 0.35
wins_arr   = [strategies[s]["wins"]   for s in strat_names]
losses_arr = [strategies[s]["losses"] for s in strat_names]
ax3.bar(x - w/2, wins_arr,   width=w, color=COLORS["pos"], alpha=0.85, label="Win",  zorder=3)
ax3.bar(x + w/2, losses_arr, width=w, color=COLORS["neg"], alpha=0.85, label="Loss", zorder=3)
ax3.set_xticks(x)
ax3.set_xticklabels(strat_names, fontsize=9)
ax3.set_ylabel("# Trades", fontsize=9)
ax3.legend(fontsize=9, facecolor=BG_AXES, labelcolor=LABEL_COLOR, framealpha=0.7)

# ══════════════════════════════════════════════
# [Row 1, Col 0-2] 누적 P&L 곡선 (전 전략)
# ══════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, :])
style_ax(ax4, "Cumulative P&L per Strategy (KRW)")

for s in strat_names:
    pnl = trade_pnl[s]
    cum = np.cumsum([0] + pnl)
    trade_idx = list(range(len(cum)))
    ax4.plot(trade_idx, cum, marker='o', markersize=5, linewidth=2,
             color=COLORS[s], label=s, zorder=3)
    # 최종값 표시
    end_val = cum[-1]
    sign = "+" if end_val >= 0 else ""
    ax4.annotate(f"{sign}{end_val:,.0f}", xy=(trade_idx[-1], end_val),
                 xytext=(5, 0), textcoords='offset points',
                 color=COLORS[s], fontsize=8, va='center')

ax4.axhline(y=0, color=LABEL_COLOR, linewidth=1, linestyle="--", alpha=0.6)
ax4.set_xlabel("Trade #", fontsize=9)
ax4.set_ylabel("Cumulative P&L (KRW)", fontsize=9)
ax4.legend(fontsize=9, facecolor=BG_AXES, labelcolor=LABEL_COLOR, framealpha=0.7,
           ncol=5, loc='upper left')

# ══════════════════════════════════════════════
# [Row 2, Col 0] RSI – 개별 거래 P&L
# ══════════════════════════════════════════════
def plot_trade_pnl(ax, strategy_name):
    style_ax(ax, f"{strategy_name} – Individual Trade P&L (KRW)")
    pnl = trade_pnl[strategy_name]
    colors = [COLORS["pos"] if v >= 0 else COLORS["neg"] for v in pnl]
    x = np.arange(1, len(pnl) + 1)
    ax.bar(x, pnl, color=colors, alpha=0.85, zorder=3)
    ax.axhline(y=0, color=LABEL_COLOR, linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Trade #", fontsize=8)
    ax.set_ylabel("P&L (KRW)", fontsize=8)
    total = sum(pnl)
    sign = "+" if total >= 0 else ""
    ax.set_title(f"{strategy_name} – Individual Trade P&L (KRW)  [Total: {sign}{total:,.0f}]",
                 color=TITLE_COLOR, fontsize=10, fontweight='bold', pad=7)

for col, sname in enumerate(strat_names[:3]):
    ax_t = fig.add_subplot(gs[2, col])
    plot_trade_pnl(ax_t, sname)

for col, sname in enumerate(strat_names[3:5]):
    ax_t = fig.add_subplot(gs[3, col])
    plot_trade_pnl(ax_t, sname)

# ══════════════════════════════════════════════
# [Row 3, Col 2] 최종 잔고 비교 + 현재 지표
# ══════════════════════════════════════════════
ax_sum = fig.add_subplot(gs[3, 2])
style_ax(ax_sum, "Final Balance (KRW)")

final_bals = [INIT_BAL + strategies[s]["profit"] for s in strat_names]
bh_final   = INIT_BAL * (1 + BUY_AND_HOLD_RETURN / 100)

all_vals = final_bals + [bh_final]
all_names = strat_names + ["B&H"]
all_colors = strat_colors + [COLORS["B&H"]]
bar_final = ax_sum.bar(all_names, all_vals, color=all_colors, alpha=0.85, width=0.6, zorder=3)
ax_sum.axhline(y=INIT_BAL, color=LABEL_COLOR, linestyle="--", linewidth=1, alpha=0.7,
               label=f"Initial: {INIT_BAL:,}")
for bar, val in zip(bar_final, all_vals):
    diff = val - INIT_BAL
    sign = "+" if diff >= 0 else ""
    ax_sum.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                f"{sign}{diff:,.0f}",
                ha='center', va='bottom', color=TITLE_COLOR, fontsize=7.5, fontweight='bold')
ax_sum.set_ylabel("Balance (KRW)", fontsize=9)
ax_sum.set_ylim(min(all_vals) - 2000, max(all_vals) + 3000)
ax_sum.tick_params(axis='x', labelsize=8)
ax_sum.legend(fontsize=8, facecolor=BG_AXES, labelcolor=LABEL_COLOR, framealpha=0.7)

# ─────────────────────────────────────────────
# 저장
# ─────────────────────────────────────────────
out_path = os.path.splitext(_json_path)[0] + "_chart.png"
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"Chart saved → {out_path}")
