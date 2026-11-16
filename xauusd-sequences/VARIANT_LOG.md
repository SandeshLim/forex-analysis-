# Study 2 variant log (append only)

Entries are written **before** the run they describe.

## 2026-11-16 00:20 — catalogue (DEV only) — done
- `src/catalogue_dev.py`: 12,995 level touches and 15,544 sequence candidates in DEV (2017-05..2021-12). Univariate quintiles of 15 touch features; the user's sequence by direction × location × containment type × stage; sweep vs test; daily-trend alignment (close vs 20-day SMA of previous days).
- That is roughly 80 cells looked at. At 95% intervals, about 4 would exclude zero by chance alone. Every DEV pattern below is a lead, not a finding.

## 2026-11-16 00:30 — formal candidates frozen for DEV variant runs (≤ 4 candidates × ≤ 3 variants)
Common execution: signals on 5m bars (Exness), entry at the close of the recognition bar, exits simulated on 1m bars, stop checked before target in the same minute, cost = bar spread + 0.1 slippage per side, P&L in R = net points / initial risk. Daily trend = sign(previous trading-day close − 20-day SMA of previous closes).

| ID | Candidate | Rationale from DEV catalogue | Variants (all run on DEV) |
|---|---|---|---|
| C1 | User's sequence and mirror **at a level**, contained B2 (range-inside or body-inside), both directions. Stop = sequence extreme + 0.1 mr. Target 2R, time exit 24 bars (2h). | Direct test of the user's hypothesis and recognition time | V1 entry at B2 close (stage 1); V2 entry at expansion close (stage 2); V3 entry at held retest (stage 3) |
| C2 | C1 stage 2, **only when the reversal direction agrees with the daily trend** | DEV asymmetry: bullish-at-lows in uptrends +0.64 mr at 1h (CI −0.04..1.38); bearish-at-highs failed | V1 target 1R; V2 target 2R; V3 target 3R (time exit 24 bars) |
| C3 | **Overshoot reversion**: a touch bar that trades ≥ p mr beyond a completed level; fade at that bar's close. Stop = bar extreme + 0.5 mr. Time exit 12 bars (1h), no target. | Strongest univariate DEV feature (penetration Q5−Q1 +0.47 mr at 1h, CI 0.10..0.84) | V1 p=1.0; V2 p=1.3; V3 p=1.6 |
| C4 | **Late-session touch fade** (touch bar opens 17:00–24:00 UK); fade at touch-bar close; stop = bar extreme + 0.5 mr; time exit 12 bars | Late touches r12 +0.22 (CI 0.04..0.39); aligned with daily trend +0.37 (0.04..0.69) | V1 all late touches; V2 trend-aligned only; V3 trend-aligned and touch bar closed back inside the level |

Selection rule for VAL: the variant with the highest DEV expectancy in R for each candidate, unless it has fewer than 100 DEV trades, in which case the next one.

## 2026-11-16 00:55 — bug fix in `src/sim.py` before any selection
The first DEV run applied entry slippage in the trader's favour and charged shorts the spread twice. Now modelled explicitly: longs buy at the ask (bid + spread + 0.1) and sell at the bid, shorts sell at bid − 0.1 and buy back at the ask; stops pay another 0.1. All 12 DEV variants are re-run; the first run's numbers are void and were not used to choose anything.

## 2026-11-16 01:05 — DEV results (after fix) and selection for VAL
All 12 DEV variants have negative expectancy after costs; 11 of 12 have 95% CIs entirely below zero. Best per candidate (rule: highest DEV expR with n ≥ 100): **C1V2** (−0.182R), **C2V3** (−0.125R, CI −0.265..+0.019), **C3V2** (−0.321R), **C4V1** (−0.378R). As pre-committed, each is run once on VAL and once on TEST regardless.

## 2026-11-16 01:12 — VAL (run once) and TEST unsealed
VAL expR: C1V2 −0.138 (CI −0.287..+0.017, n 209), C2V3 −0.132 (−0.383..+0.131, n 87), C3V2 −0.151 (−0.300..+0.005, n 652), C4V1 −0.285 (−0.379..−0.185, n 854). No changes made. TEST files (sha256 75403ad5…, ee6c92c3…) opened now for the single pre-committed run.

## 2026-11-16 01:20 — TEST (run once) — study closed
TEST expR: C1V2 −0.182 (−0.310..−0.055, n 254), C2V3 −0.179 (−0.360..+0.023, n 113), C3V2 −0.176 (−0.312..−0.032, n 724), C4V1 −0.128 (−0.232..−0.028, n 1,216). None passes. Per the stopping rule, no further variants are run on 2017–2026 data. Post-TEST descriptive checks (year-by-year sign, trap rates, post-trap moves) are reported as leads only.

## 2026-11-16 00:35 — post-TEST completeness runs (requested; not a selection step)
The report's opening claim ("lost money at every recognition stage") rested on TEST results for stage 2 only; stages 1 and 3 had DEV results only. C1V1 (entry at B2 close) and C1V3 (entry at held retest) are now run on VAL and TEST, unchanged, to complete the table. TEST is already spent, so these runs are descriptive confirmation, not out-of-sample selection.

## 2026-11-16 00:50 — corrections after review
- C1V1 and C1V3 were run on VAL and TEST (see the 00:35 entry). Report narrowed: all three stages negative on TEST; the retest stage is ≈ 0 on VAL.
- Screenshot dates corrected: captures from 15 Nov; four show 13 Nov, one shows a Bar Replay of 12 Nov.
- Drawn trades re-analysed with executable entries and targets defined before entry (`results/drawn_trades.md`).
- Dataset verification (`results/dataset_verification.md`).
- The coverage matrix (`COVERAGE.md`) and the study 3 plan (`../xauusd-discovery/PLAN.md`) were added.
