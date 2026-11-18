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
