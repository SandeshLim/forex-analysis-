# Drawn trades (13 Nov 2026) vs executable rules — OANDA 1m bars, bid chart, no spread

Entries are fixed at bar closes. "Worst" = the deepest adverse move before the first exit. Targets were defined without hindsight: fixed R multiples, the next completed level in the trade direction, the developing session low at entry, or time exits.

| Trade | Entry UK | Price | Risk | Worst | 2R | 5R | Next completed level | Developing session low | +60m | +240m |
|---|---|---|---|---|---|---|---|---|---|---|
| A as drawn | 03:38 | 3920.65 | 3.23 | −0.76R | 04:12 | 05:43 | 3852.58 not reached (+11.1R at close) | 3879.26 hit 13:30 (+12.8R) | +3.7R | +8.1R |
| A 1m sequence (B1 03:38, B2 03:39 range-inside, B3 03:40) | 03:41 | 3920.28 | 2.93 | −0.63R | 04:12 | 05:42 | not reached (+12.2R at close) | hit 13:30 (+14.0R) | +3.9R | +7.2R |
| B as drawn | 13:34 | 3903.89 | 2.30 | −0.91R | 13:35 | 13:37 | 3886.58 hit 13:46 (+7.5R) | 3879.25 hit 13:50 (+10.7R) | +4.4R | +9.7R |
| B 1m sequence (B2 close 13:32) | 13:33 | 3896.45 | 1.96 | stopped 13:33 | — | — | — | — | — | — |
| B 5m small-candle close | 13:40 | 3896.99 | 9.32 | −0.03R | 13:50 | not reached | 13:46 (+1.1R) | 13:50 (+1.9R) | +0.2R | +1.2R |
| B 5m expansion close | 13:45 | 3888.47 | 17.84 | −0.64R | not reached | not reached | 13:46 (+0.1R) | 13:50 (+0.5R) | −0.5R | 0.0R |
| C as drawn | 14:45 | 3898.54 | 3.37 | −0.39R | 15:00 | 15:19 | 3886.58 hit 15:08 (+3.5R) | 3872.73 hit 15:38 (+7.7R) | +6.4R | +5.5R |
| C 1m sequence (B2 close 14:37) | 14:38 | 3895.80 | 2.32 | stopped 14:45 | — | — | — | — | — | — |

1m sequence rule: B1 bullish, body ≥ 50% of range, range ≥ 1.5 × median 1m range of the previous 60 bars; B2 bearish with body ≤ 50% of B1's; B3 a bearish expansion within 3 bars closing below B2's low. Stop = sequence extreme + 0.1 × median 1m range.
These are single examples. They show what a rule could or could not have captured, not how often.
