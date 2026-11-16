"""Event tables for study 2. All features use only information available at the stated recognition time.

touches   : every first-entry episode of price into a completed level from the near side ("touch"), with
            approach / interaction / context features measured up to the close of the touch bar.
sequences : the user's sequence and its mirror at the 5m level:
            B1 strong candle toward the level, B2 small opposite candle (containment typed), optional B3 expansion
            away from the level, optional retest; plus the same B1/B2 pattern away from any level.
Outcomes are always measured forward from the close of the bar at which the stage is recognisable.
Direction convention: sg = +1 for a level above (high side; 'reversal' = down), -1 for a level below.
"""
import numpy as np, pandas as pd, sys

BARS = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/research/bars5.pkl"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/research/"
P = dict(tol=0.25, rearm=6, strong_range=1.5, strong_body=0.5, small_body=0.5, exp_range=1.5, exp_body=0.5,
         confirm_within=3, retest_within=12, away=3.0, horizons=(3, 6, 12, 24, 48), mfe_h=24)
TYPES = ["Asia", "London", "NewYork", "Day", "Week", "Month"]

b = pd.read_pickle(BARS)
o, h, l, c = (b[x].values for x in ["open", "high", "low", "close"])
mr = b["mr"].values; mv = b["mvol"].values; vol = b["tick_volume"].values.astype(float)
t = b.index.values; n = len(b)
rng = h - l; body = np.abs(c - o)
tday = b["tday"].values; sess = b["session"].values; ukh = b["uk_hour"].values; spread = b["spread_pts"].values

def fwd(i, sg, ref):
    """reversal-positive forward moves in mr units from close of bar i, and MFE/MAE over P['mfe_h'] bars."""
    out = {}
    for k in P["horizons"]:
        j = i + k
        out[f"r{k}"] = (-sg * (c[j] - ref) / mr[i]) if j < n else np.nan
    seg_h = h[i + 1:i + 1 + P["mfe_h"]]; seg_l = l[i + 1:i + 1 + P["mfe_h"]]
    if len(seg_h) == P["mfe_h"]:
        if sg > 0:
            out["mfe"] = (ref - seg_l.min()) / mr[i]; out["mae"] = (seg_h.max() - ref) / mr[i]
        else:
            out["mfe"] = (seg_h.max() - ref) / mr[i]; out["mae"] = (ref - seg_l.min()) / mr[i]
    else:
        out["mfe"] = out["mae"] = np.nan
    return out

lev = {}
for T in TYPES:
    for s, sg in (("H", 1), ("L", -1)):
        lev[(T, s)] = (b[f"{T}_{s}"].values, b[f"{T}_avail"].values, sg)

# ---------- touches ----------
rows = []
for (T, s), (L, av, sg) in lev.items():
    tol = P["tol"] * mr
    near = sg * (np.where(sg > 0, h, l) - L) >= -tol            # bar reached the zone [L - tol, ...) from the near side
    inst = pd.Series(av).astype("int64").values                  # level instance id = availability time
    cnt = {}
    for i in np.where(near)[0]:
        if i < 60 or np.isnan(L[i]) or np.isnan(mr[i]) or i + 48 >= n:
            continue
        lo_ = i - P["rearm"]
        prev = sg * (np.where(sg > 0, h[lo_:i], l[lo_:i]) - L[i]) < -tol[i]
        if not prev.all():                                      # need P['rearm'] bars outside the zone first
            continue
        if inst[lo_] != inst[i]:                                # level instance must exist through the approach
            continue
        key = inst[i]; cnt[key] = cnt.get(key, 0) + 1
        ext = h[i] if sg > 0 else l[i]
        r = rng[i] if rng[i] > 0 else np.nan
        toward_wick = (h[i] - max(o[i], c[i])) if sg > 0 else (min(o[i], c[i]) - l[i])
        close_loc = ((c[i] - l[i]) / r) if sg > 0 else ((h[i] - c[i]) / r)    # 1 = closed at the level-side extreme
        run = 0
        for j in range(i - 1, i - 13, -1):
            if sg * (c[j] - o[j]) > 0: run += 1
            else: break
        others = 0
        for (T2, s2), (L2, _, _) in lev.items():
            if (T2, s2) != (T, s) and not np.isnan(L2[i]) and abs(L2[i] - L[i]) <= mr[i]:
                others += 1
        d = dict(kind="touch", level=T, side=s, sg=sg, i=i, time=t[i], tday=tday[i], session=sess[i], uk_hour=ukh[i],
                 L=L[i], mr=mr[i], level_age_h=(t[i] - av[i]) / np.timedelta64(1, "h"), touch_no=cnt[key],
                 confluence=others,
                 appr6=sg * (c[i - 1] - c[i - 7]) / mr[i], appr24=sg * (c[i - 1] - c[i - 25]) / mr[i],
                 appr_run=run, appr_maxbar=rng[i - 6:i].max() / mr[i], compress6=rng[i - 6:i].mean() / mr[i],
                 htf48=sg * (c[i - 1] - c[i - 49]) / mr[i],
                 t_range=rng[i] / mr[i], t_body=body[i] / r if r == r else np.nan, t_dir=np.sign(c[i] - o[i]) * sg,
                 t_close_loc=close_loc, t_wick=toward_wick / r if r == r else np.nan,
                 pen=sg * (ext - L[i]) / mr[i], close_beyond=int(sg * (c[i] - L[i]) > 0),
                 t_vol=vol[i] / mv[i] if mv[i] > 0 else np.nan, spread=spread[i])
        d.update(fwd(i, sg, c[i]))
        # did price close beyond the level by 1 mr within 24 bars (acceptance / break) ?
        seg = sg * (c[i + 1:i + 25] - L[i]) / mr[i]
        d["broke_1mr_24"] = int((seg > 1).any())
        rows.append(d)
