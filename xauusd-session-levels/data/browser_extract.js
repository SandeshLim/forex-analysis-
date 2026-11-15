// Run in the DevTools/console of a TradingView chart showing OANDA:XAUUSD (chart timezone irrelevant; bars are UTC).
// Loads older history for the current resolution and returns [time, open, high, low, close, volume] rows.
// Used for: 5m (to 2026-08-02), 1m (to 2026-10-25), 240 (to 2026-06-03). Bar counts are capped by the TradingView plan (~20k).
async function extractBars(pages = 10) {
  const ms = TradingViewApi._activeChartWidgetWV.value()._chartWidget.model().mainSeries();
  for (let i = 0; i < pages && ms.requestMoreDataAvailable(); i++) { ms.requestMoreData(2500); await new Promise(r => setTimeout(r, 2500)); }
  const b = ms.bars(), out = [];
  for (let i = b.firstIndex(); i <= b.lastIndex(); i++) { const v = b.valueAt(i); if (v) out.push(v.slice(0, 6)); }
  return out;
}
// Fingerprint used in data/MANIFEST.md: sha256 of rows joined as "t,o,h,l,c,v" with "\n" separators.
async function sha256Rows(rows) {
  const s = rows.map(v => v.join(',')).join('\n');
  return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))).map(b => b.toString(16).padStart(2, '0')).join('');
}
