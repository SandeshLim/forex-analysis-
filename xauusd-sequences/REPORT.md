# XAUUSD candle sequences at meaningful levels — study 2 report (16 Nov 2026)

## Plain-English summary (corrected 16 Nov 2026 00:50)
- **Scope.** Four specific rule families were rejected; the broader research question is **not** settled. All tests used 5-minute recognition at *completed* session/day/week/month levels.
- **Your sequence at completed levels.** It lost money after costs on 2024–2026 TEST at all three recognition stages: small candle −0.15R, expansion −0.18R, retest −0.17R (CI −0.33..0.00). On VAL the retest stage was indistinguishable from zero (−0.04R, CI −0.24..+0.16). The stage-1 and stage-3 VAL/TEST rows were run after TEST was opened, to complete the table.
- **Not tested:** 1-minute sequences, developing session extremes, historical 1h/4h candle zones, swing changes, later retests. See `STUDY3_PLAN.md` and the coverage matrix in `COVERAGE.md`.
- **Level touches.** On average they do not reverse (DEV: +0.01 mr at 1h, CI −0.10..+0.12).
- **Drawn trades.**
  - The 03:38 Asia short matches a 1-minute sequence (entry 03:41, 0.37 points worse). Targets set before entry (2R/3R/5R; the developing Asia low, +14R) were reached.
  - The 13:34 and 14:45 drawn entries sit ahead of any defined trigger; the only earlier 1-minute triggers were stopped.
  - The exact drawn 16.5R/15.8R targets were missed by 0.31/0.17 points. That is a separate question from whether a trade was plannable. See `results/drawn_trades.md`.

## 1. Your screenshots
All five are OANDA XAUUSD captures from 15 Nov 2026. Four show Fri 13 Nov; the 21:29:18 capture shows a Bar Replay of Thu 12 Nov. No NIFTY/BANKNIFTY screenshots were attached.

| Screenshot | Clearly visible | Uncertain | What would resolve it |
|---|---|---|---|
| 21:20:54 | 1m, Fri 13 Nov 05:30–22:00 UTC; 13:30 spike to ≈3,905 then decline to ≈3,868 by 16:00; recovery to 3,884.7 at the close | nothing drawn | — |
| 21:29:18 | Bar Replay on 12 Nov; "Asian Session Range" boxes (labels A = 3826, L = 4029.5), PWL line ≈3,890; price falling into PWL ≈14:00 | The indicator's settings ("20 00 02 00 … 03 00 07 00 … 08 00 12 00") suggest session hours in another timezone (possibly New York) than the UK hours used here. Units of the A/L labels are unclear | Indicator settings and its timezone |
| 23:10:48 | Short drawn ≈3,898.5 / stop ≈3,901.9 / target ≈3,868.2 when price returned at ≈14:50 to the zone of the 13:30 spike | Exact zone edges | Verified on OANDA 1m: filled 14:45, target hit 16:01; best 9.2R, worst −0.39R. A later visit to the same zone with a different response |
| 23:12:22 | 13:30 sweep short 3,903.885 / 3,906.186 / 3,867.501 (drawn 15.81R) | — | OANDA 1m: filled 13:34, never stopped (worst −0.91R), best 15.7R; **target missed by 0.17**. On 5m it is a valid sequence at the completed London high 3,905.975 (B1 13:30 range 7.8× normal, B2 13:35 range-inside, B3 13:40) but recognisable only at 13:40 close, 3,896.99 |
| 23:13:33 | Asia short at 03:38, 3,920.651 / 3,923.880 / 3,867.359 (drawn 16.5R) | — | Filled 03:38, worst −0.76R, best 16.4R, **target missed by 0.31**; the high swept was the *developing* Asia high (made at 03:40), not a completed level. The day's low (3,867.67) came 12 hours later |

