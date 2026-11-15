function(M, X, H4, dayFrom, dayTo, opt){
 opt=opt||{}; const COST=0.3, RR=1.5, BUF=0.5;
 const ukOff=t=> (t < Date.UTC(2026,9,25,1)/1000 && t >= Date.UTC(2026,2,29,1)/1000) ? 3600 : 0; // BST 29 Mar - 25 Oct 2026
 const ema=(a,n)=>{let k=2/(n+1),e=a[0];return a.map(x=>e=x*k+e*(1-k));}; const e4=ema(H4.map(v=>v[4]),20);
 const trend=t=>{let i=H4.findIndex(v=>v[0]+14400>t)-1; if(i<5) return '?'; const c=H4[i][4],e=e4[i],sl=e4[i]-e4[i-3]; return (c>e&&sl>0)?'Up':(c<e&&sl<0)?'Down':'Mixed';};
 const med=a=>{const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)];};
 const SES=[['Asia',0,7],['London',7,12],['New York',12,17]]; const S=[];
 for(let d=Date.UTC(...dayFrom)/1000; d<=Date.UTC(...dayTo)/1000; d+=86400){ const dow=new Date(d*1000).getUTCDay(); if(dow==0||dow==6) continue;
  const off=ukOff(d+12*3600);
  for(const [n,a,b] of SES){ const s=d+a*3600-off,e=d+b*3600-off; const bs=M.filter(v=>v[0]>=s&&v[0]<e); if(!bs.length) continue;
   S.push({day:new Date(d*1000).toISOString().slice(0,10),n,s,e,hi:Math.max(...bs.map(v=>v[2])),lo:Math.min(...bs.map(v=>v[3])),nb:bs.length});}}
 const T=[];
 S.forEach((src,i)=>{ for(const side of ['H','L']){ const lvl=side=='H'?src.hi:src.lo; const sg=side=='H'?1:-1; let found=null;
  for(const ses of S.slice(i+1,i+3)){ const idx=M.findIndex(v=>v[0]>=ses.s&&v[0]<ses.e&&sg*((side=='H'?v[2]:v[3])-lvl)>0); if(idx>=0){found={idx,ses};break;} }
  if(!found){ T.push({src:src.day+' '+src.n+' '+(side=='H'?'high':'low'),lvl,side,tested:false}); continue; }
  const idx=found.idx,k=M[idx];
  // was the level crossed outside session hours before this break?
  const offCross=M.some(v=>v[0]>=src.e&&v[0]<k[0]&&sg*((side=='H'?v[2]:v[3])-lvl)>0);
  const three=M.slice(idx,idx+3); const rev=three.some(v=>sg*(v[4]-lvl)<0);
  const over=Math.max(...three.map(v=>sg*((side=='H'?v[2]:v[3])-lvl)));
  const at=m=>{const t=k[0]+300+m*60; let b=null; for(const v of X){ if(v[0]+(X===M?300:60)<=t) b=v; else break;} return b?+(sg*(lvl-b[4])).toFixed(2):null;};
  const prev=M.slice(Math.max(0,idx-24),idx); const mr=med(prev.map(v=>v[2]-v[3])), mv=med(prev.map(v=>v[5]));
  const flags=v=>({V:v[5]>2*mv,R:(v[2]-v[3])>2*mr,A:v[5]>1.5*mv&&(v[2]-v[3])<0.75*mr});
  const pre3=M.slice(idx-3,idx), pre6=M.slice(idx-6,idx);
  const C=pre6.length==6&&(pre6.reduce((a,v)=>a+v[2]-v[3],0)/6)<0.6*mr;
  const preF=pre3.map(flags), kF=flags(k);
  const r=k[2]-k[3], wk=side=='H'?k[2]-Math.max(k[1],k[4]):Math.min(k[1],k[4])-k[3]; const W=r>0&&wk/r>=0.6&&sg*(k[4]-lvl)<0;
  const early=preF.some(f=>f.V||f.R||f.A)||C;
  const codes=['V','R','A'].filter(c=>preF.some(f=>f[c])||kF[c]).join('')+(W?'W':'')+(C?'C':'');
  T.push({src:src.day+' '+src.n+' '+(side=='H'?'high':'low'),lvl,side,tested:true,idx,t:k[0],ses:found.ses.n,over,rev,r30:at(30),r60:at(60),tr:trend(k[0]),codes,early,offCross,mr,mv});
 }});
 const TT=T.filter(x=>x.tested).sort((a,b)=>a.idx-b.idx);
 // linked: same 5m candle & side -> one trade on outermost level
 const grp={}; TT.forEach(x=>{const g=x.idx+x.side; (grp[g]=grp[g]||[]).push(x);});
 TT.forEach(x=>{const g=grp[x.idx+x.side]; x.linked=g.length>1; const out=g.reduce((o,y)=>(x.side=='H'?y.lvl>o.lvl:y.lvl<o.lvl)?y:o); x.primary=(out===x);});
 const sim=(x,mode)=>{ const sg=x.side=='H'?1:-1; let ent=null,ei=null,ext=-1e9;
  for(let j=x.idx;j<x.idx+3;j++){const v=M[j]; ext=Math.max(ext,sg*((x.side=='H'?v[2]:v[3])-x.lvl)); if(mode=='c'?sg*(v[4]-x.lvl)>0:sg*(v[4]-x.lvl)<0){ent=v[4];ei=j;break;}}
  if(ent===null) return null; const v=M[ei]; const dir=mode=='c'?sg:-sg;
  const stop=mode=='c'?(sg>0?v[3]:v[2]):x.lvl+sg*(ext+BUF); const risk=Math.abs(ent-stop); const tgt=ent+dir*RR*risk;
  const tE=v[0]+300; let exit=ent,why='time',tx=null;
  for(const b of X){ if(b[0]<tE) continue; if(b[0]>=tE+3600) break; const hs=dir>0?b[3]<=stop:b[2]>=stop, ht=dir>0?b[2]>=tgt:b[3]<=tgt; if(hs){exit=stop;why='stop';tx=b[0];break;} if(ht){exit=tgt;why='target';tx=b[0];break;} exit=b[4]; tx=b[0]; }
  return {tEntry:tE,ent,stop,tgt,risk,exit,why,tExit:tx,gross:dir*(exit-ent),pnl:dir*(exit-ent)-COST};};
 TT.forEach(x=>{ if(x.primary){ x.cont=sim(x,'c'); x.fade=sim(x,'f'); } });
 return {S,T,TT};
}
