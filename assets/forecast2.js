(function(){
const C=window.CAL2,T=C.rho0,$=id=>document.getElementById(id);
const sc=C.stat.coef,bc=C.bias.coef,D=C.domain;
const stat=(N,rv,p)=>C.stat.anchor*Math.exp(sc[0]+sc[1]*Math.log(N/3585)+sc[2]*Math.log(rv/0.6)+sc[3]*p+sc[4]*p*p);
const slope=p=>Math.abs((bc[1]+bc[5]*p)*T)*C.bias.anchor;
const shift=p=>Math.abs((bc[3]*(p-C.plx0)+bc[4]*(p*p-C.plx0*C.plx0))*T);
function budget(o){const s=stat(o.N,o.rv,o.plx),y=slope(o.plx)*o.dv,q=o.corr?0:shift(o.plx);
 const sl=s*Math.exp(-C.stat.resid),sh=s*Math.exp(C.stat.resid);
 return{s,y,q,t:Math.hypot(s,y,q),lo:Math.hypot(sl,y,q),hi:Math.hypot(sh,y,q)}}
const f3=x=>x.toFixed(3);
const fmt=n=>!isFinite(n)?"∞":n>=1e6?(n/1e6).toFixed(1)+"M":n>=1e5?Math.round(n/1e3)+"k":Math.round(n).toLocaleString("en");
function solveN(o,tg){const fl=Math.hypot(slope(o.plx)*o.dv,o.corr?0:shift(o.plx));if(tg<=fl)return null;const a=Math.sqrt(tg*tg-fl*fl);
 let lo=1,hi=1e9;for(let i=0;i<80;i++){const m=Math.sqrt(lo*hi);stat(m,o.rv,o.plx)>a?lo=m:hi=m}return Math.sqrt(lo*hi)}
function nstar(o){const fl=Math.hypot(slope(o.plx)*o.dv,o.corr?0:shift(o.plx));if(fl<=0)return Infinity;let lo=1,hi=1e9;for(let i=0;i<80;i++){const m=Math.sqrt(lo*hi);stat(m,o.rv,o.plx)>fl?lo=m:hi=m}return Math.sqrt(lo*hi)}
function get(){return{N:Math.pow(10,+$("n").value),rv:+$("rv").value,plx:+$("plx").value,dv:+$("dv").value,tg:+$("tgt").value,corr:$("corr").checked}}
function set(o){$("n").value=Math.log10(o.N);$("rv").value=o.rv;$("plx").value=o.plx;$("dv").value=o.dv;if(o.tg!=null)$("tgt").value=o.tg;draw()}
const PAPER={N:3585,rv:0.59,plx:0.8,dv:0.3,tg:0.02};
const rows=[];
function chart(o,b){
 const W=680,H=350,L=58,R=16,Tp=18,B=46,xmin=2.7,xmax=5.4,ymax=Math.max(0.06,stat(Math.pow(10,xmin),o.rv,o.plx)*1.1);
 const X=x=>L+(x-xmin)/(xmax-xmin)*(W-L-R),Y=y=>H-B-Math.min(y,ymax)/ymax*(H-Tp-B);let s="";
 const x0=X(Math.log10(D.N[0])),x1=X(Math.log10(D.N[1]));
 s+=`<rect x="${L}" y="${Tp}" width="${Math.max(0,x0-L)}" height="${H-B-Tp}" fill="var(--ink)" opacity=".05"/><rect x="${x1}" y="${Tp}" width="${W-R-x1}" height="${H-B-Tp}" fill="var(--ink)" opacity=".05"/><text x="${W-R-6}" y="${Tp+14}" text-anchor="end">extrapolated beyond simulations</text><text x="${(x0+x1)/2}" y="${Tp+14}" text-anchor="middle">simulated range</text>`;
 for(let i=0;i<=4;i++){const y=ymax*i/4;s+=`<line class="gridl" x1="${L}" x2="${W-R}" y1="${Y(y)}" y2="${Y(y)}"/><text x="${L-8}" y="${Y(y)+4}" text-anchor="end">${y.toFixed(3)}</text>`}
 for(let x=3;x<=5;x++)s+=`<text x="${X(x)}" y="${H-B+18}" text-anchor="middle">10<tspan dy="-5" font-size="9">${x}</tspan></text>`;
 s+=`<text x="${(L+W-R)/2}" y="${H-6}" text-anchor="middle">Number of stars</text><text transform="translate(14 ${(Tp+H-B)/2}) rotate(-90)" text-anchor="middle">σ(ρ₀)  [M☉ pc⁻³]</text>`;
 const xs=[];for(let x=xmin;x<=xmax+1e-9;x+=0.02)xs.push(x);
 const P=f=>xs.map((x,i)=>(i?"L":"M")+X(x).toFixed(1)+" "+Y(f(Math.pow(10,x))).toFixed(1)).join("");
 const bandTop=xs.map((x,i)=>(i?"L":"M")+X(x).toFixed(1)+" "+Y(budget({...o,N:Math.pow(10,x)}).hi).toFixed(1)).join("");
 const bandBot=xs.slice().reverse().map(x=>"L"+X(x).toFixed(1)+" "+Y(budget({...o,N:Math.pow(10,x)}).lo).toFixed(1)).join("");
 s+=`<path d="${bandTop}${bandBot}Z" fill="var(--ink)" opacity=".12"/>`;
 s+=`<path d="${P(n=>stat(n,o.rv,o.plx))}" fill="none" stroke="var(--stat)" stroke-width="2"/><path d="${P(()=>b.y)}" fill="none" stroke="var(--sys)" stroke-width="2" stroke-dasharray="6 4"/>`;
 if(b.q>0)s+=`<path d="${P(()=>b.q)}" fill="none" stroke="var(--plx)" stroke-width="2" stroke-dasharray="2 4"/>`;
 s+=`<path d="${P(n=>budget({...o,N:n}).t)}" fill="none" stroke="var(--tot)" stroke-width="2.6"/>`;
 s+=`<line x1="${L}" x2="${W-R}" y1="${Y(o.tg)}" y2="${Y(o.tg)}" stroke="var(--ok)" stroke-dasharray="1 4" stroke-width="1.6"/><text x="${W-R-4}" y="${Y(o.tg)-5}" text-anchor="end" style="fill:var(--ok)">target</text>`;
 s+=`<circle cx="${X(Math.log10(o.N))}" cy="${Y(b.t)}" r="5.5" fill="var(--accent2)"/>`;
 let ly=Tp+34;const leg=[["var(--stat)","","statistical"],["var(--sys)","6 4","completeness systematic"],...(b.q>0?[["var(--plx)","2 4","parallax offset"]]:[]),["var(--tot)","","total (shaded: ±1σ forecast scatter)"]];
 s+=leg.map((l,i)=>`<g transform="translate(${L+10} ${ly+i*16})"><line x2="22" stroke="${l[0]}" stroke-width="2" stroke-dasharray="${l[1]}"/><text x="28" y="4">${l[2]}</text></g>`).join("");
 $("chart").innerHTML=s}
function sens(o,b){const sc=[["2× the stars",{...o,N:o.N*2}],["Every star with a radial velocity",{...o,rv:1}],["Parallax error halved",{...o,plx:o.plx/2}],["Completeness uncertainty halved",{...o,dv:o.dv/2}],["Completeness uncertainty 0.1 mag",{...o,dv:0.1}]];
 const base=b.t;const items=sc.map(([n,q])=>[n,(budget(q).t-base)/base]);const m=Math.max(0.05,...items.map(i=>Math.abs(i[1])));
 $("sens").innerHTML=items.map(([n,d])=>`<div class="srow"><span>${n}</span><div class="sbar"><i style="width:${Math.abs(d)/m*100}%;background:${d<=0?"var(--ok)":"var(--sys)"}"></i></div><b>${d>0?"+":""}${Math.round(d*100)}%</b></div>`).join("")}
function table(){const h="<tr><th>#</th><th>Stars</th><th>RV</th><th>σϖ</th><th>σΔV</th><th>Stat</th><th>Sys</th><th>Parallax</th><th>Total</th></tr>";
 $("tbl").innerHTML=h+rows.map((r,i)=>`<tr><td>${i+1}</td><td>${fmt(r.N)}</td><td>${Math.round(r.rv*100)}%</td><td>${r.plx.toFixed(2)}</td><td>${r.dv.toFixed(2)}</td><td>${f3(r.s)}</td><td>${f3(r.y)}</td><td>${f3(r.q)}</td><td><b>${f3(r.t)}</b></td></tr>`).join("");
 $("scn").hidden=rows.length===0}
function csv(){const l=["scenario,stars,rv_fraction,parallax_error_mas,completeness_sigma_mag,stat,sys,parallax_offset,total"];rows.forEach((r,i)=>l.push([i+1,Math.round(r.N),r.rv.toFixed(3),r.plx.toFixed(2),r.dv.toFixed(2),f3(r.s),f3(r.y),f3(r.q),f3(r.t)].join(",")));return l.join("\n")}
function draw(){
 const o=get(),b=budget(o);
 $("nO").textContent=fmt(o.N);$("rvO").textContent=Math.round(o.rv*100)+"%";$("plxO").textContent=o.plx.toFixed(2)+" mas";$("dvO").textContent="±"+o.dv.toFixed(2)+" mag";$("tgtO").textContent=o.tg.toFixed(3);
 $("kS").textContent=f3(b.s);$("kY").textContent=f3(b.y);$("kQ").textContent=f3(b.q);$("kT").textContent=f3(b.t);
 $("kTs").textContent="forecast scatter "+f3(b.lo)+" to "+f3(b.hi)+" · "+Math.round(b.t/T*100)+"% of ρ₀";
 $("eb").innerHTML=`Forecast: ρ<sub>0</sub> = ${T.toFixed(3)} ± ${f3(b.s)} (stat) ± ${f3(b.y)} (completeness)${b.q>0?` ± ${f3(b.q)} (parallax)`:""} &nbsp;→&nbsp; total ± ${f3(b.t)} M<sub>☉</sub> pc<sup>−3</sup>`;
 const ns=nstar(o),nt=solveN(o,o.tg);
 let v=`Statistical error equals the systematic floor at <b>N* ≈ ${fmt(ns)}</b> stars. `+(o.N<ns?"This survey is statistics-limited, so more stars still help.":"This survey is systematics-limited, so tighten the completeness limit or the parallaxes before adding stars.");
 v+=nt===null?` A target of ${f3(o.tg)} is below the systematic floor of ${f3(Math.hypot(b.y,b.q))} and cannot be reached by adding stars.`:` Reaching ${f3(o.tg)} needs about <b>${fmt(nt)}</b> stars.`;
 $("verdict").innerHTML=v;chart(o,b);sens(o,b)}
["n","rv","plx","dv","tgt","corr"].forEach(i=>$(i).addEventListener("input",draw));
$("paper").onclick=()=>set(PAPER);
$("pDouble").onclick=()=>set({...get(),N:get().N*2});
$("pRV").onclick=()=>set({...get(),rv:1});
$("pTight").onclick=()=>set({...get(),dv:0.1});
$("add").onclick=()=>{const o=get(),b=budget(o);rows.push({...o,...b});table()};
$("clr").onclick=()=>{rows.length=0;table()};
$("dl").onclick=()=>{try{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv()],{type:"text/csv"}));a.download="ahead-of-the-curve-scenarios.csv";a.click()}catch(e){}};
$("cp").onclick=()=>{const t=csv();try{navigator.clipboard.writeText(t).then(()=>{$("cp").textContent="Copied"},()=>{})}catch(e){}};
set(PAPER);
})();
