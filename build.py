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
<h1>Forecast the precision of a local mass density measurement.</h1>
<p class="lede">Enter the size and quality of a stellar survey. The forecaster predicts the statistical, completeness and parallax error budget on ρ<sub>0</sub> for the vertical Jeans–Poisson analysis in the paper, and shows where adding stars stops paying off.</p></section>
<div class="grid">
<div class="card"><h3>Survey design</h3>
<div class="field"><label for="n"><span>Stars in sample</span><output id="nO"></output></label><input id="n" type="range" min="2.7" max="5.4" step="any"><small>Tracer stars with astrometry inside the selection volume.</small></div>
<div class="field"><label for="rv"><span>Fraction with radial velocity</span><output id="rvO"></output></label><input id="rv" type="range" min="0.2" max="1" step="0.01"><small>Missing velocities are marginalised, not discarded.</small></div>
<div class="field"><label for="plx"><span>Parallax error</span><output id="plxO"></output></label><input id="plx" type="range" min="0.1" max="2.5" step="0.05"><small>Median σ<sub>ϖ</sub> in mas.</small></div>
<div class="field"><label for="dv"><span>Completeness-limit uncertainty</span><output id="dvO"></output></label><input id="dv" type="range" min="0" max="0.6" step="0.01"><small>1σ error on the survey’s limiting magnitude (mag).</small></div>
<div class="field"><label for="tgt"><span>Target precision on ρ<sub>0</sub></span><output id="tgtO"></output></label><input id="tgt" type="range" min="0.005" max="0.03" step="0.001"><small>Total 1σ, in M<sub>☉</sub> pc<sup>−3</sup>.</small></div>
<label class="chk"><input type="checkbox" id="corr"> Correct for the expected parallax offset</label>
<div class="btns"><button class="btn" id="paper">Paper’s survey</button><button class="btn ghost" id="pDouble">2× stars</button><button class="btn ghost" id="pRV">All RVs</button><button class="btn ghost" id="pTight">±0.1 mag</button></div></div>
<div><div class="verdict" id="eb" style="margin:0 0 14px;font-weight:600"></div><div class="kpis">
<div class="kpi stat"><div class="l">Statistical</div><div class="v" id="kS"></div><div class="s">M<sub>☉</sub> pc<sup>−3</sup></div></div>
<div class="kpi sys"><div class="l">Completeness</div><div class="v" id="kY"></div><div class="s">M<sub>☉</sub> pc<sup>−3</sup></div></div>
<div class="kpi plx"><div class="l">Parallax offset</div><div class="v" id="kQ"></div><div class="s">M<sub>☉</sub> pc<sup>−3</sup></div></div>
<div class="kpi"><div class="l">Total</div><div class="v" id="kT"></div><div class="s" id="kTs"></div></div></div>
<div class="card"><h3>Error budget vs. sample size</h3><svg id="chart" viewBox="0 0 680 350" width="100%" role="img" aria-label="Forecast error on rho0 versus number of stars"></svg>
<div class="verdict" id="verdict"></div></div></div></div>
<div class="two"><div class="card"><h3>What would help most</h3><p class="small">Change in total error for each improvement, from your current design.</p><div id="sens"></div></div>
<div class="card"><h3>Compare scenarios</h3><p class="small">Add designs to a table, then copy or download it.</p><div class="btns"><button class="btn" id="add">Add current design</button><button class="btn ghost" id="clr">Clear</button><button class="btn ghost" id="dl">Download CSV</button><button class="btn ghost" id="cp">Copy CSV</button></div><div id="scn" hidden style="overflow-x:auto"><table id="tbl"></table></div></div></div>
{BASED}
<h2>Why this is useful</h2><div class="two prose">
<p>Statistical error shrinks as more stars are added, but the completeness systematic and the parallax offset do not. The two sides cross at a sample size N*. Beyond N* the limiting factor is calibration, not volume, so a larger observing allocation buys little.</p>
<p>Use the tool to size a follow-up, to decide between radial velocities and photometric calibration, or to teach how error budgets behave. The <a href="method.html">method page</a> describes the simulations, the fitted model and its range.</p></div>'''
page("index.html","Precision Forecaster","index.html",index,'<script src="assets/calibration2.js"></script><script src="assets/forecast2.js"></script>')

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
<p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
{BASED}
<h2>Citing</h2><div class="card prose"><p>Mirpuri, V. (2026). <em>Local mass density from Hipparcos K giants: a vertical Jeans–Poisson analysis with a mixture of isothermal components.</em></p></div>'''
page("contact.html","Contact","contact.html",contact)

