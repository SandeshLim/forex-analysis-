import sys, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

src = sys.argv[1]
out = sys.argv[2]

def parse(line):
    p = line.strip().split("|")
    row, name, lvl, side, tb, mr, mv, bars = p[:8]
    lvl = float(lvl); tb = int(tb); mr = float(mr); mv = int(mv)
    B = []
    for b in bars.split(";"):
        m, o, h, l, c, v = b.split(",")
        B.append((int(m), lvl + int(o)/100, lvl + int(h)/100, lvl + int(l)/100, lvl + int(c)/100, int(v)))
    def tr(s):
        s = s[2:]
        if s == "none":
            return None
        te, e, st, tg, tx, x, why, pnl = s.split(",")
        return dict(te=int(te), e=lvl+int(e)/100, st=lvl+int(st)/100, tg=lvl+int(tg)/100,
                    tx=int(tx) if tx else None, x=lvl+int(x)/100, why=why, pnl=float(pnl))
    return dict(row=int(row), name=name, lvl=lvl, side=side, tb=tb, mr=mr, mv=mv, B=B,
                C=tr(p[8]), F=tr(p[9]))

events = [parse(l) for l in open(src) if l.strip()]
# Point-in-time baselines (median range, median tick volume of the 24 bars before each candle), candles -3..0, from engine_v2 pitFlags
PIT = {2: {-3: (3.225, 1574), -2: (3.325, 1574), -1: (3.325, 1690), 0: (3.340, 1706)},
       6: {-3: (2.750, 1162), -2: (2.865, 1162), -1: (2.865, 1162), 0: (2.960, 1162)},
       10: {-3: (3.945, 1786), -2: (3.765, 1773), -1: (3.945, 1773), 0: (3.945, 1773)},
       22: {-3: (3.470, 1448), -2: (3.470, 1448), -1: (3.490, 1526), 0: (3.500, 1563)},
       28: {-3: (3.395, 1389), -2: (3.395, 1389), -1: (3.665, 1399), 0: (4.025, 1413)}}
fig, axes = plt.subplots(len(events)*2, 1, figsize=(11, 4.3*len(events)),
                         gridspec_kw={"height_ratios": [3, 1]*len(events)})

for k, ev in enumerate(events):
    ax, av = axes[2*k], axes[2*k+1]
    t0 = dt.datetime.fromtimestamp(ev["tb"], dt.timezone.utc)
    lab = lambda m: (t0 + dt.timedelta(minutes=m)).strftime("%H:%M")
    for (m, o, h, l, c, v) in ev["B"]:
        col = "#2e7d32" if c >= o else "#c62828"
        ax.plot([m, m], [l, h], color=col, lw=1)
        ax.add_patch(Rectangle((m-1.8, min(o, c)), 3.6, max(abs(c-o), 0.05), color=col))
        av.bar(m, v, width=3.6, color="#90a4ae" if m != 0 else "#37474f")
        if -15 <= m <= 0:
            k = m // 5
            pmr, pmv = PIT[ev["row"]][k]
            f = ("V" if v > 2*pmv else "") + ("R" if h-l > 2*pmr else "") + ("A" if v > 1.5*pmv and h-l < 0.75*pmr else "")
            lg = ("V" if v > 2*ev["mv"] else "") + ("R" if h-l > 2*ev["mr"] else "") + \
                 ("A" if v > 1.5*ev["mv"] and h-l < 0.75*ev["mr"] else "")
            txt = (f or "-") + " @" + lab(m+5)
            if m < 0 and lg != f:
                txt += "\n(legacy: " + (lg or "none") + ")"
            if f or (m < 0 and lg):
                ax.annotate(txt, (m, h), xytext=(-14, 10 + 16*(3+k)), textcoords="offset points", ha="right", fontsize=7,
                            color="#6a1b9a", arrowprops=dict(arrowstyle="-", color="#6a1b9a", lw=0.5))
    ax.axhline(ev["lvl"], color="#1565c0", ls="--", lw=1)
    ax.text(ev["B"][0][0]-1, ev["lvl"], f"level {ev['lvl']:.2f}", va="bottom", fontsize=8, color="#1565c0")
    ax.axvspan(-2.5, 2.5, color="#fff59d", alpha=0.5, zorder=0)
    for key, colr, nm in (("C", "#ef6c00", "Cont"), ("F", "#00838f", "Fade")):
        tdat = ev[key]
        if not tdat:
            continue
        x0 = tdat["te"] - 2.5  # entry at close of signal candle = open of next candle
        x1 = (tdat["tx"] if tdat["tx"] is not None else tdat["te"]+60)
        ax.scatter([x0], [tdat["e"]], marker=">", color=colr, s=60, zorder=5)
        ax.hlines(tdat["st"], x0, x1, colors=colr, linestyles=":", lw=1)
        ax.hlines(tdat["tg"], x0, x1, colors=colr, linestyles="-.", lw=1)
        ax.scatter([x1], [tdat["x"]], marker="x", color=colr, s=50, zorder=5)
        ax.text(x1+0.5, tdat["x"], f"{nm} {tdat['why']} {tdat['pnl']:+.2f}", fontsize=7, color=colr)
    lo = min(b[3] for b in ev["B"]); hi = max(b[2] for b in ev["B"])
    for key in ("C", "F"):
        if ev[key]:
            lo = min(lo, ev[key]["st"], ev[key]["tg"]); hi = max(hi, ev[key]["st"], ev[key]["tg"])
    pad = (hi-lo)*0.12
    ax.set_ylim(lo-pad, hi+pad)
    ticks = list(range(-30, 50, 10))
    for a in (ax, av):
        a.set_xlim(-33, 75)
        a.set_xticks(ticks)
        a.set_xticklabels([lab(m) for m in ticks], fontsize=7)
    ax.set_title(f"Row {ev['row']}: {ev['name']} broken at {lab(0)} UK on {t0:%a %d %b} (5m, OANDA XAUUSD)", fontsize=9, loc="left")
    ax.tick_params(labelsize=7)
    av.axhline(2*ev["mv"], color="#6a1b9a", lw=0.8, ls="--")
    av.text(-32, 2*ev["mv"], "2x median vol", fontsize=6, color="#6a1b9a", va="bottom")
    av.tick_params(labelsize=6)
    av.set_ylabel("tick vol", fontsize=7)

fig.text(0.01, 0.002, "Yellow = break candle. Candles are drawn at their OPEN time; a candle labelled 12:15 covers 12:15:00-12:19:59. Purple = point-in-time footprint flag (baseline = 24 bars before that candle) "
         "and '@hh:mm' = the candle close, the earliest moment the flag is knowable. 'legacy' = flag under the old break-anchored baseline, shown only where it differs.\n"
         "Orange = continuation rule, teal = fade rule: > entry, dotted = stop, dash-dot = target, x = exit. P&L in points after 0.3 cost.",
         fontsize=7)
fig.tight_layout(rect=(0, 0.015, 1, 1))
fig.savefig(out, dpi=110)
print("saved", out)
