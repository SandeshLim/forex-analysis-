# Study 3 variant log (append only)
- 2026-11-16 00:55 — plan written; no study-3 computation yet. Waiting for the choice of final-evaluation data.
- 2026-11-16 01:15 — **Final-evaluation data re-assigned.** The user chose live observation from 16 Nov, so forward OANDA data from today is now EXPLORATORY, not the final holdout. The final evaluation must use data not looked at: OANDA 2008–2016 via Bar Replay (1m confirmed back to Jan 2008; about 22,700 bars per replay window), Dukascopy/histdata files, or a later forward window fixed in advance.
- 2026-11-16 01:15 — **Live logger started** (`live/live_logger.js`, live-1.0.0, sha256 131b8d4e…a31d, identical to the copy running in the tab). Families F1 (1m sequence stages 1–2, containment typed, context: completed level / developing extreme / 1h–4h zone / away), F2 (first trade beyond a session extreme standing ≥ 15 min), F3 (revisit of a 1h/4h displacement-body zone ≥ 4 h old). Back-filled over the OANDA 1m chart history, 2026-10-25 22:04 → 2026-11-16 01:14, then live every 20 s. Outcomes: R and mr at 15/30/60/240 min, MFE/MAE, first passage. No costs. Exploratory only.
- Back-fill first read (20 days, already-seen data, no costs). F1 stage 1: n 831, mean mr60 +0.17. F2 fade: n 184, mean mr60 −1.34 (the breaks continued). F3 4h revisits: n 140, mr60 −2.08 (the zones failed). F3 1h: n 257, ≈ 0. Leads only.
- 2026-11-16 08:22 UTC — Scheduled check of the live logger **could not run**: the Claude in Chrome side-panel connection was not available, so the TradingView tab (window.__L) could not be read. No live results recorded. If the tab stayed open, events since 01:15 should be in window.__L and in localStorage key 'claudeLiveLogger'.
- 2026-11-16 21:35 — Live logger read (exploratory). Running, no errors. However, background-tab throttling paused ticks: Asia events 04:54–05:34 were processed at 08:50, so only events with detection lag < 2 min count as truly real-time; the rest are delayed back-fill. F3 counts zone re-entries as new visits (visit numbers > 40 on one zone); revisit definition to be fixed (re-arm only after N bars outside) before F3 statistics are used.
- User example, 16 Nov Asia short (drawn 3875.51 / 3879.25 / 3832.42, 11.5R). Rule check on OANDA 1m:
  - The 1m sequence recognised at 05:23 (B1 05:21 bull, B2 05:22, not contained) → short 3876.39, stop 3878.69: 2R 05:30, 5R 05:35, developing Asia low +7.1R 05:46, previous-week low 3852.58 +10.4R 05:46, worst −0.98R.
  - Range-inside variant at 05:27 stopped at 05:28.
  - Stage 2 at 05:30 (3873.32): +5R by 05:46, worst −0.10R.
  - Drawn target missed by 0.04 (low 3832.46 at 05:58); later stopped at 14:35.
  - Context: the spike swept prior intra-session swing highs 3877.26 (02:55) / 3877.45 (04:00) inside a sequence of lower highs; it was 'away' from completed levels.
  - New exploratory lead to log, not test yet: sweeps of prior intra-session swing highs/lows (equal highs) inside a swing downtrend/uptrend (F4 extension).

## 2026-11-16 — Exploratory example: New York peak and re-entry short (user-drawn)

Source: OANDA XAUUSD 1m from the TradingView chart; times UTC = UK. Not a test; one hand-picked example, chosen after the fact.

