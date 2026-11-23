import datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

INK, MUTED, GRID = "#1f1f1f", "#6b6b6b", "#e6e6e6"
UP, DN = "#3a9d5d", "#1f1f1f"
SELLZ, BUYZ, PINK = "#d9534f", "#3a9d5d", "#c48aa8"
BLUE, ORG = "#2a5db0", "#c46a00"

data = {}
for line in open("data.txt"):
    k, v = line.strip().split("|")
    data[k] = [tuple(float(x) for x in r.split(",")) for r in v.split(";")]


def utc(t):
    return dt.datetime.utcfromtimestamp(t)


def candles(ax, bars, w=0.62):
    for i, (t, o, h, l, c) in enumerate(bars):
        col = UP if c >= o else DN
        ax.plot([i, i], [l, h], color=col, lw=1, zorder=3)
        ax.add_patch(Rectangle((i - w / 2, min(o, c)), w, max(abs(c - o), 0.05),
                               facecolor=col, edgecolor=col, zorder=4))


def idx(bars, hh, mm, day=None):
    for i, b in enumerate(bars):
        d = utc(b[0])
        if d.hour == hh and d.minute == mm and (day is None or d.day == day):
            return i
    raise KeyError((hh, mm, day))


def note(ax, x, y, text, col=INK, xt=None, yt=None, size=9, ha="left"):
    if xt is None:
        ax.text(x, y, text, color=col, fontsize=size, ha=ha, va="center", zorder=10,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, lw=1))
    else:
        ax.annotate(text, xy=(x, y), xytext=(xt, yt), color=col, fontsize=size, ha=ha, va="center",
                    zorder=10, arrowprops=dict(arrowstyle="-", color=col, lw=1),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, lw=1))


def base(ax, bars, title, sub, step, fmt="%H:%M"):
    ax.set_title(title, loc="left", fontsize=13, color=INK, fontweight="bold", pad=22)
    ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=9, color=MUTED)
    ticks = list(range(0, len(bars), step))
    ax.set_xticks(ticks)
    ax.set_xticklabels([utc(bars[i][0]).strftime(fmt) for i in ticks], fontsize=8, color=MUTED)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.yaxis.tick_right()
    ax.grid(True, color=GRID, lw=0.6)
    for s in ax.spines.values():
        s.set_visible(False)


# ---------- 1. Zone origin, 19 Nov 15m ----------
A = data["A"]
fig, ax = plt.subplots(figsize=(13, 7), dpi=130)
candles(ax, A)
n = len(A)
i1745 = idx(A, 17, 45)
ax.add_patch(Rectangle((i1745 - 0.5, 3685.91), n - i1745 + 0.5, 3690.72 - 3685.91, fc=PINK, alpha=0.45, ec="none", zorder=1))
ax.text(n - 0.3, 3688.3, "Your zone 3685.91–3690.72", ha="right", va="center", fontsize=9, color=INK, zorder=11)
i18 = idx(A, 18, 0)
ax.add_patch(Rectangle((i18 - 0.5, 3681.0), n - i18 + 0.5, 3687.3 - 3681.0, fill=False, ec=SELLZ, ls="--", lw=1.2, zorder=2))
ax.text(n - 0.3, 3679.6, "1H base rule: 3681.0–3687.3", ha="right", fontsize=8, color=SELLZ)
for hh, mm, p in [(15, 30, 3693.89), (16, 30, 3690.49), (16, 45, 3692.24), (17, 15, 3690.88), (17, 30, 3692.36)]:
    ax.plot(idx(A, hh, mm), p + 0.8, marker="v", color=SELLZ, ms=7, zorder=6)
note(ax, idx(A, 16, 45), 3692.24 + 1.5, "Five pushes failed at 3690.5–3693.9 (15:30–17:30)", SELLZ, 2.0, 3707, ha="left")
ax.hlines(3667.58, idx(A, 15, 30), idx(A, 21, 0), colors=BLUE, linestyles=":", lw=1.2)
ax.text(idx(A, 15, 30), 3666.2, "Range low 3667.6 (17:00)", fontsize=8, color=BLUE, va="top")
note(ax, idx(A, 20, 45), 3660.04, "20:45 closes 3660.0, below the range low\n→ zone identifiable from 21:00", BLUE, idx(A, 18, 0), 3652, ha="left")
note(ax, idx(A, 21, 30), 3634.71, "Displacement: −28 in one candle", INK, idx(A, 19, 45), 3640, ha="left")
note(ax, 1, 3732, "Untouched until Mon 23 Nov 14:30 (high 3689.9)", MUTED)
ax.set_ylim(3615, 3735)
ax.set_xlim(-1, n)
base(ax, A, "Where your zone came from: 15m, Thu 19 Nov 2026",
     "OANDA XAUUSD · UK time · the range top before the breakdown", 4)
fig.tight_layout()
fig.savefig("23Nov_1_zone_origin_19Nov_15m.png")

