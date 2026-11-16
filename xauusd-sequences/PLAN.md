# Study 2 — candle sequences at meaningful XAUUSD levels: plan and budget

Written 2026-11-15 23:55 UK, **before** any sequence statistics were computed on the history below.

## Data
- **Primary history:** Exness MT5 `XAUUSDm` 1-minute bars, 2017-04-28 → 2026-08-18 07:16 UTC (3,276,127 bars), from the public repository `sherwynjoel/xauusd-historical-data` (commit c6aa574). Third-party feed; not redistributed here.
- **Reference feed:** TradingView `OANDA:XAUUSD`. Used for coverage audit, compatibility checks and chart inspection only.
- Compatibility (checked before this plan): with no clock shift, OANDA minus Exness 5m closes on 5 Aug 2026 = +0.12 mean, 0.16 SD (275 bars); weekly noon closes 2023–2026 = +0.105 mean (187 checks). A one-bar shift makes the error 15×, so Exness bars are stamped in UTC.

## Chronological splits (Exness)
| Split | Dates | Use |
|---|---|---|
| DEV | 2017-05-01 → 2021-12-31 | catalogue, feature exploration, at most the variants budgeted below |
| VAL | 2022-01-01 → 2023-12-31 | each selected candidate run once, frozen afterwards |
| TEST | 2024-01-01 → 2026-07-31 | untouched until all candidates are frozen; run once |
| (excluded) | 2026-08-01 → | overlaps study 1 data already examined |
| FORWARD | OANDA from 2026-11-16 | the forward holdout registered in study 1 |

## Budget
- Base timeframe 5m (aggregated from 1m); 1m used for execution checks; 15m for one robustness check on finalists.
- Catalogue: one event table of level interactions with ≤ 25 pre-defined features; univariate summaries only (no model search).
- Formal candidates: at most **4**, chosen from the catalogue on DEV; at most **3 parameter variants each** on DEV (12 runs), every one logged in `VARIANT_LOG.md` before running.
- VAL: each candidate once. TEST: each candidate once, whatever VAL showed. No re-tuning after VAL.
- Stopping rule: stop after TEST whether or not anything passes.

## Decision bar for a "validated" finding
On TEST: expectancy in R > 0 with the 95% day-clustered bootstrap lower bound > 0, after costs of spread (from the Exness spread field) + 0.1 pts slippage per side, and still > 0 at double costs; and the sign agrees on VAL. With up to 4 candidates, report Holm-adjusted p-values alongside.
