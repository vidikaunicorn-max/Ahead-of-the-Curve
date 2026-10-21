(function(){
const C=window.CAL; // {A,alpha,beta,rv0,N0,slopeSys,plxTested,plxBias:[[mas,frac],...]}
const $=id=>document.getElementById(id);
const sStat=(N,rv)=>C.s0*Math.pow(N/C.N0,-C.alpha)*Math.pow(rv/C.rv0,-C.beta);
const sSys=dv=>C.slope*dv;
const tot=(N,rv,dv)=>Math.hypot(sStat(N,rv),sSys(dv));
function plxBias(p){const t=C.plxBias;if(p<=t[0][0])return t[0][1];for(let i=1;i<t.length;i++)if(p<=t[i][0]){const a=t[i-1],b=t[i];return a[1]+(b[1]-a[1])*(p-a[0])/(b[0]-a[0]);}return null}
const f3=x=>x.toFixed(3);
function nStar(rv,dv){const sy=sSys(dv);return sy>0?C.N0*Math.pow(sy/(C.s0*Math.pow(rv/C.rv0,-C.beta)),-1/C.alpha):Infinity}
function nFor(target,rv,dv){const sy=sSys(dv);if(target<=sy)return null;const a=Math.sqrt(target*target-sy*sy);return C.N0*Math.pow(a/(C.s0*Math.pow(rv/C.rv0,-C.beta)),-1/C.alpha)}
function fmt(n){return n>=1e5?(n/1e3).toFixed(0)+"k":Math.round(n).toLocaleString("en")}
function draw(){
 const N=Math.pow(10,+$("n").value),rv=+$("rv").value,plx=+$("plx").value,dv=+$("dv").value,tg=+$("tgt").value;
 $("nO").textContent=fmt(N);$("rvO").textContent=Math.round(rv*100)+"%";$("plxO").textContent=plx.toFixed(2)+" mas";$("dvO").textContent="±"+dv.toFixed(2)+" mag";$("tgtO").textContent=tg.toFixed(3);
 const S=sStat(N,rv),Y=sSys(dv),T=Math.hypot(S,Y);
 $("kS").textContent=f3(S);$("kY").textContent=f3(Y);$("kT").textContent=f3(T);
 $("eb").innerHTML=`Forecast: ρ<sub>0</sub> = ${C.rho0.toFixed(3)} ± ${f3(S)} (stat) ± ${f3(Y)} (sys)`;$("kTs").textContent="relative to ρ₀ = 0.063: "+Math.round(T/C.rho0*100)+"%";
 const ns=nStar(rv,dv),nt=nFor(tg,rv,dv);
 let v=`Statistical and systematic errors are equal at <b>N* ≈ ${fmt(ns)}</b> stars. `;
 v+= N<ns?`You are statistics-limited: more stars still help.`:`You are calibration-limited: more stars give diminishing returns; tighten the completeness limit instead.`;
 v+= nt===null?` The target of ${f3(tg)} cannot be reached at this completeness uncertainty (floor ${f3(Y)}).`:` To reach ${f3(tg)} you need about <b>${fmt(nt)}</b> stars.`;
 $("verdict").innerHTML=v;
 const b=plxBias(plx);let w="";
 if(b!==null&&b>0.01)w=`<div class="note warn">At σ<sub>ϖ</sub> = ${plx.toFixed(2)} mas, mock tests show ρ₀ is biased high by roughly ${Math.round(b*100)}%. The error bars above do not include this bias.</div>`;
 $("warn").innerHTML=w;
 // chart
 const W=640,H=340,L=56,R=16,Tp=16,B=44,xmin=2.7,xmax=5.2,ymax=Math.max(0.06,sStat(Math.pow(10,xmin),rv)*1.05);
 const X=x=>L+(x-xmin)/(xmax-xmin)*(W-L-R),Yp=y=>H-B-y/ymax*(H-Tp-B);
 let s="";
 for(let i=0;i<=4;i++){const y=ymax*i/4;s+=`<line class="gridl" x1="${L}" x2="${W-R}" y1="${Yp(y)}" y2="${Yp(y)}"/><text x="${L-8}" y="${Yp(y)+4}" text-anchor="end">${y.toFixed(3)}</text>`}
 for(let x=3;x<=5;x++)s+=`<text x="${X(x)}" y="${H-B+18}" text-anchor="middle">10<tspan dy="-5" font-size="9">${x}</tspan></text>`;
 s+=`<text x="${(L+W-R)/2}" y="${H-6}" text-anchor="middle">Number of stars</text><text transform="translate(14 ${(Tp+H-B)/2}) rotate(-90)" text-anchor="middle">σ(ρ₀)  [M☉ pc⁻³]</text>`;
 const pts=f=>{let p="";for(let x=xmin;x<=xmax+1e-9;x+=0.02)p+=(p?"L":"M")+X(x).toFixed(1)+" "+Yp(Math.min(f(Math.pow(10,x)),ymax)).toFixed(1);return p};
 s+=`<path d="${pts(n=>sStat(n,rv))}" fill="none" stroke="var(--stat)" stroke-width="2"/><path d="${pts(()=>Y)}" fill="none" stroke="var(--sys)" stroke-width="2" stroke-dasharray="6 4"/><path d="${pts(n=>Math.hypot(sStat(n,rv),Y))}" fill="none" stroke="var(--tot)" stroke-width="2.6"/>`;
 s+=`<line x1="${L}" x2="${W-R}" y1="${Yp(tg)}" y2="${Yp(tg)}" stroke="var(--ok)" stroke-dasharray="1 4" stroke-width="1.6"/><text x="${W-R-4}" y="${Yp(tg)-5}" text-anchor="end" style="fill:var(--ok)">target</text>`;
 const lx=Math.log10(ns);if(lx>xmin&&lx<xmax&&Y>0)s+=`<circle cx="${X(lx)}" cy="${Yp(Math.hypot(Y,Y))}" r="5" fill="none" stroke="var(--tot)" stroke-width="2"/><text x="${X(lx)+8}" y="${Yp(Math.hypot(Y,Y))-8}">N*</text>`;
 s+=`<circle cx="${X(Math.log10(N))}" cy="${Yp(T)}" r="5.5" fill="var(--accent2)"/>`;
 s+=`<g transform="translate(${L+10} ${Tp+6})"><line x2="22" stroke="var(--stat)" stroke-width="2"/><text x="28" y="4">statistical</text><line y1="16" y2="16" x2="22" stroke="var(--sys)" stroke-width="2" stroke-dasharray="6 4"/><text x="28" y="20">completeness systematic</text><line y1="32" y2="32" x2="22" stroke="var(--tot)" stroke-width="2.6"/><text x="28" y="36">total</text></g>`;
 $("chart").innerHTML=s;
}
function paper(){$("n").value=Math.log10(3585);$("rv").value=0.59;$("plx").value=0.8;$("dv").value=0.3;$("tgt").value=0.02;draw()}
["n","rv","plx","dv","tgt"].forEach(i=>$(i).addEventListener("input",draw));
$("paper").addEventListener("click",paper);paper();
})();
