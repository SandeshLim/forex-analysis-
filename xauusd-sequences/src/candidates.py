"""Build and simulate the frozen candidates C1-C4 (see VARIANT_LOG.md) on one split.
Usage: python3 candidates.py SPLIT [IDS]   e.g.  DEV all   |   VAL C1V2,C2V1   |   TEST C1V2,...
"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sim import Sim, stats

SPLIT = sys.argv[1]; IDS = sys.argv[2] if len(sys.argv) > 2 else "all"
R = "/home/claude/research/"
src = {"DEV": "", "VAL": "", "TEST": "sealed/"}[SPLIT]
suffix = "TEST_SEALED" if SPLIT == "TEST" else SPLIT
seq = pd.read_pickle(f"{R}{src}sequences_{suffix}.pkl"); tch = pd.read_pickle(f"{R}{src}touches_{suffix}.pkl")
b = pd.read_pickle(R + "bars5.pkl")
c5 = b.close.values; t5 = (b.index.astype("int64") // 10**9).values
h5 = b.high.values; l5 = b.low.values
d = b.groupby("tday").close.last(); trend = np.sign(d - d.rolling(20).mean()).shift(1)
seq["dtrend"] = seq.tday.map(trend); tch["dtrend"] = tch.tday.map(trend)
sim = Sim()

def go(sig, target_R, max_min):
    out = []
    for r in sig.itertuples():
        x = sim.run(int(t5[r.ent_i] + 300), int(r.dirn), float(c5[r.ent_i]), float(r.stop), target_R, max_min)
        if x is None or (r.dirn < 0 and x["stop"] <= x["entry"]) or (r.dirn > 0 and x["stop"] >= x["entry"]):
            continue
        x.update(tday=r.tday, entry_time=int(t5[r.ent_i] + 300), dirn=int(r.dirn), sg=int(r.sg), i=int(r.i))
        out.append(x)
    return pd.DataFrame(out)

def seq_signals(stage, aligned_only=False):
    s = seq[(seq.location == "at_level") & seq.ctype.isin(["range_inside", "body_inside_only"])].copy()
    if aligned_only:
        s = s[(-s.sg * s.dtrend) == 1]
    if stage == 1:
        s["ent_i"] = s.i
    elif stage == 2:
        s = s[s.s2 == True]; s["ent_i"] = s.i + s.s2_lag
    else:
        s = s[s.get("s3") == True]; s["ent_i"] = s.i + s.s2_lag + s.s3_lag
    s["ent_i"] = s.ent_i.astype(int)
    s["dirn"] = -s.sg; s["stop"] = s.ext + s.sg * 0.1 * s.mr
    return s.drop_duplicates(["ent_i", "sg"])

def touch_signals(filt):
    s = tch[filt(tch)].copy(); s["ent_i"] = s.i.astype(int); s["dirn"] = -s.sg
    ext = np.where(s.sg > 0, h5[s.i.values], l5[s.i.values]); s["stop"] = ext + s.sg * 0.5 * s.mr
    return s.drop_duplicates(["ent_i", "sg"])

late = lambda x: x.session == "Late"
algn = lambda x: (-x.sg * x.dtrend) == 1
V = {
    "C1V1": lambda: go(seq_signals(1), 2, 120), "C1V2": lambda: go(seq_signals(2), 2, 120), "C1V3": lambda: go(seq_signals(3), 2, 120),
    "C2V1": lambda: go(seq_signals(2, True), 1, 120), "C2V2": lambda: go(seq_signals(2, True), 2, 120), "C2V3": lambda: go(seq_signals(2, True), 3, 120),
    "C3V1": lambda: go(touch_signals(lambda x: x.pen >= 1.0), None, 60), "C3V2": lambda: go(touch_signals(lambda x: x.pen >= 1.3), None, 60),
    "C3V3": lambda: go(touch_signals(lambda x: x.pen >= 1.6), None, 60),
    "C4V1": lambda: go(touch_signals(late), None, 60), "C4V2": lambda: go(touch_signals(lambda x: late(x) & algn(x)), None, 60),
    "C4V3": lambda: go(touch_signals(lambda x: late(x) & algn(x) & (x.close_beyond == 0)), None, 60),
}
ids = list(V) if IDS == "all" else IDS.split(",")
rows = []
for k in ids:
    tr = V[k](); tr.to_pickle(f"{R}trades_{SPLIT}_{k}.pkl")
    st = stats(tr); st.update(variant=k, split=SPLIT)
    for dname, g in tr.groupby("dirn"):
        st[f"expR_{'long' if dname > 0 else 'short'}"] = round(g.R.mean(), 3); st[f"n_{'long' if dname > 0 else 'short'}"] = len(g)
    st["expR_2xcost"] = round((tr.R - tr.cost_R).mean(), 3) if len(tr) else np.nan
    rows.append(st); print(st, flush=True)
pd.DataFrame(rows).to_csv(f"{R}results_{SPLIT}_{IDS.replace(',', '_')}.csv", index=False)
