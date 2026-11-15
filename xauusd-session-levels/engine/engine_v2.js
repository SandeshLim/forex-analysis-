function xauResearch() {
  // XAUUSD session-level break study, engine v2.0.0. Runs in the TradingView chart page on bar arrays
  // [time_open_utc_sec, open, high, low, close, tick_volume]. No look-ahead in footprint flags (pitFlags).
  const VERSION = '2.0.0';
  const CONFIG = {
    symbol: 'OANDA:XAUUSD',
    sessionsUK: [['Asia', 0, 7], ['London', 7, 12], ['New York', 12, 17]],
    sessionsAhead: 2,
    bst: [Date.UTC(2026, 2, 29, 1) / 1000, Date.UTC(2026, 9, 25, 1) / 1000],
    baselineBars: 24, volSpikeMult: 2, rangeMult: 2, absorbVolMult: 1.5, absorbRangeMult: 0.75,
    wickFrac: 0.6, compressionBars: 6, compressionMult: 0.6, preBreakBars: 3, signalBars: 3,
    rr: 1.5, fadeStopBuffer: 0.5, timeExitMin: 60, costPts: 0.3, tieRule: 'stop',
    bootstrapN: 5000, seed: 12345
  };
  const C = CONFIG;
  const med = a => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
  const ukOff = t => (t >= C.bst[0] && t < C.bst[1]) ? 3600 : 0;
  const ema = (a, n) => { const k = 2 / (n + 1); let e = a[0]; return a.map(x => e = x * k + e * (1 - k)); };

  // Footprint flags for every 5m candle i, using only the baselineBars candles before i (known at i's close).
  function pitFlags(M) {
    const F = new Array(M.length).fill(null);
    for (let i = C.baselineBars; i < M.length; i++) {
      const p = M.slice(i - C.baselineBars, i), mr = med(p.map(v => v[2] - v[3])), mv = med(p.map(v => v[5]));
      const v = M[i], rg = v[2] - v[3];
      F[i] = { mr, mv, V: v[5] > C.volSpikeMult * mv, R: rg > C.rangeMult * mr,
               A: v[5] > C.absorbVolMult * mv && rg < C.absorbRangeMult * mr, visibleAt: v[0] + 300 };
    }
    return F;
  }

  function sessions(M, dayFrom, dayTo) {
    const S = [];
    for (let d = Date.UTC(...dayFrom) / 1000; d <= Date.UTC(...dayTo) / 1000; d += 86400) {
      const dow = new Date(d * 1000).getUTCDay(); if (dow === 0 || dow === 6) continue;
      const off = ukOff(d + 12 * 3600);
      for (const [n, a, b] of C.sessionsUK) {
        const s = d + a * 3600 - off, e = d + b * 3600 - off, bs = M.filter(v => v[0] >= s && v[0] < e);
        if (!bs.length) continue;
        S.push({ day: new Date(d * 1000).toISOString().slice(0, 10), n, s, e, nb: bs.length,
                 hi: Math.max(...bs.map(v => v[2])), lo: Math.min(...bs.map(v => v[3])) });
      }
    }
    return S;
  }

  // opt: {excludeOff:bool, flagMode:'pit'|'legacy', period:string}; X = execution bars (5m or 1m), xSec = X bar length
  function run(M, X, xSec, H4, dayFrom, dayTo, opt) {
    opt = Object.assign({ excludeOff: true, flagMode: 'pit', period: '' }, opt || {});
    const e4 = ema(H4.map(v => v[4]), 20);
    const trend = t => { const i = H4.findIndex(v => v[0] + 14400 > t) - 1; if (i < 5) return '?';
      const c = H4[i][4], e = e4[i], sl = e4[i] - e4[i - 3]; return (c > e && sl > 0) ? 'Up' : (c < e && sl < 0) ? 'Down' : 'Mixed'; };
    const PF = pitFlags(M), S = sessions(M, dayFrom, dayTo), levels = [], E = [];
    S.forEach((src, i) => { for (const side of ['H', 'L']) {
      const lvl = side === 'H' ? src.hi : src.lo, sg = side === 'H' ? 1 : -1, beyond = v => sg * ((side === 'H' ? v[2] : v[3]) - lvl) > 0;
      let found = null;
      for (const ses of S.slice(i + 1, i + 1 + C.sessionsAhead)) { const idx = M.findIndex(v => v[0] >= ses.s && v[0] < ses.e && beyond(v)); if (idx >= 0) { found = { idx, ses }; break; } }
      const name = src.day + ' ' + src.n + ' ' + (side === 'H' ? 'high' : 'low');
      const laterSessions = S.slice(i + 1, i + 1 + C.sessionsAhead).length;
      if (!found) { levels.push({ name, lvl, side, tested: false, censored: laterSessions < C.sessionsAhead }); continue; }
      const idx = found.idx, k = M[idx];
      const offCross = M.some(v => v[0] >= src.e && v[0] < k[0] && beyond(v));
      levels.push({ name, lvl, side, tested: true, offCross, censored: false });
      if (opt.excludeOff && offCross) continue;
      const three = M.slice(idx, idx + C.signalBars);
      const base = M.slice(idx - C.baselineBars, idx), mr = med(base.map(v => v[2] - v[3])), mv = med(base.map(v => v[5]));
      const pre = M.slice(idx - C.preBreakBars, idx);
      const legacyF = pre.map(v => ({ V: v[5] > C.volSpikeMult * mv, R: (v[2] - v[3]) > C.rangeMult * mr, A: v[5] > C.absorbVolMult * mv && (v[2] - v[3]) < C.absorbRangeMult * mr }));
      const pitF = pre.map((v, j) => PF[idx - C.preBreakBars + j]);
      const pre6 = M.slice(idx - C.compressionBars, idx);
      const comp = pre6.length === C.compressionBars && pre6.reduce((a, v) => a + v[2] - v[3], 0) / C.compressionBars < C.compressionMult * mr; // known at break-candle open
      const kF = { V: k[5] > C.volSpikeMult * mv, R: (k[2] - k[3]) > C.rangeMult * mr, A: k[5] > C.absorbVolMult * mv && (k[2] - k[3]) < C.absorbRangeMult * mr };
      const rg = k[2] - k[3], wk = side === 'H' ? k[2] - Math.max(k[1], k[4]) : Math.min(k[1], k[4]) - k[3];
      const W = rg > 0 && wk / rg >= C.wickFrac && sg * (k[4] - lvl) < 0;
      const any = fs => fs.some(f => f && (f.V || f.R || f.A));
      const earlyLegacy = any(legacyF) || comp, earlyPit = any(pitF) || comp;
      const fmt = fs => fs.map((f, j) => (f && (f.V || f.R || f.A)) ? (new Date(pre[j][0] * 1000).toISOString().slice(11, 16) + ':' + (f.V ? 'V' : '') + (f.R ? 'R' : '') + (f.A ? 'A' : '')) : '').filter(Boolean).join(' ');
      const at = m => { const t = k[0] + 300 + m * 60; let b = null; for (const v of X) { if (v[0] + xSec <= t) b = v; else break; } return b ? sg * (lvl - b[4]) : null; };
      E.push({ period: opt.period, id: opt.period + '|' + new Date(k[0] * 1000).toISOString().slice(0, 16) + '|' + side + '|' + lvl.toFixed(3),
        level: name, lvl, side, idx, t: k[0], session: found.ses.n, offCross,
        overshoot: Math.max(...three.map(v => sg * ((side === 'H' ? v[2] : v[3]) - lvl))),
        rev: three.some(v => sg * (v[4] - lvl) < 0), r30: at(30), r60: at(60), trend: trend(k[0]),
        mr, mv, comp, W, breakFlags: (kF.V ? 'V' : '') + (kF.R ? 'R' : '') + (kF.A ? 'A' : ''),
        preFlagsPit: fmt(pitF), preFlagsLegacy: fmt(legacyF), earlyPit, earlyLegacy,
        early: opt.flagMode === 'legacy' ? earlyLegacy : earlyPit });
    } });
    E.sort((a, b) => a.idx - b.idx);
    const grp = {}; E.forEach(x => (grp[x.idx + x.side] = grp[x.idx + x.side] || []).push(x));
    E.forEach(x => { const g = grp[x.idx + x.side]; x.group = opt.period + '|G' + x.idx + x.side; x.linked = g.length > 1;
      x.primary = g.reduce((o, y) => (x.side === 'H' ? y.lvl > o.lvl : y.lvl < o.lvl) ? y : o) === x; });
    const T = [];
    E.filter(x => x.primary).forEach(x => { for (const mode of ['cont', 'fade']) { const tr = sim(x, mode, M, X); if (tr) T.push(tr); } });
    return { S, levels, E, T };
  }

  function sim(x, mode, M, X) {
    const sg = x.side === 'H' ? 1 : -1; let ent = null, ei = null, ext = -1e9;
    for (let j = x.idx; j < x.idx + C.signalBars; j++) { const v = M[j];
      ext = Math.max(ext, sg * ((x.side === 'H' ? v[2] : v[3]) - x.lvl));
      if (mode === 'cont' ? sg * (v[4] - x.lvl) > 0 : sg * (v[4] - x.lvl) < 0) { ent = v[4]; ei = j; break; } }
    if (ent === null) return null;
    const v = M[ei], dir = mode === 'cont' ? sg : -sg;
    const stop = mode === 'cont' ? (sg > 0 ? v[3] : v[2]) : x.lvl + sg * (ext + C.fadeStopBuffer);
    const risk = Math.abs(ent - stop), tgt = ent + dir * C.rr * risk, tE = v[0] + 300;
    let exit = ent, why = 'time', tx = null;
    for (const b of X) { if (b[0] < tE) continue; if (b[0] >= tE + C.timeExitMin * 60) break;
      const hs = dir > 0 ? b[3] <= stop : b[2] >= stop, ht = dir > 0 ? b[2] >= tgt : b[3] <= tgt;
      if (hs) { exit = stop; why = ht ? 'stop(tie)' : 'stop'; tx = b[0]; break; }
      if (ht) { exit = tgt; why = 'target'; tx = b[0]; break; }
      exit = b[4]; tx = b[0]; }
    const gross = dir * (exit - ent), net = gross - C.costPts;
    return { period: x.period, eventId: x.id, group: x.group, day: new Date((x.t + ukOff(x.t)) * 1000).toISOString().slice(0, 10),
      rule: mode, early: x.early, earlyPit: x.earlyPit, earlyLegacy: x.earlyLegacy, offCross: x.offCross,
      tEntry: tE, entry: ent, stop, target: tgt, risk, tExit: tx, exit, reason: why, gross, cost: C.costPts, net,
      R: net / risk, grossR: gross / risk, costR: C.costPts / risk };
  }

  function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  // Cluster bootstrap of mean per trade; clusterKey: 'group' (linked events) or 'day'.
  function bootCI(trades, field, clusterKey) {
    if (trades.length < 2) return [null, null];
    const cl = {}; trades.forEach(t => (cl[t[clusterKey]] = cl[t[clusterKey]] || []).push(t[field]));
    const keys = Object.keys(cl), r = rng(C.seed), means = [];
    for (let b = 0; b < C.bootstrapN; b++) { let s = 0, n = 0;
      for (let i = 0; i < keys.length; i++) { const g = cl[keys[Math.floor(r() * keys.length)]]; for (const x of g) { s += x; n++; } }
      means.push(s / n); }
    means.sort((a, b) => a - b);
    return [means[Math.floor(0.025 * C.bootstrapN)], means[Math.floor(0.975 * C.bootstrapN) - 1]];
  }

  function maxDD(seq) { let peak = 0, cum = 0, dd = 0; for (const x of seq) { cum += x; peak = Math.max(peak, cum); dd = Math.min(dd, cum - peak); } return dd; }

  function stats(T) {
    if (!T.length) return { n: 0 };
    const s = [...T].sort((a, b) => a.tEntry - b.tEntry), w = s.filter(t => t.net > 0), l = s.filter(t => t.net <= 0);
    const mean = (a, f) => a.reduce((p, t) => p + t[f], 0) / a.length, r2 = x => x === null ? null : +x.toFixed(2);
    const ciG = bootCI(s, 'net', 'group'), ciD = bootCI(s, 'net', 'day'), ciRG = bootCI(s, 'R', 'group');
    return { n: s.length, winRate: +(w.length / s.length).toFixed(3),
      avgWinPts: w.length ? r2(mean(w, 'net')) : null, avgLossPts: l.length ? r2(mean(l, 'net')) : null,
      expPts: r2(mean(s, 'net')), expR: r2(mean(s, 'R')), avgCostR: r2(mean(s, 'costR')), medRiskPts: r2(med(s.map(t => t.risk))),
      totalPts: r2(s.reduce((p, t) => p + t.net, 0)), totalR: r2(s.reduce((p, t) => p + t.R, 0)),
      maxDDPts: r2(maxDD(s.map(t => t.net))), maxDDR: r2(maxDD(s.map(t => t.R))),
      ci95PtsGroup: ciG.map(r2), ci95PtsDay: ciD.map(r2), ci95RGroup: ciRG.map(r2) };
  }

  return { VERSION, CONFIG, pitFlags, sessions, run, sim, stats, bootCI, maxDD };
}
