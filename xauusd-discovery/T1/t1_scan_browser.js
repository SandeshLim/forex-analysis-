// T1 scanner — run in the TradingView page console (OANDA:XAUUSD).
// Needs window.__D = {'1':[[t,o,h,l,c,v]...], '60':[...], '240':[...]} loaded from the chart.
// window.__t1scan(dayStartUnix, dayEndUnix) returns one line per completed 1H candle in trend.
(function(){
const D=window.__D; const B=D['1'], H=D['60'], F=D['240']; const f=t=>new Date(t*1000).toISOString().slice(5,16).replace('T',' ');
function piv(X,n,step){const P=[];for(let i=n;i<X.length-n;i++){let hi=true,lo=true;for(let k=1;k<=n;k++){if(!(X[i][2]>X[i-k][2]&&X[i][2]>=X[i+k][2]))hi=false;if(!(X[i][3]<X[i-k][3]&&X[i][3]<=X[i+k][3]))lo=false;}const ct=X[i+n][0]+step;if(hi)P.push({k:'H',p:X[i][2],ct});if(lo)P.push({k:'L',p:X[i][3],ct});}return P;}
const P4=piv(F,3,4*3600), P1=piv(H,3,3600);
const ev=[]; for(let i=0;i<F.length;i++){const hs=P4.filter(x=>x.k==='H'&&x.ct<=F[i][0]),ls=P4.filter(x=>x.k==='L'&&x.ct<=F[i][0]);const h=hs.at(-1),l=ls.at(-1);const ct=F[i][0]+4*3600;if(h&&F[i][4]>h.p)ev.push({t:ct,d:1});if(l&&F[i][4]<l.p)ev.push({t:ct,d:-1});}
const tr4=t=>{let d=0;for(const e of ev){if(e.t<=t)d=e.d;else break;}return d;};
const tr1=t=>{const hs=P1.filter(x=>x.k==='H'&&x.ct<=t).slice(-2), ls=P1.filter(x=>x.k==='L'&&x.ct<=t).slice(-2); if(hs.length<2||ls.length<2) return 0; if(hs[1].p<hs[0].p) return -1; if(ls[1].p>ls[0].p) return 1; return 0;};
window.__t1scan=function(dayStart,dayEnd){ const out=[];
for(const R of H){ const t0=R[0]+3600; if(t0<dayStart||t0>Math.min(dayEnd,B.at(-1)[0])) continue; const d4=tr4(t0), d1=tr1(t0); if(!d4||d4!==d1) continue; const dir=d4;
 const rg=R[2]-R[3], mid=(R[2]+R[3])/2, zlo=mid-0.05*rg, zhi=mid+0.05*rg; const tgt=dir<0?R[3]:R[2];
 const bars=B.filter(x=>x[0]>=t0&&x[0]<t0+3600); let touched=false, pk=null, res=null;
 for(const x of bars){ const inZ=dir<0?x[2]>=zlo:x[3]<=zhi; if(!touched&&(dir<0?x[3]<=tgt:x[2]>=tgt)){res='no trade: target reached first';break;}
  if(dir<0?x[4]>zhi:x[4]<zlo){res='no trade: 1m close beyond zone '+f(x[0]).slice(6);break;}
  if(inZ){touched=true; if(!pk||(dir<0?x[2]>pk[2]:x[3]<pk[3])) pk=x; continue;}
  if(touched&&pk&&(dir<0?x[4]<pk[3]:x[4]>pk[2])){ const E=x[4], S=dir<0?zhi+0.5:zlo-0.5, Rk=Math.abs(S-E), rew=Math.abs(E-tgt)/Rk; if(rew<1){res='trigger '+f(x[0]).slice(6)+' skipped (reward '+rew.toFixed(2)+'R)'; continue;}
   let o='timeout', mfe=0; const k0=B.findIndex(y=>y[0]===x[0]); for(let q=k0+1;q<B.length&&q<k0+180;q++){const y=B[q]; if(dir<0?y[2]>=S:y[3]<=S){o='STOP '+f(y[0]).slice(6)+' -1R';break;} mfe=Math.max(mfe,dir<0?(E-y[3])/Rk:(y[2]-E)/Rk); if(dir<0?y[3]<=tgt:y[2]>=tgt){o='TARGET '+f(y[0]).slice(6)+' +'+rew.toFixed(2)+'R';break;}}
   res=(dir<0?'SELL ':'BUY ')+f(x[0]).slice(6)+' E'+E.toFixed(2)+' S'+S.toFixed(2)+' risk '+Rk.toFixed(1)+' -> '+o+' (MFE '+mfe.toFixed(1)+'R)'; break; } }
 out.push(f(R[0]).slice(6)+' 1H H'+R[2].toFixed(1)+' L'+R[3].toFixed(1)+' mid '+mid.toFixed(1)+' ('+(dir<0?'down':'up')+'): '+(res||(touched?'touched, no trigger':'no touch')));
} return out; };
})();
