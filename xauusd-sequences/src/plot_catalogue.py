"""Annotated catalogue: C1V2 (user's sequence at a level, stage-2 entry) on TEST, selected by a fixed rule
(first two target hits, first two stop-outs and first two time exits in 2025), so the examples are not hand-picked."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R = "/home/claude/research/"
b = pd.read_pickle(R + "bars5.pkl"); tr = pd.read_pickle(R + "trades_TEST_C1V2.pkl")
sq = pd.read_pickle(R + "sealed/sequences_TEST_SEALED.pkl").set_index("i")
tr["dt"] = pd.to_datetime(tr.entry_time, unit="s", utc=True)
y = tr[tr.dt.dt.year == 2025].sort_values("dt")
pick = pd.concat([y[y.reason == "target"].head(2), y[y.reason == "stop"].head(2), y[y.reason == "time"].head(2)])
fig, axes = plt.subplots(3, 2, figsize=(14, 13))
for ax, r in zip(axes.flat, pick.itertuples()):
    s = sq.loc[r.i]; i = r.i; lo, hi = i - 14, i + 30
    seg = b.iloc[lo:hi]
    for k, (ts, v) in enumerate(seg.iterrows()):
        x = lo + k; col = "#2e7d32" if v.close >= v.open else "#c62828"
        ax.plot([x, x], [v.low, v.high], color=col, lw=0.8)
        ax.add_patch(Rectangle((x - 0.35, min(v.open, v.close)), 0.7, max(abs(v.close - v.open), 1e-3), color=col))
    lvl_names = str(s.levels).split("+"); side = "H" if s.sg > 0 else "L"
    for nm in lvl_names:
        L = b[f"{nm}_{side}"].iloc[i]
        ax.axhline(L, color="#1565c0", ls="--", lw=1); ax.text(lo, L, f" completed {nm} {'high' if side == 'H' else 'low'} {L:.2f}", color="#1565c0", fontsize=7, va="bottom")
    ent = i + int(s.s2_lag)
    for x, lab in ((i - 1, "B1"), (i, "B2"), (ent, "B3")):
        ax.annotate(lab, (x, b.high.iloc[x] if s.sg > 0 else b.low.iloc[x]), xytext=(0, 8 if s.sg > 0 else -14), textcoords="offset points", ha="center", fontsize=8, color="#6a1b9a")
    ex = (r.exit_time - b.index[0].value // 10**9) // 300
    ex_i = int(np.searchsorted(b.index.astype("int64") // 10**9, r.exit_time, side="right") - 1)
    ax.hlines(r.entry, ent + 0.5, ex_i, colors="black", lw=1); ax.hlines(r.stop, ent + 0.5, ex_i, colors="#c62828", ls=":")
    if r.target == r.target and r.target is not None:
        ax.hlines(r.target, ent + 0.5, ex_i, colors="#2e7d32", ls="-.")
    ax.scatter([ex_i], [r.exit], marker="x", color="black", zorder=5)
    uk = r.dt.tz_convert("Europe/London")
    ax.set_title(f"{uk:%a %d %b %Y %H:%M} UK  {'bearish at high' if s.sg > 0 else 'bullish at low'}  {s.ctype}  "
                 f"{'sweep' if s.sweep else 'test'}\nexit: {r.reason}, {r.R:+.2f}R (risk {r.risk:.2f} pts, cost {r.cost_R:.2f}R); move before entry {s.s2_already:.1f} mr", fontsize=8)
    ax.set_xticks([lo, i, hi - 1]); ax.set_xticklabels([f"{b.index[x].tz_convert('Europe/London'):%H:%M}" for x in (lo, i, hi - 1)], fontsize=7)
    ax.tick_params(labelsize=7)
fig.text(0.01, 0.005, "Exness XAUUSDm 5m bars (UK time). B1 strong candle toward the level, B2 small opposite candle (containment as titled), B3 opposing expansion = entry at its close. "
         "Black = entry, red dotted = stop (sequence extreme + 0.1 mr), green dash-dot = 2R target, x = exit. Selection rule: first two target, stop and time exits of 2025.", fontsize=7)
fig.tight_layout(rect=(0, 0.015, 1, 1)); fig.savefig(R + "catalogue_C1V2_TEST2025.png", dpi=105); print("ok", len(pick))
