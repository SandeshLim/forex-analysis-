# Study 3 — bounded discovery study (plan only; nothing run)
Written 2026-11-16 00:55 UK, before any study-3 computation.

## Scope
The families from the user's examples that study 2 did not test: 1-minute sequences and their mirrors; developing session extremes; earlier 1h/4h candle zones; swing changes with later retests. Study 2's rejection covers only its four 5-minute rule families at completed levels.

## Data roles (fixed now)
| Role | Data | Status |
|---|---|---|
| Exploratory A | Exness 1m 2017-05 → 2021-12 | seen in study 2; exploratory |
| Exploratory B (replication) | Exness 1m 2022-01 → 2026-07 | seen in study 2; exploratory |
| Final, option 1 (preferred) | pre-2017 1m from a second feed supplied by the user (e.g. Dukascopy 2010–2016) | never examined; compatibility check on the 2017 overlap only |
| Final, option 2 | forward 1m from 2026-11-16 (OANDA via TradingView; Exness if available) | exported and hashed every 2 weeks, unopened until evaluation, ≥ 6 months |
The final data set must be chosen before exploratory work starts.

## Families (recognition uses only closed bars; nothing defined by outcome)
- **F1 — 1m sequences and mirrors.**
  - B1 strong: body ≥ 50% of range, range ≥ 1.5 × mr1 (mr1 = median 1m range of the previous 60 bars).
  - B2 opposite, body ≤ 50% of B1's. Containment typed: range-inside / body-inside-only / not-contained, never pooled.
  - B3 expansion within 3 bars; retest stage as in study 2.
  - Context: completed level / developing extreme / F3 zone / away from all.
  - Also an enumeration of 2–4-candle sign and size sequences, with occurrences, candles and distinct days counted.
- **F2 — Developing session extremes.**
  - Standing extreme = the current session high/low unchanged for ≥ m minutes (m ∈ {15, 30, 60}).
  - Event = the first trade beyond it.
  - Measures: penetration, minutes to the first 1m close back inside, time spent beyond.
- **F3 — Earlier 1h/4h candle zones.**
  - Source candle: range ≥ 2 × median of the previous 20 same-timeframe bars, body ≥ 60%. Usable from its close.
  - Zone = body; body-to-wick kept separate.
  - Revisit = the first trade into the zone ≥ 4 h after formation. Visit number, zone age and the excursion since formation are recorded.
- **F4 — Swing changes and retests.**
  - 5m pivots with 3 bars each side, usable at the close of the 3rd confirming bar.
  - Change = a close beyond the last confirmed opposite swing after ≥ 2 swings the other way.
  - Retest = the first return to the broken swing within 1–24 h; responses on later visits are recorded.

## Outcomes and baselines (fixed now)
- MFE/MAE in R and in mr at 15/30/60/240 min.
- First passage to +1R/+2R/+3R before −1R.
- Trap within 30 min.
- Move already made at recognition.
- Executable rules: entry at the recognition close, spread from the data + 0.1 slippage per side, stop checked first within each minute.
- Baselines: the same context without the pattern; the same pattern away from the context; random times matched by session and hour.

## Budget and controls
- ≤ 6 exploratory variants per family (24 in total), each appended to `VARIANT_LOG.md` before it runs.
- ≤ 2 finalists per family (≤ 8), frozen with a config hash and evaluated once on the final data. Holm correction across the finalists.
- Bootstrap intervals clustered by trading day. Events overlapping across families or timeframes deduplicated by time window.
- Example catalogues chosen by fixed rules (first N successes, failures and time exits per family).
- Stop after the final evaluation.
