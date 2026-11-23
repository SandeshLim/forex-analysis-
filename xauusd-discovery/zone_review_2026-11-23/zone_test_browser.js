// Run in the TradingView page console with OANDA:XAUUSD loaded.
// window.__D must hold bars per resolution: {'15':[[t,o,h,l,c,v],...], '60':..., '240':...}
// Exploratory test run on 23 Nov 2026 (latest 1H bar 21:00 UK). Rules fixed before results were read,
// but chosen after seeing the 23 Nov example: treat as exploratory, not validation.
const COST = 0.4, TGT = 2;
function atr14(H){const a=[];let x=null;for(let i=0;i<H.length;i++){const tr=i?Math.max(H[i][2]-H[i][3],Math.abs(H[i][2]-H[i-1][4]),Math.abs(H[i][3]-H[i-1][4])):H[i][2]-H[i][3];x=x===null?tr:(x*13+tr)/14;a.push(x);}return a;}
// 4H swing points: high/low beyond 3 candles each side; confirmed at close of 3rd candle after.
function pivots(F,n=3){const P=[];for(let i=n;i<F.length-n;i++){let hi=true,lo=true;for(let k=1;k<=n;k++){if(!(F[i][2]>F[i-k][2]&&F[i][2]>=F[i+k][2]))hi=false;if(!(F[i][3]<F[i-k][3]&&F[i][3]<=F[i+k][3]))lo=false;}const ct=F[i+n][0]+4*3600;if(hi)P.push({k:'H',p:F[i][2],ct});if(lo)P.push({k:'L',p:F[i][3],ct});}return P;}
// Trend = direction of the latest 4H close beyond the latest confirmed swing high/low (break of structure).
function bosEvents(F,P){const ev=[];for(let i=0;i<F.length;i++){const ct=F[i][0]+4*3600;const hs=P.filter(x=>x.k==='H'&&x.ct<=F[i][0]),ls=P.filter(x=>x.k==='L'&&x.ct<=F[i][0]);const h=hs[hs.length-1],l=ls[ls.length-1];if(h&&F[i][4]>h.p)ev.push({t:ct,d:1,ref:h.p});if(l&&F[i][4]<l.p)ev.push({t:ct,d:-1,ref:l.p});}return ev;}
function trendAt(ev,t){let d=0;for(const e of ev){if(e.t<=t)d=e.d;else break;}return d;}
// 1H zones: base of 2-6 candles, height <= 1.2 ATR, no body > 0.8 ATR; next candle closes beyond base.
// Sell zone: proximal = highest body edge, distal = highest wick. Buy zone mirrored.
function zones(H,atr){const Z=[];let lastEnd=-1;for(let i=20;i<H.length;i++){for(let L=6;L>=2;L--){const s=i-L;if(s<=lastEnd)continue;const b=H.slice(s,i);const bh=Math.max(...b.map(x=>x[2])),bl=Math.min(...b.map(x=>x[3]));const A=atr[i-1];if(bh-bl>1.2*A)continue;if(b.some(x=>Math.abs(x[4]-x[1])>0.8*A))continue;const c=H[i];let dir=0;if(c[4]<bl)dir=-1;else if(c[4]>bh)dir=1;if(!dir)continue;const prox=dir<0?Math.max(...b.map(x=>Math.max(x[1],x[4]))):Math.min(...b.map(x=>Math.min(x[1],x[4])));Z.push({dir,s:H[s][0],t:c[0]+3600,prox,dist:dir<0?bh:bl,i});lastEnd=i;break;}}return Z;}
// Outcomes: first touch = limit at proximal, stop distal +/- 0.5 (variant: +/- 0.25 ATR); touch bar reaching stop = loss.
// Confirmation (15m, data from 19 Oct): after the 15m touch, first 15m candle within 2h that closes back beyond proximal,
// against the touch, and beyond the prior 15m candle's low/high; stop = touch extreme +/- 0.5; a 15m close beyond distal cancels.
// Target 2R, timeout 48h; cost 0.4 points per trade; stop assumed before target inside a bar.
