"""DEV-only catalogue: base rates, univariate feature relationships and the user's sequence vs baselines.
All CIs are 95% bootstrap intervals with trading days as clusters (events on the same day resampled together)."""
import numpy as np, pandas as pd, sys
R = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/research/"
rng = np.random.default_rng(7)

def boot(df, col, B=2000):
    g = df.groupby("tday")[col].agg(["sum", "count"]).values
    if len(g) < 5: return (np.nan, np.nan)
    idx = rng.integers(0, len(g), (B, len(g)))
    s = g[idx, 0].sum(1) / g[idx, 1].sum(1)
    return tuple(np.percentile(s, [2.5, 97.5]))

def summ(df, label, cols=("r6", "r12", "r24"), pre=""):
    out = {"group": label, "n": len(df), "days": df.tday.nunique()}
    for cname in cols:
        cc = pre + cname
        d = df.dropna(subset=[cc])
        out[cname] = d[cc].mean(); lo, hi = boot(d, cc); out[cname + "_ci"] = f"{lo:.2f}..{hi:.2f}"
    if pre + "mfe" in df:
        d = df.dropna(subset=[pre + "mfe"])
        out["p_mfe2"] = (d[pre + "mfe"] >= 2).mean(); out["p_mae2"] = (d[pre + "mae"] >= 2).mean()
    return out

tch = pd.read_pickle(R + "touches_DEV.pkl"); sq = pd.read_pickle(R + "sequences_DEV.pkl")
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
print("=== DEV touches:", len(tch), "days", tch.tday.nunique())
print(pd.DataFrame([summ(tch, "all touches")] + [summ(g, f"{k}") for k, g in tch.groupby("level")] +
                   [summ(g, f"side {k}") for k, g in tch.groupby("side")]).round(3).to_string())
print("\nby session of touch"); print(pd.DataFrame([summ(g, k) for k, g in tch.groupby("session")]).round(3).to_string())

feats = ["appr6", "appr24", "appr_run", "appr_maxbar", "compress6", "htf48", "t_range", "t_body", "t_close_loc",
         "t_wick", "pen", "t_vol", "level_age_h", "touch_no", "confluence"]
rows = []
for f in feats:
    d = tch.dropna(subset=[f, "r12"]).copy()
    try:
        d["q"] = pd.qcut(d[f].rank(method="first"), 5, labels=False)
    except ValueError:
        continue
    q1, q5 = d[d.q == 0], d[d.q == 4]
    diff = q5.r12.mean() - q1.r12.mean()
    # bootstrap the Q5-Q1 difference by day (vectorised: per-day sums/counts for Q1 and Q5)
    agg = d.assign(a1=(d.q == 0) * d.r12, n1=(d.q == 0) * 1, a5=(d.q == 4) * d.r12, n5=(d.q == 4) * 1)\
           .groupby("tday")[["a1", "n1", "a5", "n5"]].sum().values
    ix = rng.integers(0, len(agg), (1000, len(agg))); S = agg[ix].sum(1)
    bs = S[:, 2] / S[:, 3] - S[:, 0] / S[:, 1]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    rows.append(dict(feature=f, q1_edge=d[d.q == 0][f].max(), q5_edge=d[d.q == 4][f].min(),
                     q1_r12=q1.r12.mean(), q3_r12=d[d.q == 2].r12.mean(), q5_r12=q5.r12.mean(), q5_minus_q1=diff,
                     ci=f"{lo:.2f}..{hi:.2f}", q1_broke=q1.broke_1mr_24.mean(), q5_broke=q5.broke_1mr_24.mean()))
fr = pd.DataFrame(rows).sort_values("q5_minus_q1", key=abs, ascending=False)
print("\n=== univariate (touch features vs reversal-positive 1h move, mr units)"); print(fr.round(3).to_string())
fr.to_csv(R + "dev_feature_quintiles.csv", index=False)

print("\n=== close_beyond on touch bar"); print(pd.DataFrame([summ(g, f"close_beyond={k}") for k, g in tch.groupby("close_beyond")]).round(3).to_string())
print("\n=== touch number"); print(pd.DataFrame([summ(g, f"touch {k}") for k, g in tch.groupby(tch.touch_no.clip(upper=4))]).round(3).to_string())

print("\n=== USER SEQUENCE (stage 1: after small contained candle closes), DEV")
rows = []
for (sg, loc, ct), g in sq.groupby(["sg", "location", "ctype"]):
    rows.append(summ(g, f"{'bear@high' if sg > 0 else 'bull@low'} {loc} {ct}", pre="s1_"))
print(pd.DataFrame(rows).round(3).to_string())
print("\nsweep vs test (at level only)")
rows = [summ(g, f"{'bear' if sg > 0 else 'bull'} sweep={sw} {ct}", pre="s1_") for (sg, sw, ct), g in
        sq[sq.location == "at_level"].groupby(["sg", "sweep", "ctype"])]
print(pd.DataFrame(rows).round(3).to_string())
print("\n=== stage 2 (after opposing expansion), at level vs away")
s2 = sq[sq.s2 == True]
rows = [summ(g, f"{'bear' if sg > 0 else 'bull'} {loc} {ct}", pre="s2_") | {"already_mr": g.s2_already.mean()} for (sg, loc, ct), g in
        s2.groupby(["sg", "location", "ctype"])]
print(pd.DataFrame(rows).round(3).to_string())
print("\nstage-2 rate:", sq.groupby(["location", "ctype"]).s2.mean().round(3).to_dict())
s3 = sq[sq.get("s3") == True]
print("\n=== stage 3 (retest held), at level vs away")
rows = [summ(g, f"{'bear' if sg > 0 else 'bull'} {loc}", pre="s3_") for (sg, loc), g in s3.groupby(["sg", "location"])]
print(pd.DataFrame(rows).round(3).to_string())