- Context: the earlier NY swing high was 3885.45 (14:36), set by a strong bull bar at 14:35 (range 5.0×, body +3.3×, volume 3.2× median). The London high 3876.84 had already been broken. No completed session level sat at 3885–3889 (Asia high 3900.56, Fri NY low 3867.67).
- 14:48 peak bar: H 3888.95 swept the 14:36 high by 3.5, closed 3886.36 with an upper wick of 1.3×; volume 2.0×. Up bodies were shrinking: +3.3× (14:35), +1.8× (14:47), +1.6× (14:48), +0.7× (14:50).
- 14:49 and 14:50 were range-inside the peak bar. 14:51 bear expansion (body −1.6×) broke the peak bar low (3883.03), so the F1 bearish sequence printed at 14:51.
- 14:50–14:53 highs were 3887.48 / 3887.47 / 3887.48 / 3887.43: four failures at the same price under the peak. Volume eased to 1.2–1.4× on the drift to 3875.93 (15:00).
- Re-entry: the 15:01 bull bar (+2.0×, vol 2.5×) and 15:02 bar reached 3885.95, a lower high under both 3887.4 and the peak, then closed 3881.48 (upper wick). 15:03–15:10 printed lower highs on 2.0–2.6× volume.
- Drawn short: entry 3885.17, stop 3889.129 (R 3.96), target 3846.17 (9.85R). Filled in the 15:02 bar (a limit at 3885.17 would also have filled at 14:50). Stop never touched. Worst move against 3885.95 = 0.20R. 2R 15:07, 3R 15:10, 5R 15:23, 7R 16:00. NY low 3856.32 (16:37) = 7.3R by the 17:00 NY close. Target 9.85R touched 18:07, after the NY session; low 3841.21 at 18:10 (MFE 11.1R). No costs deducted.
- Recurring motif (same as 16 Nov Asia): the sweep of an earlier intra-session swing high, then a lower high that fails, within a fading up-move. Still an n=2 observation from one day; to be defined point-in-time and counted in the F1/F4 families before any claim.

## 2026-11-18 — 17 Nov scan for the user's "sweep → fail → lower-high re-entry" shape

