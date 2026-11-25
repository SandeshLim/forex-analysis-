# T1 setup — "hourly midpoint rejection in the trend" (XAUUSD)

Named by the user on Wed 25 Nov 2026 after their live sell (15:02–15:15 UK, 3465.73 → 3452.05).
Rules fixed on 25 Nov 2026 17:45 UK. Do not change them after looking at results; any change gets a new version number (T1 v2…) and its own log.

## Instrument, feed, time
- XAUUSD, OANDA feed on TradingView. All times Europe/London (UK). Broker (MT5) clock is UK + 2 h.
- Sessions: Asia 00:00–07:00, London 07:00–12:00, New York 12:00–17:00. T1 can form in any session; the session is recorded.

## Timeframes
- Direction: 4H (break of structure).
- Confirmation of direction: 1H swing structure.
- Range candle: the last completed 1H candle ("R").
- Trigger and entry: 1m.

## Criteria (sell version; buys are the mirror)
1. 4H trend down: the latest 4H close beyond a confirmed 4H swing point was a close below a swing low (swing = high/low with 3 candles each side, confirmed when the 3rd candle after it closes).
2. 1H structure down: the last two confirmed 1H swing highs are descending.
3. Range candle R = the 1H candle that has just closed. Midpoint M = (high + low) / 2. Range = high − low.
4. Midpoint zone = M ± 5 % of the range.
5. During the next hour, price trades up into the zone. If a 1m candle closes above the zone top, there is no trade that hour. If price reaches R's low before touching the zone, there is no trade.
6. Trigger: after the touch, a 1m candle closes below the low of the highest candle in the zone (the "peak candle"). Entry = that close.
7. Stop = zone top + 0.5.
8. Target = R's low (the opposite end of the range candle). If the target is less than 1× the risk away, skip the trigger.
9. Outcome is recorded on 1m: target first = win (+reward in R); stop first = −1R; neither within 3 h = time-out at the close. Spread/slippage (~0.4 points) is deducted when summarising.

## Grading and no-trade conditions
- A grade: 4H, 1H and 15m all agree, and the zone has a second reason (broken support/resistance, session high/low/mid, a marked zone).
- Skip within 15 min of high-impact US data (CPI, PCE, NFP, FOMC, GDP), or when the spread is unusually wide.

## Why it can work (hypotheses, not proven)
- Market structure: in a downtrend each bounce makes a lower high; T1 sells the bounce.
- Candle Range Theory: every candle's range is a mini-range with an equilibrium at 50 %. In a trend, a pullback that stalls at the previous candle's midpoint and fails tends to run to the opposite end of that candle.
- Price theory / premium–discount: above the midpoint is "premium" — where sellers in a downtrend prefer to sell.
- Liquidity: stops sit beyond the range candle's low; when it breaks, those stops can speed the move (25 Nov: −23 points in 2 minutes).
- Price action at the level is the trigger, not the reason: candle patterns alone were mixed on 25 Nov; the level and the trend did the work.

## Known weaknesses
- Built from one example on a strong trend day; likely to lose on ranging days.
- The target (R's low) is often only 1–2× the risk.
- Fast news spikes can blow through the zone.
