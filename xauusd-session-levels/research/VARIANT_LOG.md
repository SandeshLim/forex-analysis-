# Variant log

Every rule, filter, definition and descriptive cut that has been run, in order, with the data it touched. Append only: never edit past rows. A period listed here is no longer untouched for anything derived from these results.

| # | When (UK) | Variant | Data touched | Result (net, per trade) | Status |
|---|---|---|---|---|---|
| 1 | 15 Nov 21:30 | Descriptive: 30 tests, 3-candle reversal, +30/+60, 4h trend, session, overshoot, footprint splits | P3 (1m/5m) | 20/30 "reversals", 9 inside at +60 | Descriptive only |
| 2 | 15 Nov 21:35 | **Fade rule** (set before results) | P3 | 19 trades, −5.42 pts | Rejected |
| 3 | 15 Nov 21:36 | **Continuation rule** (designed after #2 failed, same data) | P3 | 20 trades, +5.52 pts | In-sample only |
| 4 | 15 Nov 21:36 | Early-footprint split of #2 and #3 (legacy flags; fade split also counted W) | P3 | cont +8.47 / +1.90; fade −5.31 / −5.54 | — |
| 5 | 15 Nov 21:37 | Trend-aligned / counter-trend split of #2 and #3 | P3 | no consistent effect | Descriptive only |
| 6 | 15 Nov 21:40 | #2 and #3 frozen (quick check) | P2 | cont −1.99, fade +0.41 | — |
| 7 | 15 Nov 22:00 | Off-session crossing check → "corrected" event definition | P3, then P1 | 6 of 30 events affected in P3 | Adopted as primary (bug fix) |
| 8 | 15 Nov 22:05 | #2, #3, early filter, frozen | P1 (5m) | cont −2.19, cont-early −5.28; fade −0.91, fade-early −0.42 | Rejected |
| 9 | 15 Nov 22:05 | Same with corrected events | P1 | cont −2.75, cont-early −6.69 | Rejected |
| 10 | 15 Nov 22:05 | Monthly breakdown of #8 | P1 | cont negative in Aug, Sep, Oct | Descriptive only |
| 11 | 15 Nov 22:40 | Point-in-time footprint flags (look-ahead fix) | P1–P3 | adds 16 early labels, removes 0 | Adopted (bug fix) |
| 12 | 15 Nov 22:45 | Identical 5m execution for all periods; 1m refinement on P2/P3 | P1–P3 | see results/summary.md | Reference implementation |

Observed but **not** adopted (post-hoc, would be data-snooping if pursued on P1–P3):
- P1 corrected continuation *without* an early footprint: +0.12 pts/trade (95% CI −1.82..+2.12).
- P1 corrected fade *with* an early footprint: +0.17 pts/trade (95% CI −2.79..+3.53).
- P3 Asia-session breaks all continued; P1 does not show this strongly.
