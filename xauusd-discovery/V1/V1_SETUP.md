# V1 setup (working name) — V-shape recovery buy (XAUUSD)

Described by the user on Wed 25 Nov 2026 18:22 UK from the 17:30–17:39 move. Rules written on 25 Nov 18:25 UK; any change after results = new version.
Feed: OANDA XAUUSD on TradingView; UK time (broker MT5 clock = UK + 2 h).

## Criteria (buy; a sell mirror is not defined yet)
1. V-shape recovery: after a sharp fall to a low, price rallies and a 15m candle closes above the last 1H lower high (here: the 17:00 15m closed 3493.1 above the 14:00 1H high 3489.9; low was 3426.8 at 15:19).
2. Pullback on 1m after the recovery's first high (here: 3518.2 at 17:22 → 3494.9 at 17:24).
3. Two shooting-star candles at the pullback low: upper wick ≥ 50 % of the candle's range and body ≤ 35 % of the range (here 17:31 and 17:32).
4. Strong buying candle: bullish, body ≥ 2× the median body of the previous 20 one-minute candles, and closes above the high of the small range (here 17:35: open 3498.1, close 3503.1).
5. Range = lowest low to highest high from the first shooting star to the candle before the strong candle (here 17:31–17:34: 3496.3–3500.5).
6. Entry: buy limit at range top + 0.5 when price comes back to retest the range within 15 minutes of the strong candle (here 3501.0; the 17:38 low was 3500.7, so it filled — a limit exactly at the range top would have missed by 0.2).
7. Stop: range low − 0.5 (here 3495.8; risk 5.2).
8. Targets: first the recovery's high (here 3518.2, ≈3.3R), then the next session level (here the London high 3540.5, ≈7.6R).
9. No trade if the range low breaks before the retest, if no retest comes within 15 minutes, or within 15 minutes of high-impact US data.

## Grade
- Counter to the 4H trend (as on 25 Nov) = grade B, smaller risk.
- With the 4H trend = grade A.

## 25 Nov example result
Entry ≈3501.0 at 17:38, stop 3495.8. After entry: low 3501.5 (17:45), high 3540.87 (18:17) ≈ +7.6R; 3518.2 reached 17:54 (≈3.3R). Context: day before Thanksgiving, US stocks closed 18:00 UK, thin trading, short covering.

## Open question for the user
Entry price: limit at range top (+0.5 used here) or another level — confirm.

## How V1 looked on each timeframe, 25 Nov (added 18:50 UK)
- 1m: shooting stars 17:31 and 17:32 (range 3496.3–3500.5) → strong candle 17:35 (3498.1→3503.1) → retest low 3500.7 at 17:38.
- 5m: shooting star 17:40 (upper wick 9.8, body 0.9) and hammer 17:45 (range 3501.5–3517.5) → strong candle 17:50 (3506.3→3520.2) → retest lows 3514.3 (17:55) and 3512.8 (18:00).
- 15m: shooting star 17:15 (upper wick 17.9, body 7.2); 17:30 nearly one (wick 46 % of range) → strong candle 18:00 (3514.8→3528.1) → 18:30 hammer low 3526.1 back into the 18:00 candle.
- The same pattern repeated on 1m, then 5m, then 15m, each a step higher.

## User's actual trades, 25 Nov (from screenshots)
- A (1m version): buy 3497.63, stop 3495.45 (risk 2.18), target 3527.20. Filled in the dip at the start of the 17:35 strong candle (low 3497.0), inside the range. Target hit about 17:55–17:59 (5m high 3527.7) ≈ +13.6R.
- B (5m version): buy 3515.49, stop 3512.64 (risk 2.85), target 3537.76. Filled on the retest about 17:55; the 18:00 low 3512.8 missed the stop by 0.16. Target hit about 18:05–18:09 (high 3538.2) ≈ +7.8R.
- Note: the user's entries were inside the range (not "range top + 0.5"), and trade B's stop was below the retest, not below the 5m range low. Entry/stop rule to be confirmed by the user before tracking starts.