Feed: FX_IDC:XAUUSD 1m (the chart's symbol on 18 Nov; earlier work used OANDA, differences ~0.03 at the 16 Nov NY high). 17 Nov 00:00–21:00 UTC, 1,260 bars, no gaps. Costs not deducted. Exploratory; one day.

Rule fixed before looking at results (both directions, per session Asia/London/NY):
1. Sweep: a bar trades beyond the developing session extreme that has stood ≥15 bars.
2. Peak: the extreme keeps updating while new extremes print within 15 bars.
3. E1: first close beyond the far side of the peak candle (below its low for shorts). Stop = peak ± 0.2.
4. Re-entry E2: within 60 bars, price retraces ≥50% of the move from the peak without reaching it; first close beyond the far side of the retrace-extreme bar.
5. Outcome to 21:00 UTC: stop first vs 2R/5R; MFE/MAE in R.

Result: 11 setups (6 short, 5 long). E1 reached 2R before stop 3/11, 5R 1/11. E2 occurred 6 times; 1/6 reached 2R and 5R.
- Only clean winner: Asia short, peak 3887.35 at 05:35 (Asia high, 1.6 below the 16 Nov NY high 3888.98). E1 3882.39 05:36 (R 5.16, 5R 10:11). Lower high 3885.94 05:46, E2 3880.76 05:52 (R 6.79, 2R 08:04, 5R 13:37; NY low 3836.50 13:40). Stopped 15:42. A limit at 3885.00 (user style) filled 05:46, R 2.55, MFE 19R at 13:40 before the 15:42 stop.
- Missed by the rule (found by eye afterwards — hindsight risk): NY 15:43 spike to 3890.98 swept the 16 Nov NY high 3888.98 and the 17 Nov Asia high; 15:44 closed below the peak-candle low; 15:45 lower high 3889.84; 15:46 close 3881.15 (stop 3891.18, R 10.03). Reached 4.0R by 20:01 (low 3840.90); continued to 3757.20 on 18 Nov 08:21. Missed because the sweep came <15 bars after the prior 15:39 peak.
- Losers dominated: the rule as written is not an edge on this day; the two good examples sat at prior-session highs (16 Nov NY high), suggesting the level matters more than the candle shape. Next: require the sweep/stall to be at a completed prior-session or prior-day level and count over many days.

## 2026-11-21 — 20 Nov scan (same rule as the 17 Nov scan, plus a level tag)

Feed: OANDA:XAUUSD 1m, 20 Nov 00:00–21:00 UTC, no gaps. Very volatile, falling day (median 1m range 3.33 vs 2.2 on 17 Nov). Costs not deducted. Exploratory.

Level tag (decided before reading results): peak within 1.5× median 1m range (5.0) of a completed earlier-session high/low from 19–20 Nov. Result: 16 rule setups, none tagged.

- E1 reached 2R before stop on 9 of 16 setups and 5R on 3 (two of the three are the same Asia floor). A trending, wide-range day gives room, so 2R hits are not comparable with 17 Nov.
- NY short (best fit to the user's shape): 15:00 spike to 3586.1 through equal NY highs 3581.3 (13:06) / 3581.5 (14:20), 9.2 below the London high 3595.3. 15:01 closed 3575.6 below the peak-candle low 3578.6. Lower highs 3576.2 (15:04), 3574.4 (15:08). R 10.7; low 3526.7 at 15:27 (4.6R); 5R 17:48; day low 3503.0 at 18:47 (6.7R). Caveat: 15:00 UK = 10:00 ET.
- Asia long (mirror): 05:16 low 3514.6 swept the 03:24 low 3517.4; 05:18 close above the 05:16 high, entry 3521.5, R 7.1; floor 3515.0 at 05:30/05:32/05:40, 3514.6 at 05:43; breakout 05:45–05:47; 2R 05:47, 5R 06:06, 06:10 high 3565.8, London high 3595.3 at 10:44 (~10R). Not at an earlier-session level.
- London double top 3594.7/3594.9/3595.3 (10:39–10:44) dropped to 3574.6 by 11:59; ~2–3R; the rule's first trigger at 10:40 was stopped at 10:43.
- Running pattern note: the winners on 16, 17 and 20 Nov all show repeated failures at one price (equal highs/lows or a floor/ceiling) before the break. Candidate feature for the formal test.

## 2026-11-21 — User's live trade, 18–19 Nov (user's broker screenshots)

Sell 0.01 XAUUSD at 3778.11, opened 18 Nov 14:30 UK (broker clock UK+2), stop 3787.74 (risk 9.63). Setup: New York 13:51 push to 3790.60 (OANDA) through the London high 3786.63, failure, lower highs 3787.5 (14:06) and ~3779.9 (14:29). Phone screenshot later on 19 Nov (broker axis ~17:25, so ~15:25 UK) shows bid 3685.81 and +70.23 GBP: ~92 points ≈ 9.6R against the original risk. The R came from holding through a strong downtrend, not from a tight stop. One trade; it does not test the setup.

## 2026-11-21 — 18 Nov scan (same rule and level tag as 17/20 Nov)

Feed: OANDA:XAUUSD 1m, 18 Nov 00:00–21:00 UTC, no gaps; median 1m range 2.13, level tolerance 3.2. Costs not deducted. Exploratory.

- 11 setups; E1 reached 2R before stop on 6, 5R on 2. Only one setup was level-tagged (NY short 13:26 near the 18 Nov Asia low 3776.0): stopped at 13:31.
- London short (rule): peak 3786.7 at 09:41 with highs 3786.4 (09:42) and 3786.3 (09:43) at the same price; 09:43 closed 3783.3 below the 09:41 low 3784.3 (E1, R 3.5); lower high 3784.2 at 09:51 (limit-style risk ~2.7); 2R 10:01, 5R 11:09, low 3743.0 at 12:56 ≈ 11R (E1) / ≈15R (limit). Not at an earlier-session level.
- NY long (rule): lows 3746.1–3746.6 (12:50–12:54) swept by 12:56 low 3743.0; 13:00 close 3747.5 above the 12:56 high; R 4.7; 5R 13:12; 3790.6 at 13:51 ≈ 9R.
- NY short at 13:51 (the user's live trade) was missed by the rule: the push from 3743 to 3790.6 never let a high stand 15 bars (same failure as 17 Nov 15:43). Rule change to consider: allow a sweep of a completed earlier-session level (here the London high 3786.68) regardless of the 15-bar condition.
- Asia longs against a falling market: mostly 2R then stopped.
