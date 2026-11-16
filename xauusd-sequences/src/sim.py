"""Trade simulation for study 2 candidates on 1m bars with spread and slippage.

Signals come from the event tables (5m). A trade is entered at the close of the recognition 5m bar
(= open of the next minute) at that bar's close price, adjusted by slippage. Prices are Exness bid prices;
a short is exited at the ask (bid + spread), so short stops trigger when bid_high + spread >= stop, and short
targets fill when bid_low + spread <= target; longs mirror on the bid. Stop is checked before target within
the same minute. Net P&L = direction * (exit - entry) - spread - 2*slip.
"""
import numpy as np, pandas as pd

SLIP = 0.10

class Sim:
    def __init__(self, m1_path="/home/claude/research/exness_m1.pkl"):
        m = pd.read_pickle(m1_path)
        self.t = (m.index.astype("int64") // 10**9).values
        self.h = m.high.values; self.l = m.low.values; self.c = m.close.values
        self.sp = m.spread.values / 1000.0

    def run(self, entry_time_s, direction, entry, stop, target_R=None, max_min=120):
        """entry_time_s: unix seconds of the first minute after entry; entry = bid close of the signal bar.
        Long: buys at ask (bid + spread + slip), exits at bid. Short: sells at bid - slip, exits at ask (bid + spread).
        Stops get a further slip on exit. Net P&L therefore already contains spread and slippage."""
        i = np.searchsorted(self.t, entry_time_s)
        if i >= len(self.t): return None
        sp0 = self.sp[i - 1] if i > 0 else self.sp[i]
        e = entry + sp0 + SLIP if direction > 0 else entry - SLIP
        risk = abs(e - stop)
        if risk <= 0 or (direction > 0 and stop >= e) or (direction < 0 and stop <= e): return None
        tgt = e + direction * target_R * risk if target_R else None
        end_t = entry_time_s + max_min * 60
        j = i; reason = "time"; px = None; sp = sp0
        while j < len(self.t) and self.t[j] < end_t:
            sp = self.sp[j]
            if direction < 0:
                if self.h[j] + sp >= stop: px, reason = stop + SLIP, "stop"; break
                if tgt is not None and self.l[j] + sp <= tgt: px, reason = tgt, "target"; break
            else:
                if self.l[j] <= stop: px, reason = stop - SLIP, "stop"; break
                if tgt is not None and self.h[j] >= tgt: px, reason = tgt, "target"; break
            j += 1
        if px is None:
            j = max(min(j, len(self.t)) - 1, i); px = self.c[j] + (self.sp[j] if direction < 0 else 0.0)
        net = direction * (px - e)
        return dict(entry=e, stop=stop, target=tgt, risk=risk, exit=px, reason=reason, gross=net + sp0 + 2 * SLIP, net=net,
                    R=net / risk, cost_R=(sp0 + 2 * SLIP) / risk, exit_time=int(self.t[j]))

def stats(tr, key="R", B=4000, seed=11):
    if len(tr) == 0: return {"n": 0}
    rng = np.random.default_rng(seed)
    g = tr.groupby("tday")[key].agg(["sum", "count"]).values
    ix = rng.integers(0, len(g), (B, len(g))); bs = g[ix, 0].sum(1) / g[ix, 1].sum(1)
    srt = tr.sort_values("entry_time"); cum = srt[key].cumsum(); dd = (cum - cum.cummax()).min()
    p = (bs <= 0).mean()
    return dict(n=len(tr), days=tr.tday.nunique(), win=(tr[key] > 0).mean().round(3), expR=tr[key].mean().round(3),
                ci_lo=np.percentile(bs, 2.5).round(3), ci_hi=np.percentile(bs, 97.5).round(3), p_le0=round(p, 4),
                totalR=tr[key].sum().round(1), maxDD_R=round(dd, 1), avg_cost_R=tr["cost_R"].mean().round(3),
                exp_pts=tr["net"].mean().round(3), med_risk=tr["risk"].median().round(2),
                share_target=(tr.reason == "target").mean().round(3), share_stop=(tr.reason == "stop").mean().round(3))
