# Implementation audit (2026-11-15)

## 1. Reproduction
- `engine/legacy/engine_v1_original.fn.js` is the exact function that produced the first results (SHA-256 `cb61032b…67da89`, matched against the copy running in the browser). `stats_v1_original.fn.js` likewise (`a392fb8d…94aa`).
- The "corrected" v1 run differed only by `TT=T.filter(x=>x.tested&&!(opt.excludeOff&&x.offCross))`.
- `engine/engine_v2.js` (SHA-256 `a5334b91…3da7`) was loaded into the chart page and its `toString()` hash matched the file before any run.
- v2 in legacy mode (`excludeOff:false, flagMode:'legacy'`) reproduces v1 exactly: P3 cont 20 trades +5.52, fade 19 trades −5.42, cont-early 11 trades +8.47 (1m exits); P1 cont 145 −2.19, cont-early 54 −5.28, fade 145 −0.91, fade-early 55 −0.42 (5m exits).
- `analysis/decode_and_report.py` recomputes every statistic from the logs alone (including the same seeded bootstrap) and matches the engine (two figures differ by ±0.01 from rounding of x.xx5 values).

## 2. Look-ahead in footprint flags — FOUND and fixed
- **v1 defect:** V/R/A on each of the 3 pre-break candles were judged against the median range/volume of the 24 bars before the **break** candle. For the candle at −15 min that baseline includes the −10 and −5 candles, i.e. up to 10 minutes of information not available when that candle closed. The flag on the −5 candle used a baseline that included itself.
- **v2:** `pitFlags` judges every candle against the 24 bars strictly before it, so each flag is identifiable at that candle's close (`visibleAt`). Compression (C) and break-candle flags already used only pre-break bars and were unchanged.
- **Flag vs label:** a *flag* is a property of one candle, knowable at its close. The *early-footprint label* ("a flag on one of the 3 candles before a break") can only be assigned once the break happens, i.e. at the break candle's open at the earliest. It is usable for a trade entered at or after the break; it is not a forecast of the break.
- **Effect:** v1 baselines were inflated by the later, larger pre-break candles, so v1 was *stricter*: point-in-time flags add early labels and remove none (original events: P1 84→95, P2 3→5, P3 16→19). The look-ahead did not flatter the earlier results; it mislabelled 16 of 262 events.

## 3. Row 6 timing
- The 12:15 bar is the candle 12:15:00–12:19:59. The first written evidence and the first image both said it was flagged V+R and "visible 12:20"; the image placed that label above the gap between the 12:15 and 12:20 candles, which made it readable as belonging to the 12:20 break candle.
- The substantive error was different: the "visible at" times were stated as if the flags were knowable then, but under the v1 baseline they were not (see §2). Under point-in-time baselines: 12:10 candle = **V+R** (v1 said V only: range 5.91 vs v1 threshold 5.92 but PIT threshold 5.73), visible 12:15; 12:15 candle = **V+R**, visible 12:20; 12:20 break candle V+R (break baseline).
- `evidence/rows_2_6_10_22_28_pit.png` now uses point-in-time baselines, draws each label on a leader line to its own candle, states the open/close convention, and shows the legacy flag wherever it differs.

## 4. Event definition — corrected definition is primary
- 44 of 262 original events (P1 38, P2 5, P3 6) were levels that price had already traded beyond between the session end and the in-session "break" (mostly 17:00–24:00 UK). Their recorded break time was not the first break. The corrected definition removes them; linked groups are re-formed after removal.
- Linked events: same side broken on the same 5m candle → one trade on the outermost level; bootstrap clusters on these groups (and separately on UK day).
- Completeness: every level appears in `logs/levels.csv` as tested / untested / censored (fewer than two later sessions inside the window).

## 5. Execution assumptions
- Identical across P1–P3: 5m bars for signals and exits, entry at signal-bar close, stop checked before target within a bar, 60-min time exit, 0.3 pts round-trip, stops filled at the stop price.
- 1m refinement (P2, P3 only): 0 of 21 and 1 of 32 trades changed exit label; no change in P&L. Finer data would mainly help stop/target ordering and realistic fills, not the signal.
- Not modelled: spread widening and stop slippage at 13:30 UK data releases (e.g. row 22, a 41-point candle). Treat results near releases as optimistic.
