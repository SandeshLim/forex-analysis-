# Data provenance

| Item | Value |
|---|---|
| Source | TradingView chart, symbol `OANDA:XAUUSD` (OANDA spot gold CFD quotes, as served by TradingView) |
| Extracted | 2026-11-15, from the user's chart via the TradingView page's own series data (`data/browser_extract.js`) |
| Time stamps | Bar **open** time, UTC epoch seconds. A 5m bar stamped 12:15 covers 12:15:00–12:19:59 |
| Volume | Tick volume (count of OANDA price updates), not traded volume |
| Price units | USD per troy ounce; 1 point = $1/oz |
| Weekly/daily schedule | Sunday open ~22:00/23:00 UTC; daily break ~21:00–22:00 UTC (summer) / 22:00–23:00 UTC (winter) |
| Plan limit | TradingView served at most ~20,000 bars per resolution, which sets the earliest date below |

| Dataset | Bars | First bar (UTC) | Last bar (UTC) | SHA-256 of rows `t,o,h,l,c,v` joined by `\n` |
|---|---|---|---|---|
| 5-minute | 20,670 | 2026-08-02 22:00 | 2026-11-13 21:55 | `5d89f5f8df4d0201f6e250c17a3411f2c00e85ddeeb36523a24ed4f505b96f59` |
| 1-minute | 20,640 | 2026-10-25 22:04 | 2026-11-13 21:59 | `8f97addc33d6cfc7a24a8894bf8d89dd92fb0e1f0db9548a80c6d71d06d9307d` |
| 4-hour | 701 | 2026-06-03 17:00 | 2026-11-13 18:00 | `fa2cb729f3abe9da2a640fd6bd55dd1cfb0d84527b6fad45acebf404166e697a` |

Checks run on 2026-11-15:
- The native 5m bars equal 1m bars aggregated to 5m on every overlapping bar (4,140 bars; max price difference 0, volume mismatches 0).
- Every Asia/London/New York session in P1–P3 has its full bar count (84 / 60 / 60 five-minute bars).

## What is and is not in this repository

- **Not committed:** the raw OHLCV bars. This repository is public and the bars are OANDA/TradingView market data; redistributing them may breach those providers' terms. Re-extract with `data/browser_extract.js` and compare against the hashes above.
- **Committed:** `export_compact.txt`, the engine's own event/trade/level export (SHA-256 `260260e62ef6d7673c31396cd5ec2bbd369a49ef547425ce5780b96de9d2cfec`), and the CSV logs decoded from it in `logs/`. These contain only levels, entry/stop/exit prices and derived measures, not bar series.
- The five evidence panels in `evidence/` contain a few 5m bars around each event (as offsets from the level) for audit purposes.
