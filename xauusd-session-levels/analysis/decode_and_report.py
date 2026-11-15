#!/usr/bin/env python3
"""Expand the compact export from engine_v2.js into CSV logs and recompute every summary statistic.

Usage: python3 decode_and_report.py ../data/export_compact.txt ../
Writes logs/events.csv, logs/trades.csv, logs/levels.csv and results/summary.csv, results/summary.md.
The statistics are recomputed here independently of the browser engine; they must match the engine's output.
"""
import csv, datetime as dt, hashlib, math, os, sys

CFG = dict(rr=1.5, cost=0.3, t0=1785000000, boot_n=5000, seed=12345,
           bst=(int(dt.datetime(2026, 3, 29, 1, tzinfo=dt.timezone.utc).timestamp()),
                int(dt.datetime(2026, 10, 25, 1, tzinfo=dt.timezone.utc).timestamp())))
PERIODS = {"1": "P1 2026-08-03..2026-10-23", "2": "P2 2026-10-26..2026-10-30", "3": "P3 2026-11-02..2026-11-13"}
SESS = {"A": "Asia", "L": "London", "N": "New York"}
REASON = {"T": "target", "S": "stop", "X": "stop(tie)", "M": "time"}


def uk_off(t):
    return 3600 if CFG["bst"][0] <= t < CFG["bst"][1] else 0


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def decode(text):
    _, ev_s, _, tr_s, _, lv_s = text.split("~")
    events = []
    for i, row in enumerate(ev_s.split(";")):
        f = row.split(",")
        (per, code, lvl, tq, off, over, rev, r30, r60, trend, mr, mv, comp, wick, bflags, pit, leg, lp) = f
        t = CFG["t0"] + int(tq) * 300
        side = code[-1]
        pre_pit = pit.split("/"); pre_leg = leg.split("/")
        early_pit = any(pre_pit) or comp == "1"; early_leg = any(pre_leg) or comp == "1"
        events.append(dict(idx=i, period=PERIODS[per], period_code="P" + per,
            level=f"2026-{code[0:2]}-{code[2:4]} {SESS[code[4]]} {'high' if side == 'H' else 'low'}",
            side=side, level_price=float(lvl), break_bar_open_utc=iso(t), t=t,
            break_uk_date=dt.datetime.fromtimestamp(t + uk_off(t), dt.timezone.utc).strftime("%Y-%m-%d"),
            crossed_outside_sessions_first=int(off), overshoot_pts=float(over), closed_back_inside_3=int(rev),
            r30_pts=float(r30), r60_pts=float(r60), trend_4h=trend, base_median_range=float(mr), base_median_vol=int(mv),
            compression=int(comp), wick_W=int(wick), break_candle_flags=bflags,
            pre_flags_pit_m15_m10_m5=pit, pre_flags_legacy_m15_m10_m5=leg,
            early_pit=int(early_pit), early_legacy=int(early_leg),
            linked_original=int(lp[0]), primary_original=int(lp[1]),
            in_corrected=int(len(lp) == 4), linked_corrected=int(lp[2]) if len(lp) == 4 else "",
            primary_corrected=int(lp[3]) if len(lp) == 4 else "",
            group=f"P{per}|{t}|{side}"))
    c5 = {}
    trades = []
    for row in tr_s.split(";"):
        f = row.split(",")
        code, ev, rule = f[0], int(f[1]), f[2]
        if f[3] == "=":
            base = dict(c5[(ev, rule)]); base["variant"] = code
            trades.append(base); continue
        e = events[ev]
        ent_off, entry, stop, ex_off, rs = int(f[3]), float(f[4]), float(f[5]), f[6], f[7]
        sg = 1 if e["side"] == "H" else -1
        d = sg if rule == "c" else -sg
        risk = abs(entry - stop)
        target = entry + d * CFG["rr"] * risk
        t_entry = e["t"] + ent_off * 60
        reason = REASON[rs[0]]
        exit_px = target if rs[0] == "T" else stop if rs[0] in "SX" else float(rs[1:])
        gross = d * (exit_px - entry); net = gross - CFG["cost"]
        tr = dict(variant=code, event_idx=ev, period_code=e["period_code"], rule="cont" if rule == "c" else "fade",
                  early_pit=e["early_pit"], early_legacy=e["early_legacy"],
                  crossed_outside_sessions_first=e["crossed_outside_sessions_first"],
                  group=e["group"], day=e["break_uk_date"], level=e["level"], side=e["side"],
                  entry_utc=iso(t_entry), t_entry=t_entry, entry=entry, stop=round(stop, 3), target=round(target, 3),
                  risk_pts=round(risk, 3), exit_bar_open_utc=iso(t_entry + int(ex_off) * 60) if ex_off else "",
                  exit=round(exit_px, 3), reason=reason, gross_pts=round(gross, 4), cost_pts=CFG["cost"],
                  net_pts=round(net, 4), R=round(net / risk, 4), gross_R=round(gross / risk, 4), cost_R=round(CFG["cost"] / risk, 4))
        trades.append(tr)
        if code == "c":
            c5[(ev, rule)] = tr
    levels = []
    for row in lv_s.split(";"):
        per, code, lvl, st = row.split(",")
        levels.append(dict(period=PERIODS[per], period_code="P" + per,
            level=f"2026-{code[0:2]}-{code[2:4]} {SESS[code[4]]} {'high' if code[5] == 'H' else 'low'}",
            level_price=float(lvl), status={"t": "tested", "u": "untested", "c": "censored"}[st[0]],
            crossed_outside_sessions_first=int(st[1])))
    return events, trades, levels


