"""Build 5m bars from Exness 1m bars and the level tables with their availability times.

Levels (all are *completed* levels: a level only exists from the moment its period has ended):
  Asia 00:00-07:00, London 07:00-12:00, New York 12:00-17:00 (Europe/London local time, so GMT/BST handled);
  previous trading day / week / month, where the trading day rolls at 17:00 America/New_York.
Each 5m bar gets, for every level type, the most recent completed level value, its availability time and age.
"""
import numpy as np, pandas as pd, sys

M1 = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/research/exness_m1.pkl"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/research/bars5.pkl"

m1 = pd.read_pickle(M1)
m1 = m1[["open", "high", "low", "close", "tick_volume", "spread"]]
b5 = m1.resample("5min", label="left", closed="left").agg(
    {"open": "first", "high": "max", "low": "min", "close": "last", "tick_volume": "sum", "spread": "median"}).dropna()
b5["n1m"] = m1["close"].resample("5min", label="left", closed="left").count().reindex(b5.index)
b5["spread_pts"] = b5["spread"] / 1000.0          # Exness XAUUSDm: 3 digits, spread in points of 0.001
uk = b5.index.tz_convert("Europe/London")
ny = b5.index.tz_convert("America/New_York")
b5["uk_hour"] = uk.hour + uk.minute / 60
b5["session"] = np.select([b5.uk_hour < 7, b5.uk_hour < 12, b5.uk_hour < 17], ["Asia", "London", "NewYork"], "Late")
# trading day: NY 17:00 rollover -> label = NY date of the session end
tday = (ny + pd.Timedelta(hours=7)).normalize().tz_localize(None)
b5["tday"] = tday
b5["uk_date"] = uk.normalize().tz_localize(None)
# point-in-time volatility unit: median 5m range of the previous 48 bars (4 h), known at the bar's open
rng = (b5.high - b5.low)
b5["mr"] = rng.shift(1).rolling(48, min_periods=24).median()
b5["mvol"] = b5.tick_volume.shift(1).rolling(48, min_periods=24).median()

levels = {}
def add_level(name, key, avail_time):
    g = b5.groupby(key)
    t = pd.DataFrame({"hi": g.high.max(), "lo": g.low.min(), "start": g.apply(lambda x: x.index[0]),
                      "end": g.apply(lambda x: x.index[-1] + pd.Timedelta(minutes=5)), "nb": g.size()})
    t["avail"] = t["end"] if avail_time is None else avail_time(t)
    levels[name] = t.sort_values("avail")

# sessions: key = (uk_date, session)
for s in ["Asia", "London", "NewYork"]:
    sub = b5[b5.session == s]
    g = sub.groupby("uk_date")
    t = pd.DataFrame({"hi": g.high.max(), "lo": g.low.min(), "start": g.apply(lambda x: x.index[0]),
                      "last": g.apply(lambda x: x.index[-1]), "nb": g.size()})
    # availability = scheduled session end in UK time (not last bar), so an early-closing day is still on time
    endh = {"Asia": 7, "London": 12, "NewYork": 17}[s]
    t["avail"] = [pd.Timestamp(d).tz_localize("Europe/London") + pd.Timedelta(hours=endh) for d in t.index]
    t["avail"] = pd.to_datetime(t["avail"]).dt.tz_convert("UTC")
    levels[s] = t.sort_values("avail")
add_level("Day", "tday", None)
wk = (b5.tday - pd.to_timedelta(b5.tday.dt.dayofweek, unit="D"))   # Monday of the trading week
b5["tweek"] = wk
add_level("Week", "tweek", None)
b5["tmonth"] = b5.tday.dt.to_period("M")
add_level("Month", "tmonth", None)

for name, t in levels.items():
    a = pd.DataFrame({"avail": t["avail"].values, f"{name}_H": t.hi.values, f"{name}_L": t.lo.values,
                      f"{name}_t": t["avail"].values})
    a["avail"] = pd.to_datetime(a["avail"], utc=True); a[f"{name}_t"] = a["avail"]
    m = pd.merge_asof(pd.DataFrame({"time": b5.index}), a.rename(columns={"avail": "time"}).sort_values("time"),
                      on="time", direction="backward")
    for c in [f"{name}_H", f"{name}_L"]:
        b5[c] = m[c].values
    b5[f"{name}_avail"] = m[f"{name}_t"].values
b5.to_pickle(OUT)
pd.to_pickle(levels, OUT.replace(".pkl", "_levels.pkl"))
print(len(b5), b5.index[0], b5.index[-1])
print("5m bars with <5 one-minute bars:", int((b5.n1m < 5).sum()))
print(b5[["session", "Asia_H", "London_H", "NewYork_H", "Day_H", "Week_H", "Month_H"]].iloc[[100000, 400000]])
for n, t in levels.items():
    print(n, len(t), "median bars", int(t.nb.median()))
