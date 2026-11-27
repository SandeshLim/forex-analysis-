# XAUUSD zones after the reset: Friday 27 Nov 2026 (05:40 UK)

Feed: OANDA:XAUUSD. At the user's request, all old drawings were removed. A backup is stored in browser localStorage under `xau_drawings_backup_2026-11-27`. No trades were placed.

## Why the 27 Nov Asia plan failed
- Asia rallied from 3557.7 to 3666.7 (a 109-point range, against a median of 44).
- S1 and S2 were cancelled by 15m closes above them at 01:45 and 02:00.
- B1 was missed by 1.8 points, so no trigger fired and no trade was lost.
- The plan bet on continuation of a down move, and the market squeezed the other way.

## Facts at 05:40
- **Asia so far:** H 3666.7 (a 1m spike at 05:30), L 3557.7, midpoint 3612.2.
- **The spike at 05:30 was rejected.** The highs after it were 3659.8, 3659.3 and 3659.3. The failed-break sell trigger fired at 05:33, at 3652.4, with a stop at 3667.2.
- **The 4H candle running 02:00–06:00 is trading above the last 4H swing high of 3607.2.** If it closes there at 06:00, the 4H trend flips up.

## Backtest, 17 Sep – 27 Nov (15m fills on 1H base zones, 2R target)

| Group | First-touch entry | 15m-confirmed entry |
|---|---|---|
| With the 4H trend | n63, 30% won, −6.0R | n47, 30% won, −6.8R |
| Against the 4H trend | n62, 40% won, +13.0R | n51, 39% won, +7.6R |
| With trend, New York session only | n21, 38% won, +3.0R | n16, 44% won, +5.0R |
| With trend, Asia session only | n31, 23% won, −10.0R | n21, 29% won, −4.8R |

**Conclusion:** in this window, the 4H BOS filter did not help. With-trend zones only worked during New York with confirmation, on a small sample.

## Days with a strong up Asia session (closing in the top 25% of its range), n = 12
- On 9 of 12 days, price traded back below the Asia midpoint later in the day.
- On 8 of 12 days, price made a new high above the Asia high, but the median extension was only 7.1 points.
- The median pullback from the Asia close was 32.6 points.
- When the Asia range was at least 60 points (n = 5): 3 days went back below the midpoint and 3 made a new high (median extension 2.3).

## Zones (drawn until 21:00 UK)

| Zone | Range | Logic |
|---|---|---|
| S1 sell | 3659.3–3666.7 | The 05:30 spike was rejected: 24 Nov 1H high 3660.9, then three lower highs. The trigger has already fired |
| S2 sell | 3672.3–3681.3 | A 1H sell base from 23 Nov plus the 24 Nov Asia highs (3670.2, 3678.5). Statistically, any new high should extend only a few points |
| B1 buy | 3621.2–3626.9 | The Asia base from 02:45–04:45, which broke upward at 05:00 |
| B2 buy | 3600.0–3612.2 | Yesterday's broken sell zone (3607.2) now acting as support, the Asia midpoint (3612.2) and the round number 3600. On 9 of 12 comparable days price returned below the Asia midpoint |

**Entries:** use the failed-break trigger at every zone, and put the stop beyond the spike extreme by 0.5. Following the backtest, prefer New York over London.