def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF
    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = imul(t ^ (t >> 15), t | 1)
        t = (t ^ ((t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


def boot_ci(trades, field, key):
    if len(trades) < 2:
        return (None, None)
    cl = {}
    for t in trades:
        cl.setdefault(t[key], []).append(t[field])
    keys = list(cl.keys()); r = mulberry32(CFG["seed"]); means = []
    for _ in range(CFG["boot_n"]):
        s = n = 0
        for _ in range(len(keys)):
            g = cl[keys[math.floor(r() * len(keys))]]
            s += sum(g); n += len(g)
        means.append(s / n)
    means.sort()
    return (means[math.floor(0.025 * CFG["boot_n"])], means[math.floor(0.975 * CFG["boot_n"]) - 1])


def max_dd(seq):
    peak = cum = dd = 0.0
    for x in seq:
        cum += x; peak = max(peak, cum); dd = min(dd, cum - peak)
    return dd


def median(a):
    s = sorted(a); return s[len(s) // 2]


def stats(T):
    if not T:
        return dict(n=0)
    s = sorted(T, key=lambda t: t["t_entry"])
    w = [t for t in s if t["net_pts"] > 0]; l = [t for t in s if t["net_pts"] <= 0]
    m = lambda a, f: sum(t[f] for t in a) / len(a)
    r2 = lambda x: None if x is None else round(x, 2)
    g = boot_ci(s, "net_pts", "group"); d = boot_ci(s, "net_pts", "day"); gr = boot_ci(s, "R", "group")
    return dict(n=len(s), win_rate=round(len(w) / len(s), 3),
        avg_win_pts=r2(m(w, "net_pts")) if w else None, avg_loss_pts=r2(m(l, "net_pts")) if l else None,
        exp_pts=r2(m(s, "net_pts")), exp_R=r2(m(s, "R")), avg_cost_R=r2(m(s, "cost_R")),
        median_risk_pts=r2(median([t["risk_pts"] for t in s])),
        total_pts=r2(sum(t["net_pts"] for t in s)), total_R=r2(sum(t["R"] for t in s)),
        max_dd_pts=r2(max_dd([t["net_pts"] for t in s])), max_dd_R=r2(max_dd([t["R"] for t in s])),
        ci95_pts_linked=f"{r2(g[0])}..{r2(g[1])}", ci95_pts_day=f"{r2(d[0])}..{r2(d[1])}", ci95_R_linked=f"{r2(gr[0])}..{r2(gr[1])}")


def main():
    src, out = sys.argv[1], sys.argv[2]
    text = open(src).read().rstrip("\n")
    print("export sha256", hashlib.sha256(text.encode()).hexdigest())
    events, trades, levels = decode(text)
    os.makedirs(os.path.join(out, "logs"), exist_ok=True); os.makedirs(os.path.join(out, "results"), exist_ok=True)
    for name, rows in (("events", events), ("trades", trades), ("levels", levels)):
        rows_out = [{k: v for k, v in r.items() if k not in ("t", "t_entry", "idx")} | ({"event_idx": r["idx"]} if name == "events" else {}) for r in rows]
        with open(os.path.join(out, "logs", f"{name}.csv"), "w", newline="") as fh:
            wri = csv.DictWriter(fh, fieldnames=list(rows_out[0].keys())); wri.writeheader(); wri.writerows(rows_out)
    labels = {"o": "ORIGINAL (all events, legacy flags, 5m exec)", "c": "CORRECTED - PRIMARY (off-session crossings removed, point-in-time flags, 5m exec)",
              "m": "CORRECTED, 1m exits (P2, P3 only)"}
    rows = []
    for var in ("c", "o", "m"):
        for per in ("P1", "P2", "P3"):
            for rule in ("cont", "fade"):
                base = [t for t in trades if t["variant"] == var and t["period_code"] == per and t["rule"] == rule]
                if not base:
                    continue
                eflag = "early_legacy" if var == "o" else "early_pit"
                for sub, f in (("all", lambda t: True), ("FILTERED: early footprint", lambda t: t[eflag] == 1),
                               ("complement: no early footprint", lambda t: t[eflag] == 0)):
                    st = stats([t for t in base if f(t)])
                    rows.append(dict(analysis=labels[var], period=per, rule=rule, subset=sub) | st)
    with open(os.path.join(out, "results", "summary.csv"), "w", newline="") as fh:
        keys = list(rows[0].keys()); wri = csv.DictWriter(fh, fieldnames=keys); wri.writeheader(); wri.writerows(rows)
    ev_rows = []
    for var, key in (("ORIGINAL", None), ("CORRECTED - PRIMARY", "in_corrected")):
        for per in ("P1", "P2", "P3"):
            E = [e for e in events if e["period_code"] == per and (key is None or e[key] == 1)]
            pseudo = [dict(group=e["group"], v=1 if e["r60_pts"] > 0 else 0) for e in E]
            ci = boot_ci(pseudo, "v", "group")
            ev_rows.append(dict(analysis=var, period=per, events=len(E), linked_groups=len({e["group"] for e in E}),
                closed_back_inside_3=sum(e["closed_back_inside_3"] for e in E), back_inside_60=sum(1 for e in E if e["r60_pts"] > 0),
                back_inside_60_ci95=f"{ci[0]:.2f}..{ci[1]:.2f}", avg_r60_pts=round(sum(e["r60_pts"] for e in E) / len(E), 2),
                early_pit=sum(e["early_pit"] for e in E), early_legacy=sum(e["early_legacy"] for e in E),
                early_changed_by_pit=sum(1 for e in E if e["early_pit"] != e["early_legacy"])))
    with open(os.path.join(out, "results", "event_summary.csv"), "w", newline="") as fh:
        wri = csv.DictWriter(fh, fieldnames=list(ev_rows[0].keys())); wri.writeheader(); wri.writerows(ev_rows)
    lv_rows = []
    for per in ("P1", "P2", "P3"):
        L = [l for l in levels if l["period_code"] == per]
        lv_rows.append(dict(period=per, levels=len(L), tested=sum(l["status"] == "tested" for l in L),
            untested=sum(l["status"] == "untested" for l in L), censored=sum(l["status"] == "censored" for l in L),
            crossed_outside_sessions_first=sum(l["crossed_outside_sessions_first"] for l in L)))
    with open(os.path.join(out, "results", "level_summary.csv"), "w", newline="") as fh:
        wri = csv.DictWriter(fh, fieldnames=list(lv_rows[0].keys())); wri.writeheader(); wri.writerows(lv_rows)
    print(f"events {len(events)} trades {len(trades)} levels {len(levels)}")
    for r in rows:
        print(r["analysis"][:9], r["period"], r["rule"], r["subset"][:12], r.get("n"), r.get("exp_pts"), r.get("exp_R"),
              r.get("ci95_pts_linked"), r.get("max_dd_pts"))
    for r in ev_rows:
        print(r)
    for r in lv_rows:
        print(r)


if __name__ == "__main__":
    main()
