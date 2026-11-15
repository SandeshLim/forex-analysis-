# Pre-registered hypotheses (registered 2026-11-15, before any test)

## What has been rejected, and what has not

**Rejected (corrected events, identical 5m execution, 0.3 pts cost):**
- *Fade rule:* P1 −0.91 pts/trade (95% CI −2.40..+0.72, n=128), P3 −5.25 (−9.38..−1.51). No period shows a positive expectancy outside noise.
- *Continuation rule:* P1 −2.75 pts/trade (−4.64..−0.96, n=114). Its +7.64 on P3 is the design sample.
- *Early-footprint filter (V/R/A/C in the 3 bars before a break) as a quality filter for continuation:* P1 −7.00 pts/trade filtered vs −2.75 unfiltered; filtered CI excludes zero on the negative side.

**Not rejected, because never tested:** session-level breaks as context with any *other* entry, stop, target or holding rule; acceptance (several closes beyond) instead of one close; volatility-scaled stops; timing filters around scheduled data; footprints used as a fade signal rather than a continuation filter; any other instrument; any period outside 2026-08-03..11-13.

## Data plan

| Role | Period | Status |
|---|---|---|
| Development (DEV) | P1 2026-08-03..10-23 | seen; may be used to fit the hypotheses below |
| Validation (VAL) | P2+P3 2026-10-26..11-13 | seen; used once per hypothesis after DEV, no re-tuning |
| **Final holdout (FINAL)** | **2026-11-16 .. 2027-02-26** (15 weeks, forward) | **untouched**; nothing may be computed on it until every hypothesis below is frozen |

There is no untouched history: TradingView limits 5m bars to about 14 weeks back, and all of it has been seen. FINAL is therefore forward data. Because 5m history only reaches ~14 weeks back (1m ~3 weeks), FINAL bars must be exported and hashed **every two weeks**; exports are stored privately and not opened for analysis until the evaluation date.

## Rules for every hypothesis

1. Base event set = corrected definition, point-in-time flags (engine v2.0.0), 0.3 pts cost, stop before target in a tied bar.
2. At most **2 parameter variants per hypothesis** on DEV, each appended to `VARIANT_LOG.md` before it is run.
3. The chosen variant is run **once** on VAL and frozen (config hash recorded) regardless of the VAL result.
4. FINAL decision rule (per hypothesis): pass only if expectancy in R is > 0 with the 95% linked-cluster bootstrap lower bound > 0, **and** expectancy in points stays > 0 when cost is raised to 0.6 pts. With 3 hypotheses, a pass at this bar is still reported with a note that 3 tests were made.
5. Report every hypothesis's FINAL result, passed or failed.

## Hypotheses

### H1 — Acceptance continuation
- **Rationale:** in P1, 133 of 178 corrected events closed back inside within 3 bars, and the one-close continuation rule lost. A break whose first two 5m bars both close beyond the level has shown acceptance rather than a probe, so the follow-through may be different from that of all breaks.
- **Rule:** enter at the close of the 2nd consecutive 5m bar closing beyond the level (the break bar may be the 1st). Stop = level −/+ 1× point-in-time median range. Target 1.5R. Time exit 60 min.
- **Variants allowed on DEV:** stop multiplier 1.0 or 1.5.

### H2 — Volatility-scaled risk for both directions
- **Rationale:** in the rejected rules, risk came from single-candle extremes (median 5–8 pts, but up to 37 pts on row 22), so R outcomes were dominated by stop placement noise. Scaling stop and target to recent volatility separates the direction question from stop placement.
- **Rule:** same entry triggers as the rejected cont and fade rules; stop = 2× point-in-time median 5m range from entry; target 1.5R; time exit 60 min.
- **Variants allowed on DEV:** stop multiplier 1.5 or 2.5.

### H3 — Scheduled-data exclusion
- **Rationale:** the largest outcomes in P3 (rows 2, 3, 22, 28) were breaks at 13:10–13:35 UK, around 08:30 New York data releases, where the 0.3 pt cost and perfect stop fills are least realistic. Results that survive without those windows are more likely to be tradeable.
- **Rule:** apply H1 and H2 with every break whose break bar opens 13:20–13:45 UK or 15:00–15:10 UK excluded, on every weekday (the usual 08:30 and 10:00 New York release times; no calendar is used, so quiet days are excluded too). Reported as a robustness condition on H1/H2, not a separate edge.
- **Variants allowed on DEV:** none.

Footprint flags may be reported as descriptors on H1–H3 trades. They are not a filter in any hypothesis, because the only test of them so far (#8, #9) went the wrong way.
