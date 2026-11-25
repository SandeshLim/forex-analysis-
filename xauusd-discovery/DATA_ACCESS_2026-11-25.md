# Data access check, 25 Nov 2026 22:06 UK (TradingView Premium)
- Feed for all zones, reviews and tests: OANDA:XAUUSD (verified: 25 Nov 14:59 high 3473.78, 02:31 high 3575.29, 24 Nov 12:45 high 3646.80 all match earlier OANDA pulls).
- Live chart, 1m: 24,767 bars loaded (1 Nov 23:04 → 25 Nov 21:59); no more history loads beyond that.
- Bar Replay (separate from export): available. Replay start date reported for the symbol: 19 Mar 2006 20:29 UTC. Tested 1m windows: 4 Mar 2025 → 22,642 bars back to 9 Feb 2025; 5 Jan 2010 → bars present; the Mar 2006 start loaded no 1m bars. Each replay window holds ~22.6k 1m bars (~3.5 weeks) before the chosen date.
- CSV export ("Download chart data"): exports only the bars loaded on the chart (here 1–25 Nov 2026, plus indicator columns). Downloaded to the user's Mac; folder access to ~/Downloads was refused, so the file must be attached by the user. To export older periods: start Bar Replay at a date, load history, then export (to be verified).
- Test replay was left without saving; the chart is back on live OANDA 1m.
