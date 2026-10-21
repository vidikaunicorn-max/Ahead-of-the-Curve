import json,os
EMAIL="vidika.unicorn@gmail.com"
def page(fname,title,active,body,script=""):
    nav="".join(f'<a href="{h}" class="{"on" if h==active else ""}">{t}</a>' for h,t in [("index.html","Forecaster"),("method.html","Method"),("about.html","About"),("contact.html","Contact")])
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Ahead of the Curve</title>
<meta name="description" content="Ahead of the Curve: a precision forecaster for measuring the local dark and baryonic mass density, based on a Hipparcos K-giant Jeans–Poisson analysis.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="index.html">Ahead of the <span>Curve</span></a><nav>{nav}</nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><div><strong>Ahead of the Curve</strong><br>A precision forecaster for the local mass density ρ<sub>0</sub>.<br>Based on the research paper by Vidika Mirpuri.</div>
<div>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a><br>© 2026 Vidika Mirpuri. Forecasts are model-based estimates, not measurements.</div></div></footer>{script}</body></html>'''
    open(fname,"w").write(html)

BASED='''<div class="based"><strong>Based on a research paper.</strong> This tool implements the error budget of <em>“Local mass density from Hipparcos K giants: a vertical Jeans–Poisson analysis with a mixture of isothermal components”</em> by Vidika Mirpuri, in which ρ<sub>0</sub> = 0.063 ± 0.016 (stat) ± 0.017 (completeness sys.) M<sub>☉</sub> pc<sup>−3</sup> was obtained from 3,585 stars. Forecasts are calibrated on mock catalogues generated and fitted with that paper’s pipeline.</div>'''

index=f'''
<section class="hero"><div class="eyebrow">Survey-planning tool</div>
<h1>How many stars do you need to weigh the Galactic disc?</h1>
<p class="lede">Enter the size and quality of a stellar survey. The forecaster predicts the uncertainty on the local mass density ρ<sub>0</sub> and shows the point beyond which observing more stars stops helping.</p></section>
<div class="grid">
<div class="card"><h3>Survey design</h3>
<div class="field"><label for="n"><span>Stars in sample</span><output id="nO"></output></label><input id="n" type="range" min="2.7" max="5.2" step="any"><small>Tracer stars with 6D or 5D data inside the selection volume.</small></div>
<div class="field"><label for="rv"><span>Fraction with radial velocity</span><output id="rvO"></output></label><input id="rv" type="range" min="0.2" max="1" step="0.01"><small>Missing velocities are marginalised, not discarded.</small></div>
<div class="field"><label for="plx"><span>Parallax error</span><output id="plxO"></output></label><input id="plx" type="range" min="0.1" max="2.5" step="0.05"><small>Median σ<sub>ϖ</sub> in mas. Tested up to 1.5 mas.</small></div>
<div class="field"><label for="dv"><span>Completeness-limit uncertainty</span><output id="dvO"></output></label><input id="dv" type="range" min="0" max="0.6" step="0.01"><small>1σ error on the survey’s limiting magnitude (mag).</small></div>
<div class="field"><label for="tgt"><span>Target precision on ρ<sub>0</sub></span><output id="tgtO"></output></label><input id="tgt" type="range" min="0.005" max="0.03" step="0.001"><small>Total 1σ, in M<sub>☉</sub> pc<sup>−3</sup>.</small></div>
<button class="btn" id="paper">Set to the paper’s survey</button></div>
<div><div class="kpis">
<div class="kpi stat"><div class="l">Statistical</div><div class="v" id="kS"></div><div class="s">M<sub>☉</sub> pc<sup>−3</sup></div></div>
<div class="kpi sys"><div class="l">Completeness sys.</div><div class="v" id="kY"></div><div class="s">M<sub>☉</sub> pc<sup>−3</sup></div></div>
<div class="kpi"><div class="l">Total</div><div class="v" id="kT"></div><div class="s" id="kTs"></div></div></div>
<div class="card"><h3>Error budget vs. sample size</h3><svg id="chart" viewBox="0 0 640 340" width="100%" role="img" aria-label="Forecast error on rho0 versus number of stars"></svg>
<div class="verdict" id="verdict"></div><div id="warn"></div></div></div></div>
{BASED}
<h2>Why this is useful</h2><div class="two prose">
<p>Statistical error shrinks as more stars are added, but the systematic error from not knowing exactly where the survey stops being complete does not. The two curves cross at a sample size N*. Beyond N* the limiting factor is calibration, not volume, so a larger observing allocation buys almost nothing.</p>
<p>Use the tool to size a spectroscopic follow-up, to decide whether to spend time on radial velocities or on photometric calibration, or to teach how error budgets behave in astronomy. See the <a href="method.html">method page</a> for the model, calibration and limits of validity.</p></div>'''
page("index.html","Precision Forecaster","index.html",index,'<script src="assets/forecast.js"></script>')

about=f'''
<section class="hero"><div class="eyebrow">About</div><h1>Making uncertainty visible before the telescope time is spent.</h1></section>
<div class="prose"><h2 style="margin-top:0">Purpose of this site</h2>
<p>Measuring the local mass density ρ<sub>0</sub> is a central problem in Galactic dynamics. It sets how much unseen matter sits in the disc, and the answer depends as much on survey design and calibration as on the number of stars observed. <strong>Ahead of the Curve</strong> turns the error budget of one specific published analysis into an interactive forecaster, so students and researchers can see how sample size, radial-velocity coverage, parallax quality and completeness-limit uncertainty combine into a final error bar.</p>
<p>It is intended for planning and teaching. It is a calibrated model of one specific analysis, not a replacement for running the full pipeline.</p></div>
{BASED}
<h2>Founder</h2><div class="founder"><div class="mono" aria-hidden="true">VM</div><div class="prose">
<h3 style="margin-top:0">Vidika Mirpuri</h3>
<p class="sans" style="color:var(--mute);margin-top:-4px">Founder · Grade 12, IB Diploma Programme · The Cathedral and John Connon School</p>
<p>Vidika is an IB student with a focus on astrophysics and data analysis. Her research paper applies a vertical Jeans–Poisson analysis with a mixture of isothermal components to Hipparcos K giants, quantifying the local mass density together with its statistical and completeness-driven systematic uncertainty. This website grew out of a question that analysis raised: how much would a bigger or better survey actually improve the answer?</p>
<span class="tag">Galactic dynamics</span><span class="tag">Bayesian inference</span><span class="tag">Python · emcee</span><span class="tag">Science outreach</span></div></div>
<h2>Mission</h2>
<blockquote>To make the limits of measurement as easy to see as the measurements themselves, so that the next generation of observers plans smarter, spends less, and asks better questions.</blockquote>
<div class="prose"><p>Ahead of the Curve exists to give early-career scientists a transparent, free tool for reasoning about uncertainty, and to show that real research tools can be built by students.</p></div>
<h2>Get in touch</h2><p>Questions, corrections, collaboration: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''
page("about.html","About","about.html",about)