## 2. Data coverage
| Feed / timeframe | Bars | First (UTC) | Last (UTC) | Source |
|---|---|---|---|---|
| OANDA:XAUUSD monthly | 249 | 2006-02-28 | 2026-11 | TradingView, direct |
| weekly | 1,079 | 2006-03-19 | 2026-11-15 | direct |
| daily | 5,352 | 2006-03-19 | 2026-11-15 | direct |
| 4h | 21,433 | 2013-01-01 | 2026-11-15 | direct |
| 2h | 21,218 | 2020-01-01 | 2026-11-15 | direct |
| 1h | 22,907 | 2023-01-02 | 2026-11-15 | direct |
| 15m | 20,632 | 2026-01-01 | 2026-11-15 | direct |
| 5m | 20,670 | 2026-08-02 | 2026-11-13 | direct |
| 1m | 20,640 | 2026-10-25 | 2026-11-13 | direct |
| Exness MT5 XAUUSDm 1m | 3,276,127 | 2017-04-28 | 2026-08-18 07:16 | public GitHub dataset `sherwynjoel/xauusd-historical-data` @c6aa574 (sha256 of parquet 74b277a0…) |
| Exness 5m (research base) | 656,385 | 2017-04-28 | 2026-08-18 | aggregated here from 1m |

- TradingView caps each resolution at about 20,000 bars, so its intraday history is short. Gaps on TradingView are holiday closures (largest about 28–29 h at Christmas); 2 OHLC inconsistencies on 4h.
- **Exness 1m checks.** No duplicate timestamps and no OHLC violations. 2,404 gaps longer than 60 minutes (weekends, daily breaks, holidays). 4,162 of 656,385 five-minute bars contain fewer than five 1-minute bars. Volume is broker tick volume; spread is the broker's quoted spread in 0.001 units (median 0.16–0.30 points by year).
- **Compatibility.** With zero clock shift, OANDA − Exness 5m close = +0.12 (SD 0.16, 275 bars, 5 Aug 2026), and weekly noon closes 2023–26 = +0.105 (187 checks). A ±5-minute shift makes the error 17× larger. Timestamps are UTC bar-open.
- **Not available here.** Any intraday data before 2017 (histdata.com, Dukascopy, Yahoo and Stooq are unreachable from this workspace), and anything before 2006. **A 10–20-year intraday study was not possible.** If you can supply Dukascopy or histdata files, the same code runs on them.
- **Timezones.** Sessions are UK local time (Europe/London, so GMT/BST handled): Asia 00:00–07:00, London 07:00–12:00, New York 12:00–17:00, "Late" 17:00–24:00. The trading day rolls at 17:00 New York. Every level is a **completed** level, usable only after its period ends (Asia at 07:00 UK, London at 12:00, New York at 17:00, day at the rollover, week at the Friday close, month at month-end).

## 3. Method
- **Base timeframe and units.** 5m bars, with exits simulated on 1m. Volatility unit `mr` = median 5m range of the previous 48 bars (known in advance). All outcomes are measured from the close of the bar at which a stage is first recognisable.
- **Touch.** First entry of price to within 0.25 mr of a completed level from the near side, after 6 bars outside.
- **Sequence (bearish; the bullish case mirrors it).**
  - B1: bullish, body ≥ 50% of range, range ≥ 1.5 mr.
  - B2: bearish, body ≤ 50% of B1's body. Containment is typed separately: *range-inside* (high and low inside B1), *body-inside only*, or *not contained*.
  - "At level": B1/B2 reached a completed high from below. "Away": no level within 3 mr.
  - Stage 2: within 3 bars, a bearish expansion bar (body ≥ 50%, range ≥ 1.5 mr) closing below B2's low, with no close above the sequence high first.
  - Stage 3: within 12 bars, a retest into B3's body midpoint that closes back below it.
- **Trap.** A stage-2 signal followed within 12 bars by a close beyond the sequence extreme.
- **Splits (chronological, fixed before scanning).** DEV 2017-05→2021, VAL 2022–23, TEST 2024→2026-07 (sealed, hashed, opened once). Budget: ≤ 4 candidates × ≤ 3 variants on DEV.
- **Execution.** Entry at the recognition close. Longs buy at the ask (bid + spread + 0.1), shorts sell at the bid − 0.1; exits at the opposite side; stops pay another 0.1. Stop is checked before target within each minute.
- **Uncertainty.** Bootstrap CIs resample trading days. All runs are in `VARIANT_LOG.md`, including one cost-model bug found and fixed before any selection.