touches = pd.DataFrame(rows)
touches.to_pickle(OUT + "touches.pkl")
print("touches", len(touches))

# ---------- sequences (user's pattern and mirror) ----------
seq = []
Hside = [(T, "H") for T in TYPES]; Lside = [(T, "L") for T in TYPES]
for sg, sides in ((1, Hside), (-1, Lside)):
    # B1 strong toward the level side (bullish for sg=+1), B2 opposite colour with small body
    k = np.arange(2, n - 60)
    b1 = k - 1
    strong = (sg * (c[b1] - o[b1]) > 0) & (body[b1] >= P["strong_body"] * rng[b1]) & (rng[b1] >= P["strong_range"] * mr[b1])
    opp = sg * (c[k] - o[k]) < 0
    small = body[k] <= P["small_body"] * body[b1]
    cand = k[strong & opp & small & ~np.isnan(mr[k])]
    for kk in cand:
        k1 = kk - 1
        ri = (h[kk] <= h[k1]) and (l[kk] >= l[k1])
        bi = (max(o[kk], c[kk]) <= max(o[k1], c[k1])) and (min(o[kk], c[kk]) >= min(o[k1], c[k1]))
        ctype = "range_inside" if ri else ("body_inside_only" if bi else "not_contained")
        ext = max(h[kk], h[k1]) if sg > 0 else min(l[kk], l[k1])
        tol = P["tol"] * mr[kk]
        at, sweep, near_levels, mind = [], False, [], np.inf
        for (T, s) in sides:
            L = lev[(T, s)][0][kk]
            if np.isnan(L):
                continue
            d_ = sg * (ext - L)
            mind = min(mind, abs(ext - L) / mr[kk])
            if d_ >= -tol and sg * (c[kk - 2] - L) < -tol:          # reached the level, approached from the near side
                at.append(T); sweep = sweep or d_ > 0
        any_lvl = min([abs(ext - lev[x][0][kk]) / mr[kk] for x in lev if not np.isnan(lev[x][0][kk])] or [np.inf])
        loc = "at_level" if at else ("away" if any_lvl >= P["away"] else "near_not_tested")
        d = dict(kind="seq", sg=sg, i=kk, time=t[kk], tday=tday[kk], session=sess[kk], uk_hour=ukh[kk], mr=mr[kk],
                 ctype=ctype, location=loc, levels="+".join(at), sweep=int(sweep), ext=ext,
                 b1_range=rng[k1] / mr[kk], b2_range=rng[kk] / mr[kk], b2_body_ratio=body[kk] / max(body[k1], 1e-9),
                 appr6=sg * (c[kk - 2] - c[kk - 8]) / mr[kk], htf48=sg * (c[kk - 2] - c[kk - 50]) / mr[kk],
                 b2_vol=vol[kk] / mv[kk] if mv[kk] > 0 else np.nan, b1_vol=vol[k1] / mv[k1] if mv[k1] > 0 else np.nan,
                 spread=spread[kk])
        st1 = fwd(kk, sg, c[kk]); d.update({f"s1_{a}": v for a, v in st1.items()})
        # stage 2: opposing expansion within confirm_within bars, before any close beyond the sequence extreme
        j2 = None
        for j in range(kk + 1, kk + 1 + P["confirm_within"]):
            if sg * (c[j] - ext) > 0:
                break
            if (sg * (c[j] - o[j]) < 0) and body[j] >= P["exp_body"] * rng[j] and rng[j] >= P["exp_range"] * mr[kk] \
                    and sg * (c[j] - (l[kk] if sg > 0 else h[kk])) < 0:
                j2 = j; break
        d["s2"] = j2 is not None
        d["s2_lag"] = (j2 - kk) if j2 else np.nan
        if j2:
            d["s2_already"] = -sg * (c[j2] - c[kk]) / mr[kk]          # move already made by recognition (mr units)
            st2 = fwd(j2, sg, c[j2]); d.update({f"s2_{a}": v for a, v in st2.items()})
            mid = (o[j2] + c[j2]) / 2; j3 = None; failed = False
            for m in range(j2 + 1, j2 + 1 + P["retest_within"]):
                if sg * (c[m] - ext) > 0:
                    failed = True; break
                if sg * ((h[m] if sg > 0 else l[m]) - mid) >= 0 and sg * (c[m] - mid) < 0:
                    j3 = m; break
            d["s3"] = j3 is not None; d["s3_failed_before"] = failed
            if j3:
                d["s3_lag"] = j3 - j2
                st3 = fwd(j3, sg, c[j3]); d.update({f"s3_{a}": v for a, v in st3.items()})
        seq.append(d)
seqs = pd.DataFrame(seq)
seqs.to_pickle(OUT + "sequences.pkl")
print("sequence candidates", len(seqs)); print(seqs.groupby(["sg", "location", "ctype"]).size())