contact=f'''
<section class="hero"><div class="eyebrow">Contact</div><h1>Get in touch</h1><p class="lede">Feedback on the model, requests for new tracer populations, or collaboration ideas are all welcome.</p></section>
<div class="card prose"><h3>Vidika Mirpuri</h3><p>Founder, Ahead of the Curve<br>Grade 12 IB student, The Cathedral and John Connon School</p>
<p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><strong>Source code:</strong> <a href="https://github.com/vidikaunicorn-max/ahead-of-the-curve">github.com/vidikaunicorn-max/ahead-of-the-curve</a></p></div>
{BASED}
<h2>Citing</h2><div class="card prose"><p>Mirpuri, V. (2026). <em>Local mass density from Hipparcos K giants: a vertical Jeans–Poisson analysis with a mixture of isothermal components.</em> Ahead of the Curve forecaster: github.com/vidikaunicorn-max/ahead-of-the-curve.</p></div>'''
page("contact.html","Contact","contact.html",contact)

import json,os
cal=json.load(open("forecast/calibration.json")) if os.path.exists("forecast/calibration.json") else None
if cal:
    open("assets/calibration.js","w").write("window.CAL="+json.dumps(cal)+";")
    for f in ["index.html"]:
        s=open(f).read().replace('<script src="assets/forecast.js">','<script src="assets/calibration.js"></script><script src="assets/forecast.js">'); open(f,"w").write(s)
    V=cal["validation"]
    method=f'''
<section class="hero"><div class="eyebrow">Method</div><h1>How the forecast works</h1><p class="lede">A compact, calibrated model of the error budget in the underlying paper. Every number on the forecaster page comes from the relations below.</p></section>
<div class="prose">
<h2 style="margin-top:0">1. The analysis being forecast</h2>
<p>The paper fits the vertical distribution and kinematics of Hipparcos K giants with the Jeans–Poisson equations. Total density follows ρ(z) = ρ<sub>0</sub> sech²(z/z<sub>ρ</sub>), with stellar velocities described by a mixture of two isothermal components. Selection effects are handled with a Poisson point-process likelihood using the Hipparcos completeness law V ≤ 7.3 + 1.1 sin|b|, and missing radial velocities are marginalised exactly. Posteriors are sampled with an ensemble MCMC (emcee).</p>
<h2>2. Statistical error</h2>
<p>Mock catalogues were drawn from the best-fitting model, with the paper’s selection function, and refitted with the full pipeline on a grid of sample sizes and radial-velocity fractions. The resulting posterior widths were fitted with</p>
<div class="eq">σ<sub>stat</sub>(N, f<sub>RV</sub>) = σ<sub>0</sub> (N / {cal["N0"]})<sup>−α</sup> (f<sub>RV</sub> / {cal["rv0"]})<sup>−β</sup></div>
<p>with σ<sub>0</sub> = {cal["s0"]:.4f}, α = {cal["alpha"]:.2f}, β = {cal["beta"]:.2f}. The scaling of α with N is not forced to ½, because the dominant degeneracy (ρ<sub>0</sub> against the scale height) is not purely Poisson.</p>
<h2>3. Completeness systematic</h2>
<p>The paper shifted the limiting magnitude by ΔV and refitted. ρ<sub>0</sub> responds roughly linearly, with slope ≈ −{abs(cal["slope"]):.3f} M<sub>☉</sub> pc<sup>−3</sup> per magnitude, which is nearly independent of N. The systematic error is therefore</p>
<div class="eq">σ<sub>sys</sub> = |dρ<sub>0</sub>/dΔV| · σ<sub>ΔV</sub></div>
<p>and the total is σ<sub>tot</sub> = √(σ<sub>stat</sub>² + σ<sub>sys</sub>²). Increasing N lowers only the first term, which is why a crossover sample size N* exists.</p>
<h2>4. Validation</h2>
<table><tr><th>Quantity</th><th>Paper</th><th>Forecaster</th></tr>
<tr><td>Statistical, N = 3,585, 59% RV</td><td>0.016</td><td>{V["stat"]:.3f}</td></tr>
<tr><td>Completeness sys., σ<sub>ΔV</sub> = 0.3 mag</td><td>0.017</td><td>{V["sys"]:.3f}</td></tr></table>
<p>{cal["validation_note"]}</p>
<h2>5. Limits of validity</h2>
<ul><li>Only the paper’s setup is modelled: K giants, vertical Jeans equilibrium, a two-component mixture, Hipparcos-like completeness.</li>
<li>Equilibrium is assumed, not tested. Departures from it (e.g. the vertical phase-space spiral) are not in the error budget.</li>
<li>Parallax errors: mock tests showed no bias at 0.8 mas and about +20% in ρ<sub>0</sub> at 1.5 mas; larger values were not tested. The forecaster warns rather than extrapolating.</li>
<li>Forecasts are fitted scaling relations with their own scatter ({cal["scatter_note"]}), not new measurements. The tool is novel as a planning aid, not as a new dynamical method.</li></ul>
<p>Questions or corrections: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
{BASED}'''
    page("method.html","Method","method.html",method)