## 4. Counts
- **Level touches:** 25,846 over the full history (DEV 12,995 on 1,207 days).
- **Two-candle formations (B1+B2):** 29,194 over the full history (58,388 candles). 7,406 occurred at a completed level (range-inside 2,913, body-inside-only 2,040, not contained 2,453), on 2,241 distinct trading days.
- **Stage 2 (three candles):** reached by 20–27% of formations.
- **Stage 3 (four or more candles):** reached by about 60% of stage-2 cases (DEV 2,137 of about 3,400).

## 5. Ranked results (executable, after costs; R per trade, 95% day-clustered CI)
| Candidate | DEV 2017–21 | VAL 2022–23 | TEST 2024–26 (untouched) | TEST at double cost |
|---|---|---|---|---|
| C2V3 trend-aligned sequence, stage 2, 3R | −0.125 (−0.265..+0.019), n 298 | −0.132 (−0.383..+0.131), n 87 | **−0.179 (−0.360..+0.023)**, n 113 | −0.236 |
| C1V2 your sequence at level, stage 2, 2R | −0.182 (−0.269..−0.095), n 643 | −0.138 (−0.287..+0.017), n 209 | **−0.182 (−0.310..−0.055)**, n 254 | −0.249 |
| C3V2 fade ≥ 1.3 mr overshoot, 1h exit | −0.321 (−0.397..−0.244), n 1,792 | −0.151 (−0.300..+0.005), n 652 | **−0.176 (−0.312..−0.032)**, n 724 | −0.326 |
| C4V1 fade late-session touches, 1h exit | −0.378 (−0.436..−0.318), n 2,171 | −0.285 (−0.379..−0.185), n 854 | **−0.128 (−0.232..−0.028)**, n 1,216 | −0.315 |

- **Recognition stage (DEV, C1):** entering at B2 close −0.476R; at expansion close −0.182R; at a held retest −0.212R. Waiting improves selection, but about 1.9 mr of the move has already happened at stage 2.
- **Drawdowns (in R):** TEST C1V2 −48.7; C2V3 −24.6; C3V2 −177; C4V1 −172.
- **Long vs short:** in DEV and VAL, bearish (short) versions were consistently worse than bullish, matching the 2017–2026 gold uptrend. On TEST, C4's long side was ≈ 0 (+0.009R).

## 6. Observations, interpretations and validated findings
**Validated findings:** none met the pre-set bar (TEST lower 95% bound > 0 after costs, same sign on VAL).

**Observations (descriptive, DEV, about 80 cells examined, so some are chance):**
1. **Penetration depth.** Deeper pushes beyond a level were followed by more 1-hour reversion (top-fifth penetration ≥ 1.29 mr: +0.36 mr vs −0.11 for shallow touches; difference +0.47, CI +0.10..+0.84). They were also more often followed by a full break within 2 hours (82% vs 53%). Big pushes resolve both ways.
2. **Approach speed.** Stronger approaches (24-bar) were followed by less reversal (−0.37, CI −0.71..+0.02). This is consistent with momentum.
3. **Confluence.** More levels within 1 mr were followed by less reversal (−0.30, CI −0.61..−0.01).
4. **Quiet hours.** Late-session (17:00–24:00 UK) touches reversed more (+0.22, CI +0.04..+0.39). Executable, the effect was too small for the costs.
5. **Your bearish sequence at highs.** It failed in DEV even when aligned with a daily downtrend: −0.33 mr at 1h after the small candle (CI −0.66..−0.01).
6. **Bullish mirror at lows with the uptrend.** +0.64 mr after confirmation (CI −0.04..+1.38). It did not survive costs or VAL/TEST.
7. **Year by year.** The stage-2 sequence's 1h outcome changes sign from year to year in both directions (e.g. bearish 2019 −1.02, 2023 +0.38, 2024 −0.76 mr). It is not stable.
8. **Traps.** 24–33% of confirmed sequences fail within 1h in every split. After a bearish trap (price reclaims the high), the next hour moved further up by +0.01 (DEV), +1.71 (VAL) and +1.01 mr (TEST), on 30–106 cases. Inconsistent, and a lead only.
9. **Elephant's footprint.** Tick-volume spikes at the touch (top fifth) went with larger subsequent moves *in both directions*: more reversion on average, but breaks 72% vs 55%. Activity signals the size of what follows, not its direction. Candles and broker tick counts cannot identify who traded.

