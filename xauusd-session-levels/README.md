# XAUUSD session-level break study

Research into what happens when OANDA spot gold trades beyond an earlier Asia / London / New York session high or low (UK time: Asia 00–07, London 07–12, New York 12–17).

**Status (2026-11-15):** the two rules tested so far (fade and one-close continuation, with or without an "early footprint" filter) are **rejected**. This rejects those specific rules, not the research question. New hypotheses are pre-registered in `research/HYPOTHESES.md` with a forward holdout that has not been looked at.

## Layout

| Path | What |
|---|---|
| `engine/engine_v2.js` | Current engine (v2.0.0): sessions, events, point-in-time footprint flags, both rules, stats with R, drawdown, cluster bootstrap. Runs in the TradingView chart page. |
| `engine/legacy/` | The exact v1 functions that produced the first results, hash-verified. |
| `config/config_v2.json` | Every parameter, the event definitions and the execution assumptions. |
| `data/MANIFEST.md` | Data source, extraction date, bar counts, SHA-256 fingerprints. Raw bars are **not** committed (see manifest). |
| `data/browser_extract.js` | How the bars were pulled from the chart. |
| `data/export_compact.txt` | The engine's compact export of all events, trades and levels (SHA-256 in manifest). |
| `analysis/decode_and_report.py` | Expands the export into `logs/*.csv` and recomputes every statistic independently. |
| `analysis/plot_events.py` | Evidence chart for audited rows. |
| `logs/events.csv`, `logs/trades.csv`, `logs/levels.csv` | Every event (original and corrected flags), every trade (variants `c` corrected 5m, `o` original 5m, `m` corrected 1m), every session level with tested/untested/censored status. |
| `results/summary.md` | Primary (corrected) results first, then original, then 1m refinement, event behaviour and level completeness. |
| `research/AUDIT.md` | Look-ahead finding and fix, row 6 timing, event-definition correction, execution assumptions. |
| `research/VARIANT_LOG.md` | Every variant run so far and the data it touched. Append only. |
| `research/HYPOTHESES.md` | What was rejected, what remains untested, three pre-registered hypotheses, data plan and decision rules. |
| `evidence/` | Annotated 5m charts for rows 2, 6, 10, 22, 28 of the first study. |

## Reproduce

1. Open a TradingView chart of `OANDA:XAUUSD`, set the resolution, and run `extractBars()` from `data/browser_extract.js` for 5m, 1m and 240. Check `sha256Rows()` against `data/MANIFEST.md`.
2. Paste `engine/engine_v2.js`, then e.g. `const X = xauResearch(); X.run(bars5m, bars5m, 300, bars4h, [2026,7,3], [2026,9,23], {excludeOff:true, flagMode:'pit', period:'P1'})`. Months are 0-based (JavaScript `Date.UTC`).
3. `python3 analysis/decode_and_report.py data/export_compact.txt .` regenerates `logs/` and `results/` from the committed export.

## Labels used everywhere

- **CORRECTED - PRIMARY**: levels already crossed outside session hours are removed; footprint flags are point-in-time.
- **ORIGINAL**: the definition first reported, with legacy (break-anchored) footprint baselines.
- **FILTERED**: a subset with an early footprint; always shown next to its unfiltered and complement rows.

Candle patterns and tick volume describe activity. They do not identify who traded, and nothing here treats them as proof of institutional participation.