cal=json.load(open("forecast/calibration2.json"))
open("assets/calibration2.js","w").write("window.CAL2="+json.dumps(cal)+";")
sc=cal["stat"]["coef"]
method=f"""
<section class="hero"><div class="eyebrow">Method</div><h1>How the forecast is built</h1><p class="lede">A forecaster fitted to {cal["nfits"]} full MCMC analyses of simulated catalogues, scaled to the paper’s published errors at its own configuration.</p></section>
<div class="prose">
<h2 style="margin-top:0">1. The analysis being forecast</h2>
<p>The paper fits the vertical distribution and kinematics of Hipparcos K giants with the Jeans–Poisson equations. Total density follows ρ(z) = ρ<sub>0</sub> sech²(z/z<sub>ρ</sub>), with stellar velocities described by a mixture of two isothermal components. Selection effects are handled with a Poisson point-process likelihood using the Hipparcos completeness law V ≤ 7.3 + 1.1 sin|b|, and missing radial velocities are marginalised exactly. Posteriors are sampled with an ensemble MCMC (emcee).</p>
<h2>2. Simulated catalogues</h2>
<p>Catalogues were drawn from the best-fitting model with the paper’s selection function, including Gaussian parallax errors applied before the distance selection, a shifted assumed completeness limit, and a variable fraction of stars with radial velocities. Each was analysed with the full pipeline. The {cal["nfits"]} runs follow a space-filling (Sobol) design over four inputs, plus {8} repeats at the paper’s configuration:</p>
<table><tr><th>Input</th><th>Simulated range</th></tr>
<tr><td>Stars in sample</td><td>{cal["domain"]["N"][0]:,} to {cal["domain"]["N"][1]:,}</td></tr>
<tr><td>Fraction with radial velocity</td><td>{int(cal["domain"]["rv"][0]*100)}% to {int(cal["domain"]["rv"][1]*100)}% requested</td></tr>
<tr><td>Parallax error σ<sub>ϖ</sub></td><td>{cal["domain"]["plx"][0]} to {cal["domain"]["plx"][1]} mas</td></tr>
<tr><td>Assumed limiting-magnitude shift ΔV</td><td>{cal["domain"]["dv"][0]} to +{cal["domain"]["dv"][1]} mag</td></tr></table>
<h2>3. Statistical error</h2>
<p>The posterior width σ(ρ<sub>0</sub>) was fitted with a log-linear model in the number of stars N, the radial-velocity fraction f<sub>RV</sub> and the parallax error σ<sub>ϖ</sub>:</p>
<div class="eq">ln σ<sub>stat</sub> = {sc[0]:.2f} {sc[1]:+.2f} ln(N/3585) {sc[2]:+.2f} ln(f<sub>RV</sub>/0.6) {sc[3]:+.2f} σ<sub>ϖ</sub> {sc[4]:+.2f} σ<sub>ϖ</sub>² {sc[5]:+.2f} ΔV²</div>
<p>The N exponent is close to the Poisson ½. The fitted surface reproduces the simulated widths with {cal["stat"]["resid"]*100:.0f}% rms scatter, shown as the shaded band on the forecaster.</p>
<h2>4. Completeness systematic</h2>
<p>An error σ<sub>ΔV</sub> on the limiting magnitude moves ρ<sub>0</sub> by (dρ<sub>0</sub>/dΔV) σ<sub>ΔV</sub>. The slope is measured from the simulations as a function of parallax error and is nearly independent of N, so the systematic sets a floor that more stars cannot lower.</p>
<h2>5. Parallax offset</h2>
<p>Parallax errors scatter stars across the distance limit, and distances computed from noisy parallaxes shift the recovered ρ<sub>0</sub>. The forecaster reports this offset relative to the paper’s 0.8 mas and, unless corrected, adds it in quadrature to the total.</p>
<h2>6. Total error</h2>
<div class="eq">σ<sub>tot</sub> = √(σ<sub>stat</sub>² + σ<sub>sys</sub>² + σ<sub>plx</sub>²)</div>
<p>N* is the sample size at which σ<sub>stat</sub> equals the combined floor. Sample sizes for a target precision come from solving σ<sub>tot</sub> = target.</p>
<h2>7. Scaling to the paper</h2>
<p>The statistical and completeness terms are scaled so that the forecaster returns the paper’s published ±{cal["paper"]["stat"]:.3f} (statistical) and ±{cal["paper"]["sys"]:.3f} (completeness, σ<sub>ΔV</sub> = 0.3 mag) at the paper’s configuration: 3,585 stars, 59% with radial velocities, σ<sub>ϖ</sub> = 0.8 mas. Away from that point the dependence on each input comes from the simulations.</p>
<h2>8. Scope</h2>
<ul><li>The forecast applies to this analysis: K giants, vertical Jeans equilibrium, a two-component mixture, Hipparcos-like completeness. It is not a forecast for other tracers, other methods or other surveys.</li>
<li>Simulated catalogues follow the fitted model, so departures from equilibrium and from the mixture assumption are not in the budget.</li>
<li>Regions of the chart outside the simulated range are extrapolations and are shaded.</li>
<li>The simulated central value of ρ<sub>0</sub> scatters about the input by roughly one posterior width, so a forecast describes the size of the error bar, not where one particular measurement will land.</li></ul>
<p>Questions or corrections: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
{BASED}"""
page("method.html","Method","method.html",method)