**Interpretations (not tested here):** see section 7.

## 7. Psychology and market structure (hypotheses, not conclusions)
| Directly observable | Possible behavioural explanation | Alternatives | Distinguishing prediction | Data cannot establish |
|---|---|---|---|---|
| Reversion after deep overshoot | Stop-loss orders resting just beyond levels are triggered (Osler 2003 found stop-losses clustered just beyond round numbers in FX order books; take-profits at the numbers) | Liquidity vacuum and spread widening; mechanical mean reversion of noise | Overshoot reversion should be stronger at round numbers and at widely watched levels than at arbitrary prices with the same volatility | Whether stops existed; Exness tick volume is not order flow |
| Strong approaches continue through levels | Anchoring and slow adjustment near reference prices, then catch-up once crossed (George & Hwang 2004 for 52-week highs in equities) | Momentum from information arrival; trend regime of gold 2017–2026 | Continuation should be larger the more salient the level (week/month vs session) | Investor beliefs |
| Late-hour touches revert more | Thin participation lets small orders move price and then fade | Wider spreads; Asian-hour mean reversion is a generic microstructure effect | The effect should scale with spread and volume, not with level type | Liquidity provider behaviour |
| Small contained candle after a strong push | "Pause" or hesitation | Pure noise: a small bar is the most common bar after a large one | If informative, outcomes should differ from the same push followed by any other bar (they did not, beyond noise) | Exhaustion of buyers |

Academic studies of candlestick rules generally find little or no value after costs and data-snooping control. For example, an intraday 5-minute study of DJIA stocks found no out-performance once trading costs were included (Duvinage, Mazza & Petitjean 2013), and a EURUSD study of adaptive candlestick patterns found no net positive returns after costs (Orquín-Serrano 2020). The results here are consistent with that literature.

## 8. Entry playbook
**None is supported.** No variant produced positive expectancy after costs out of sample. If you trade these patterns, the data suggest that:
1. Waiting for the expansion candle is better than entering on the small candle, though still negative.
2. Short versions underperformed in a rising market.
3. Wide sequence stops make R-multiples look large, but costs are a large share of R when stops are 1–3 points.
4. A drawn target at the eventual extreme is not a forecast.

## 9. Unsuccessful hypotheses and remaining questions
- **Rejected:** C1 (your sequence and mirror at completed levels, 3 recognition stages); C2 (trend-aligned, 3 targets); C3 (overshoot fade, 3 thresholds); C4 (late-session fade, 3 filters).
- **Not tested, within budget:**
  - 1-minute recognition (entry on 1m closes, nearer your drawn entries).
  - Round-number levels.
  - Historical displacement-candle zones (bodies of large 1h/4h candles) and their revisits.
  - Retests later than 1 hour (your 14:45 example came 75 minutes after the 13:30 bar).
  - Developing (intra-session) highs and lows, as in your Asia example.
  - Swing-structure changes.
  - Verified economic calendar (no calendar source reachable from this workspace).
  - The post-trap continuation lead.
- **Any of these needs a new pre-registered test on fresh data.** VAL and TEST are now spent. The only untouched data is forward from 16 Nov 2026, or pre-2017 intraday data from another source.

## Files
`PLAN.md` (written before scanning), `VARIANT_LOG.md` (every run), `src/` (prepare, events, catalogue, sim, candidates, plot), `results/` (CSV tables and catalogue output), `logs/` (every simulated trade), `evidence/` (rule-selected example panels). Raw Exness and OANDA bars are not committed.

## References
- Osler, C. L. (2003). Currency orders and exchange rate dynamics: an explanation for the predictive success of technical analysis. *Journal of Finance* 58(5), 1791–1819.
- George, T. J. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance* 59(5), 2145–2176.
- Duvinage, M., Mazza, P. & Petitjean, M. (2013). The intra-day performance of market timing strategies and trading systems based on Japanese candlesticks. *Quantitative Finance* 13(7), 1059–1070.
- Orquín-Serrano, I. (2020). Predictive power of adaptive candlestick patterns in Forex market: EURUSD case. *Mathematics* 8(5), 802.
