function claudeLiveLogger() {
  // Study 3 live/back-fill event logger (EXPLORATORY). Runs in the TradingView chart page on the 1m main series.
  // Every event is defined from closed bars only and stamped with the bar it was recognisable at and, when found
  // live, the wall-clock time it was detected. Outcomes are filled in later from subsequent bars.
  const VERSION = 'live-1.0.0';
  const L = { version: VERSION, ev: [], zones: [], started: Date.now(), lastT: 0, mode: 'backfill', errors: [], ticks: 0 };
  const med = a => { const s = a.slice().sort((x, y) => x - y); return s[s.length >> 1]; };
  const lastSun = (y, m) => { const d = new Date(Date.UTC(y, m + 1, 0)); return Date.UTC(y, m, d.getUTCDate() - d.getUTCDay()) / 1000; };
  const ukOff = t => { const y = new Date(t * 1000).getUTCFullYear(); return (t >= lastSun(y, 2) + 3600 && t < lastSun(y, 9) + 3600) ? 3600 : 0; };
  const nthSun = (y, m, n) => { const d = new Date(Date.UTC(y, m, 1)); return Date.UTC(y, m, 1 + (7 - d.getUTCDay()) % 7 + 7 * (n - 1)) / 1000; };
  const nyDst = t => { const y = new Date(t * 1000).getUTCFullYear(); return t >= nthSun(y, 2, 2) + 7 * 3600 && t < nthSun(y, 10, 1) + 6 * 3600; };
  const tday = t => Math.floor((t - (nyDst(t) ? 21 : 22) * 3600) / 86400) + 1;
  const weekOf = td => Math.floor((td - 4) / 7);
  const sessOf = t => { const u = t + ukOff(t); const h = Math.floor(u / 3600) % 24, d = Math.floor(u / 86400);
    return h < 7 ? ['Asia', d, 7] : h < 12 ? ['London', d, 12] : h < 17 ? ['NewYork', d, 17] : ['Late', d, 24]; };
  // sweep state
  const A = { t: [], o: [], h: [], l: [], c: [] };
  let cur = null, done = {}, dayCur = null, dayPrev = null, wkCur = null, wkPrev = null;
  let h1 = null, H1 = [], h4 = null, H4 = [];
  const pendS2 = [];
  const fmt = t => new Date(t * 1000).toISOString().slice(0, 16).replace('T', ' ');

  function addEvent(e, k) {
    e.barTime = A.t[k]; e.recognisedAt = A.t[k] + 60; e.mode = L.mode;
    e.detectedAt = L.mode === 'live' ? Math.round(Date.now() / 1000) : null;
    e.risk = Math.abs(e.entry - e.stop); e.out = { mfeR: 0, maeR: 0, first: null, hits: {} };
    if (e.risk > 0) L.ev.push(e);
  }
  function updateOutcomes(k) {
    const t = A.t[k];
    for (const e of L.ev) {
      if (e.closed || t <= e.barTime) continue;
      const mins = (t + 60 - e.recognisedAt) / 60, d = e.dir, r = e.risk;
      const fav = d > 0 ? A.h[k] - e.entry : e.entry - A.l[k], adv = d > 0 ? e.entry - A.l[k] : A.h[k] - e.entry;
      e.out.mfeR = Math.max(e.out.mfeR, fav / r); e.out.maeR = Math.max(e.out.maeR, adv / r);
      if (!e.out.first) {
        if (adv >= r) e.out.first = 'stop@' + Math.round(mins);
        else for (const m of [1, 2, 3]) if (fav >= m * r && !e.out.hits[m]) e.out.hits[m] = Math.round(mins);
        if (!e.out.first && e.out.hits[3]) e.out.first = '3R@' + e.out.hits[3];
      }
      for (const hm of [15, 30, 60, 240]) if (mins >= hm && e.out['R' + hm] === undefined) {
        e.out['R' + hm] = +(d * (A.c[k] - e.entry) / r).toFixed(2); e.out['mr' + hm] = +(d * (A.c[k] - e.entry) / e.mr).toFixed(2); }
      if (mins >= 240) e.closed = true;
    }
  }
  function process(bar) {
    const [t, o, h, l, c] = bar; const k = A.t.length;
    A.t.push(t); A.o.push(o); A.h.push(h); A.l.push(l); A.c.push(c);
    if (k < 61) { roll(k); return; }
    const mr = med(A.h.slice(k - 60, k).map((x, i) => x - A.l[k - 60 + i]));
    // ---------- F1: 1m two-candle sequence (stage 1) at bar k, and stage-2 confirmations ----------
    for (const p of pendS2.splice(0)) {
      if (k - p.k > 3) continue;
      const sg = p.sg, ext = p.ext;
      if (sg * (c - ext) > 0) continue;                                     // invalidated
      const body = Math.abs(c - o), rg = h - l;
      if (sg * (c - o) < 0 && body >= 0.5 * rg && rg >= 1.5 * p.mr && sg * (c - (sg > 0 ? A.l[p.k] : A.h[p.k])) < 0) {
        addEvent(Object.assign({}, p.base, { fam: 'F1', stage: 2, entry: c, stop: ext + sg * 0.1 * p.mr, already_mr: +(-sg * (c - A.c[p.k]) / p.mr).toFixed(2) }), k);
      } else pendS2.push(p);
    }
    const k1 = k - 1, rg1 = A.h[k1] - A.l[k1], b1 = Math.abs(A.c[k1] - A.o[k1]), b2 = Math.abs(c - o);
    for (const sg of [1, -1]) {
      const strong = sg * (A.c[k1] - A.o[k1]) > 0 && b1 >= 0.5 * rg1 && rg1 >= 1.5 * mr;
      if (!(strong && sg * (c - o) < 0 && b2 <= 0.5 * b1)) continue;
      const ri = h <= A.h[k1] && l >= A.l[k1];
      const bi = Math.max(o, c) <= Math.max(A.o[k1], A.c[k1]) && Math.min(o, c) >= Math.min(A.o[k1], A.c[k1]);
      const ext = sg > 0 ? Math.max(h, A.h[k1]) : Math.min(l, A.l[k1]);
      const ctx = [];
      for (const nm of ['Asia', 'London', 'NewYork']) if (done[nm]) {
        const Lv = sg > 0 ? done[nm].hi : done[nm].lo;
        if (sg * (ext - Lv) >= -0.25 * mr && sg * (A.c[k - 2] - Lv) < -0.25 * mr) ctx.push('completed ' + nm + (sg > 0 ? ' high' : ' low'));
      }
      for (const [nm, P] of [['prev day', dayPrev], ['prev week', wkPrev]]) if (P) {
        const Lv = sg > 0 ? P.hi : P.lo;
        if (sg * (ext - Lv) >= -0.25 * mr && sg * (A.c[k - 2] - Lv) < -0.25 * mr) ctx.push(nm + (sg > 0 ? ' high' : ' low'));
      }
      if (cur && cur.n >= 15) {                                              // developing session extreme made by B1/B2
        const ex = sg > 0 ? cur.hiPrev : cur.loPrev, stood = sg > 0 ? cur.hiStood : cur.loStood;
        if (ex !== null && sg * (ext - ex) > 0 && stood >= 15) ctx.push('developing ' + cur.name + (sg > 0 ? ' high' : ' low') + ' (stood ' + stood + 'm)');
      }
      for (const z of L.zones) if (A.t[k] - z.formed >= 14400 && z.dir === -sg && ext >= z.lo && ext <= z.hi) ctx.push(z.tf + ' zone ' + fmt(z.formed));
      const base = { sg, ctype: ri ? 'range_inside' : bi ? 'body_inside_only' : 'not_contained', ctx: ctx.length ? ctx : ['away'], mr: +mr.toFixed(3), ext };
      addEvent(Object.assign({}, base, { fam: 'F1', stage: 1, dir: -sg, entry: c, stop: ext + sg * 0.1 * mr }), k);
      pendS2.push({ k, sg, ext, mr, base: Object.assign({ dir: -sg }, base) });
    }
    // ---------- F2: first trade beyond a standing developing session extreme ----------
    const [sn, sd] = sessOf(t);
    if (cur && cur.name === sn && cur.d === sd && sn !== 'Late') {
      for (const sg of [1, -1]) {
        const ex = sg > 0 ? cur.hi : cur.lo, stood = k - (sg > 0 ? cur.hiI : cur.loI);
        if (stood >= 15 && sg * ((sg > 0 ? h : l) - ex) > 0)
          addEvent({ fam: 'F2', sg, dir: -sg, ctx: ['session ' + sn + (sg > 0 ? ' high' : ' low') + ' stood ' + stood + 'm'], mr: +mr.toFixed(3),
                     pen_mr: +(sg * ((sg > 0 ? h : l) - ex) / mr).toFixed(2), closedBackInside: sg * (c - ex) < 0, entry: c,
                     stop: (sg > 0 ? h : l) + sg * 0.1 * mr, level: ex }, k);
      }
    }
    // ---------- F3: revisit of an earlier 1h/4h displacement-candle body ----------
    for (const z of L.zones) {
      if (z.dead || A.t[k] - z.formed < 14400) continue;
      const prevC = A.c[k - 1];
      const entering = z.dir > 0 ? (prevC > z.hi && l <= z.hi) : (prevC < z.lo && h >= z.lo);
      if (entering) { z.visits++;
        addEvent({ fam: 'F3', sg: -z.dir, dir: z.dir, ctx: [z.tf + ' ' + (z.dir > 0 ? 'bullish' : 'bearish') + ' zone from ' + fmt(z.formed) + ', visit ' + z.visits],
                   mr: +mr.toFixed(3), entry: c, stop: (z.dir > 0 ? z.lo : z.hi) - z.dir * 0.1 * mr, zone: [z.lo, z.hi] }, k); }
      if (z.dir > 0 ? c < z.lo : c > z.hi) z.dead = true;                   // closed through the far side
    }
    updateOutcomes(k);
    roll(k);
  }
  function roll(k) {
    const t = A.t[k], h = A.h[k], l = A.l[k], o = A.o[k], c = A.c[k];
    const [sn, sd, eh] = sessOf(t);
    if (!cur || cur.name !== sn || cur.d !== sd) {
      if (cur && cur.name !== 'Late') done[cur.name] = { hi: cur.hi, lo: cur.lo, d: cur.d };
      cur = { name: sn, d: sd, hi: h, lo: l, hiI: k, loI: k, n: 0, hiPrev: null, loPrev: null, hiStood: 0, loStood: 0 };
    } else {
      cur.hiPrev = cur.hi; cur.loPrev = cur.lo; cur.hiStood = k - cur.hiI; cur.loStood = k - cur.loI;
      if (h > cur.hi) { cur.hi = h; cur.hiI = k; } if (l < cur.lo) { cur.lo = l; cur.loI = k; }
    }
    cur.n++;
    const td = tday(t);
    if (!dayCur || dayCur.td !== td) { if (dayCur) dayPrev = dayCur; dayCur = { td, hi: h, lo: l }; }
    else { dayCur.hi = Math.max(dayCur.hi, h); dayCur.lo = Math.min(dayCur.lo, l); }
    const wk = weekOf(td);
    if (!wkCur || wkCur.wk !== wk) { if (wkCur) wkPrev = wkCur; wkCur = { wk, hi: h, lo: l }; }
    else { wkCur.hi = Math.max(wkCur.hi, h); wkCur.lo = Math.min(wkCur.lo, l); }
    for (const [tf, sec, off, list] of [['1h', 3600, 0, H1], ['4h', 14400, 22 * 3600, H4]]) {
      const bucket = Math.floor((t - off) / sec);
      let st = tf === '1h' ? h1 : h4;
      if (!st || st.b !== bucket) {
        if (st) { list.push(st); if (list.length > 21) {
          const prev = list.slice(-21, -1), mrg = med(prev.map(x => x.h - x.l)), rg = st.h - st.l, bd = Math.abs(st.c - st.o);
          if (rg >= 2 * mrg && bd >= 0.6 * rg) L.zones.push({ tf, dir: st.c > st.o ? 1 : -1, lo: Math.min(st.o, st.c), hi: Math.max(st.o, st.c), formed: (st.b + 1) * sec + off, visits: 0 });
        } }
        st = { b: bucket, o, h, l, c };
      } else { st.h = Math.max(st.h, h); st.l = Math.min(st.l, l); st.c = c; }
      if (tf === '1h') h1 = st; else h4 = st;
    }
  }
  function bars() { const ms = TradingViewApi._activeChartWidgetWV.value()._chartWidget.model().mainSeries(); const b = ms.bars(), a = [];
    for (let i = b.firstIndex(); i <= b.lastIndex(); i++) { const v = b.valueAt(i); if (v) a.push(v.slice(0, 5)); } return a; }
  function tick() {
    try { L.ticks++; const a = bars(), now = Date.now() / 1000;
      for (const v of a) if (v[0] > L.lastT && v[0] + 60 <= now - 2) { process(v); L.lastT = v[0]; }
      try { localStorage.setItem('claudeLiveLogger', JSON.stringify({ v: VERSION, at: Date.now(), ev: L.ev.slice(-3000) })); } catch (e) {}
    } catch (e) { L.errors.push(String(e).slice(0, 200)); }
  }
  L.backfill = () => { L.mode = 'backfill'; tick(); L.mode = 'live'; };
  L.start = (ms = 20000) => { if (L.timer) clearInterval(L.timer); L.timer = setInterval(tick, ms); };
  L.stop = () => clearInterval(L.timer);
  L.fmt = fmt;
  return L;
}