# ---------- 2. Reaction, 23 Nov 1m ----------
B = data["B"]
fig, ax = plt.subplots(figsize=(13, 7), dpi=130)
candles(ax, B, 0.7)
n = len(B)
ax.axhspan(3685.91, 3690.72, color=PINK, alpha=0.45, zorder=1)
ax.text(n - 0.5, 3690.2, "Your zone", ha="right", va="center", fontsize=9, color=INK)
ax.axhline(3693.89, color=SELLZ, ls=":", lw=1)
ax.text(n - 0.5, 3694.4, "19 Nov highest wick 3693.9", ha="right", fontsize=8, color=SELLZ)
note(ax, idx(B, 14, 24), 3684.83, "14:24 first entry into the zone", INK, idx(B, 14, 2), 3681, ha="left")
note(ax, idx(B, 14, 27), 3686.4, "14:25–14:28 four highs 3685.9–3686.4: stall", BLUE, idx(B, 14, 2), 3692, ha="left")
note(ax, idx(B, 14, 30), 3689.86, "14:30 PEAK 3689.86 (US stock open; 1m volume about 2×)", SELLZ, idx(B, 14, 36), 3697, ha="left")
note(ax, idx(B, 14, 32), 3689.19, "14:31–14:32 lower highs 3689.1 / 3689.2", BLUE, idx(B, 14, 40), 3692.5, ha="left")
note(ax, idx(B, 14, 33), 3680.26, "14:33 closes 3680.3, below the 14:30 low 3682.4\n= 1m confirmation (stop 3690.1, risk 9.8)", ORG, idx(B, 14, 40), 3683.5, ha="left")
note(ax, idx(B, 15, 9), 3657.70, "15:09 low 3657.7 (2R for the 1m entry)", INK, idx(B, 14, 50), 3651, ha="left")
ax.hlines(3685.91, idx(B, 14, 25), n - 1, colors=PINK, lw=1.5)
note(ax, idx(B, 15, 13), 3648.5, "First-touch sell 3685.91, stop 3691.22 (risk 5.3): worst 0.74R against,\n2R 14:34, 5R 15:09. A stop just 2.6 lower would have been hit.", INK, size=8.5, ha="right")
ax.set_ylim(3644, 3700)
ax.set_xlim(-1, n)
base(ax, B, "The reaction: 1m, Mon 23 Nov 2026, 14:00–15:20",
     "OANDA XAUUSD · UK time · arrival came straight after the 13:56 headline jump (+26 in one missing minute)", 5)
fig.tight_layout()
fig.savefig("23Nov_2_reaction_1m.png")

# ---------- 3. Map for Tuesday, 15m 22 Nov 23:00 → 23 Nov 21:30 ----------
C = data["C"]
fig, ax = plt.subplots(figsize=(14, 8), dpi=130)
candles(ax, C, 0.6)
n = len(C)
right = n + 22
zones = [
    ("S1 sell 3653.4–3659.7 · 1H base 18:00–19:59, known 21:00", 3653.4, 3659.7, SELLZ, idx(C, 18, 0)),
    ("S2 sell 3672.3–3681.3 · 1H base 15:00–16:59, known 18:00", 3672.3, 3681.3, SELLZ, idx(C, 15, 0)),
    ("S3 sell 3685.9–3690.7 · your zone, already visited once", 3685.91, 3690.72, PINK, idx(C, 14, 30)),
    ("B1 buy (conditional) 3600.5–3614.4 · 1H base 08:00–13:59", 3600.5, 3614.4, BUYZ, idx(C, 8, 0)),
    ("B2 buy (conditional) 3589.0–3591.7 · 1H base 03:00–04:59", 3589.0, 3591.7, BUYZ, idx(C, 3, 0)),
    ("B3 buy (conditional) 3558.6–3573.0 · Monday-open base", 3558.63, 3573.0, BUYZ, 0),
]
for lab, lo, hi, col, start in zones:
    ax.add_patch(Rectangle((start - 0.5, lo), right - start, hi - lo, fc=col, alpha=0.22 if col != PINK else 0.45, ec=col, lw=0.8, zorder=1))
    ax.text(right - 0.3, (lo + hi) / 2, lab, ha="right", va="center", fontsize=8.2, color=INK, zorder=11,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))
ax.axhline(3538.2, color=MUTED, ls=":", lw=1)
ax.text(1, 3540, "Friday close 3538.2 (weekend gap up to 3576.2)", fontsize=8, color=MUTED)
ax.axhline(3689.86, color=INK, ls="--", lw=1)
ax.text(1, 3692.5, "4H trend-change line: 3689.9 once confirmed as a 4H swing high (~06:00 Tue); until then 3891.1", fontsize=8.5, color=INK)
note(ax, idx(C, 13, 45), 3611.48, "13:54 1H higher low 3611.5", BLUE, idx(C, 10, 0), 3585, ha="left")
ax.axvline(n - 0.5, color=MUTED, lw=0.8)
ax.text(n + 0.3, 3700, "Tuesday 24 Nov →\nconditional zones", fontsize=8.5, color=MUTED, va="top")
note(ax, n - 1, 3633.15, "Last 15m close 3633.2 (21:30)", INK, n + 1, 3628, ha="left")
ax.set_ylim(3530, 3705)
ax.set_xlim(-1, right)
ticks = list(range(0, n, 8))
base(ax, C, "Tuesday map: 15m, Sun 22 Nov 23:00 – Mon 23 Nov 21:30",
     "OANDA XAUUSD · UK time · 4H trend bearish → sell zones first; buy zones only after a defined trend change", 8)
fig.tight_layout()
fig.savefig("23Nov_3_Tuesday_zones_15m.png")
print("ok")
