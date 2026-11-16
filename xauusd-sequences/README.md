# XAUUSD candle sequences at meaningful levels (study 2)
See `REPORT.md` for results. `PLAN.md` was written before any statistics were computed; `VARIANT_LOG.md` lists every run.
Reproduce: obtain the Exness parquet (`sherwynjoel/xauusd-historical-data`, commit c6aa574, sha256 74b277a0…), convert it to `exness_m1.pkl`, then run `src/prepare.py`, `src/events.py`, split by date as in PLAN.md, then `src/catalogue_dev.py` and `src/candidates.py SPLIT IDS`. Raw bars are not redistributed.
