import json,numpy as np
rows=[json.loads(l) for l in open('/home/claude/paper2/fc_grid2.jsonl')]
T=0.063
N=np.array([r['N'] for r in rows],float); rv=np.array([r['rv'] for r in rows]); sp=np.array([r['sig_plx'] for r in rows]); dv=np.array([r['dv'] for r in rows])
med=np.array([r['med'] for r in rows]); sg=np.array([r['sig'] for r in rows])
# --- statistical error surface (log-linear, quadratic in parallax error)
X=np.c_[np.ones(len(N)),np.log(N/3585),np.log(rv/0.6),sp,sp**2,dv**2]
c,res,rk,_=np.linalg.lstsq(X,np.log(sg),rcond=None)
resid=np.log(sg)-X@c; dof=len(N)-X.shape[1]; s_res=float(np.sqrt(np.sum(resid**2)/dof))
# --- bias surface (relative shift of rho0), weighted by inverse variance
y=(med-T)/T; w=(T/sg)
B=np.c_[np.ones(len(N)),dv,dv**2,sp,sp**2,sp*dv]
cb=np.linalg.lstsq(B*w[:,None],y*w,rcond=None)[0]
rb=(y-B@cb)*w; s_b=float(np.sqrt(np.sum(rb**2)/(len(N)-B.shape[1])))
# --- anchors to the paper's own configuration (N=3585, rv=0.59, plx=0.8 mas, dv=0)
x0=np.array([1,0,np.log(0.59/0.6),0.8,0.64,0.0]); emu0=float(np.exp(x0@c))
slope_emu=float(cb[1]*T)               # d rho0 / d dv at plx=0.8, dv=0 (per mag)
slope_emu=(cb[1]+cb[5]*0.8)*T
cal=dict(N0=3585,rv0=0.59,rho0=T,
 stat=dict(coef=c.tolist(),anchor=0.016/emu0,resid=s_res),
 bias=dict(coef=cb.tolist(),anchor=(0.017/0.3)/abs(slope_emu),resid=s_b),
 plx0=0.8,
 domain=dict(N=[800,12000],rv=[0.3,1.0],plx=[0.0,2.5],dv=[-0.5,0.5]),
 nfits=len(N),
 paper=dict(stat=0.016,sys=0.017),
 emu_free=dict(stat_at_paper=emu0,sys_slope=slope_emu))
json.dump(cal,open('/home/claude/ahead-of-the-curve/forecast/calibration2.json','w'),indent=1)
print('n',len(N),'resid',s_res,'bias resid',s_b); print('stat coef',np.round(c,3)); print('bias coef',np.round(cb,3))
print('free emulator at paper config: stat',emu0,'sys slope',slope_emu,'-> sys(0.3)',abs(slope_emu)*0.3)
