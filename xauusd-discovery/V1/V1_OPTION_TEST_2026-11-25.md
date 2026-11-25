# V1 entry/stop option test (exploratory), run 25 Nov 2026 ~22:15 UK
Data: OANDA:XAUUSD 1m from the live chart (1–25 Nov) plus Bar Replay windows (~20–26k bars each) covering 31 May – 25 Nov 2026 (small gaps: 19 Jun 17:00–21 Jun, weekends). Costs 0.4 points per trade. Stop assumed first if hit in the same minute as the target. Time-out 4 h.

Detector (fixed before the option results were read; adjusted once so the 25 Nov origin example is detected):
- V recovery: a 1H candle makes a new 24 h low; within 8 h (and before a lower low) a 15m candle closes above that 1H candle's high.
- Within 4 h after that: two consecutive 1m shooting stars (upper wick >= 50 % of range, body <= 35 %).
- Strong candle within 6 minutes: bullish, body >= the range height, close above the range high. Range = first shooting star to the candle before the strong candle.

Options:
1. Buy limit at the shooting-star range midpoint, placed when the 2nd shooting star closes (no strong candle required yet), valid 15 min; stop range low − 0.5.
2. After the strong candle, buy limit at range top + 0.5 within 15 min; stop range low − 0.5.
3. Same fill as 2; stop 0.5 below the fill candle's low.

Results (one trade per V event):
| Option | Trades | Win % (2R) | Total R (2R) | Avg R | Worst losing run | Max drawdown | Total R (3R target) |
|---|---|---|---|---|---|---|---|
| 1 (honest: no knowledge of a later strong candle) | 93 | 16 % | −72.7 | −0.78 | 16 | −72.7 | −65.7 |
| 2 | 35 | 46 % | +7.9 | +0.23 | 5 | −7.7 | +7.9 |
| 3 | 35 | 43 % | −2.9 | −0.08 | 7 | −10.8 | +4.1 |

Note: a first run of option 1 that only counted setups where the strong candle later appeared showed 81 % wins / +49 R. That used future information (the limit fills before the strong candle exists) and is invalid.
Option 2's edge is not statistically established: 35 trades, average +0.23 R with a standard error of roughly ±0.24 R.
25 Nov 17:31 (origin example): option 2 entry 3501.03, stop 3495.79 → +1.92 R at 2R.
