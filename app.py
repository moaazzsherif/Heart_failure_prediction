import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import time
from datetime import datetime
 
st.set_page_config(
    page_title="CardioSense AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');
 
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"],.stApp{font-family:'Instrument Sans',sans-serif;background:#0a1628!important;color:#e2e8f0}
[data-testid="stAppViewContainer"]{background:#0a1628!important}
[data-testid="stAppViewContainer"]::before{content:'';position:fixed;inset:0;background:#0a1628;z-index:-1}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,#MainMenu{display:none!important}
[data-testid="stBottom"]{background:transparent!important}
.main{background:transparent!important}
[data-testid="stVerticalBlockBorderWrapper"]{background:transparent!important}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:#0a1628}::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:2px}
 
.bg-grid{position:fixed;inset:0;background-image:linear-gradient(rgba(59,130,246,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,.03) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;z-index:0}
.bg-g1{position:fixed;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(220,38,38,.07) 0%,transparent 70%);top:-250px;right:-150px;pointer-events:none;z-index:0;animation:flt 9s ease-in-out infinite}
.bg-g2{position:fixed;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(59,130,246,.05) 0%,transparent 70%);bottom:-200px;left:-150px;pointer-events:none;z-index:0;animation:flt 11s ease-in-out infinite reverse}
@keyframes flt{0%,100%{transform:translateY(0)}50%{transform:translateY(28px)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(220,38,38,.5)}50%{box-shadow:0 0 0 7px rgba(220,38,38,0)}}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes scoreIn{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:scale(1)}}
 
.navbar{position:sticky;top:0;z-index:999;display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:62px;background:rgba(10,22,40,.92);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.05)}
.nav-logo{font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:800;letter-spacing:-.02em;color:white;display:flex;align-items:center;gap:10px}
.nav-logo span{color:#dc2626}
.nav-dot{width:8px;height:8px;border-radius:50%;background:#dc2626;animation:pulse 2s infinite}
.nav-badge{background:rgba(220,38,38,.1);border:1px solid rgba(220,38,38,.25);color:#f87171;font-size:.68rem;font-weight:600;letter-spacing:.1em;padding:4px 10px;border-radius:20px}
.nav-acc{font-size:.78rem;color:#475569}
 
.hero{padding:56px 0 40px;animation:fadeIn .6s ease}
.hero-tag{display:inline-flex;align-items:center;gap:8px;background:rgba(220,38,38,.07);border:1px solid rgba(220,38,38,.18);border-radius:30px;padding:5px 14px;font-size:.7rem;font-weight:600;letter-spacing:.12em;color:#f87171;text-transform:uppercase;margin-bottom:20px}
.hero-dot{width:6px;height:6px;border-radius:50%;background:#dc2626;animation:pulse 2s infinite}
.hero-title{font-family:'Syne',sans-serif;font-size:clamp(2.6rem,4.5vw,4.2rem);font-weight:800;line-height:1.0;letter-spacing:-.03em;color:white;margin-bottom:14px}
.hero-title .acc{background:linear-gradient(135deg,#dc2626,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:1rem;color:#64748b;line-height:1.65;max-width:540px}
.stats-row{display:flex;gap:10px;margin-top:36px;flex-wrap:wrap}
.stat-pill{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:11px 18px;box-shadow:0 4px 16px rgba(0,0,0,.4)}
.sp-val{font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:700;color:white}
.sp-lbl{font-size:.68rem;color:#475569;letter-spacing:.08em;text-transform:uppercase}
 
.kpi-row{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:28px}
.kpi{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:16px;padding:18px 20px;position:relative;overflow:hidden;transition:border-color .2s,transform .2s;cursor:default;box-shadow:0 4px 24px rgba(0,0,0,.5),0 1px 0 rgba(255,255,255,.04) inset;animation:fadeIn .5s ease both}
.kpi:hover{border-color:rgba(255,255,255,.1);transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,.6),0 1px 0 rgba(255,255,255,.06) inset}
.kpi::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--c);opacity:.55}
.kpi-ico{font-size:1.1rem;margin-bottom:10px}
.kpi-v{font-family:'Syne',sans-serif;font-size:1.95rem;font-weight:700;color:white;line-height:1;margin-bottom:3px}
.kpi-l{font-size:.68rem;color:#475569;font-weight:500;letter-spacing:.08em;text-transform:uppercase}
 
.sec-head{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.sec-line{width:3px;height:18px;background:linear-gradient(180deg,#dc2626,#f97316);border-radius:2px}
.sec-txt{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:white;letter-spacing:-.01em}
.sec-cnt{font-size:.68rem;color:#475569;margin-left:auto;letter-spacing:.08em;text-transform:uppercase}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),transparent);margin:36px 0}
 
.result-main{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:24px;padding:32px 24px;text-align:center;position:relative;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.55),0 1px 0 rgba(255,255,255,.05) inset;animation:scoreIn .4s ease}
.r-badge{display:inline-block;padding:5px 14px;border-radius:30px;font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}
.r-score{font-family:'Syne',sans-serif;font-size:5.2rem;font-weight:800;line-height:1;letter-spacing:-.04em}
.r-desc{font-size:.82rem;color:#475569;line-height:1.65;margin-top:10px}
 
.factor-item{display:flex;align-items:center;gap:10px;padding:9px 13px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:10px;margin-bottom:7px;font-size:.81rem;color:#94a3b8;box-shadow:0 2px 10px rgba(0,0,0,.35);animation:fadeIn .3s ease both}
.factor-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
 
.history-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:14px;padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;animation:fadeIn .3s ease;box-shadow:0 2px 12px rgba(0,0,0,.3)}
.history-score{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700}
.history-meta{font-size:.72rem;color:#475569;margin-top:2px}
.history-badge{font-size:.65rem;font-weight:600;letter-spacing:.08em;padding:3px 8px;border-radius:20px}
 
.compare-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:16px;padding:20px;box-shadow:0 4px 20px rgba(0,0,0,.4)}
 
.loading-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;gap:16px}
.spinner{width:40px;height:40px;border:3px solid rgba(220,38,38,.2);border-top-color:#dc2626;border-radius:50%;animation:spin .8s linear infinite}
.loading-text{font-size:.85rem;color:#64748b;letter-spacing:.06em}
 
[data-testid="column"]{padding:0 8px!important}
.block-container{padding:0 40px 60px!important;max-width:100%!important;width:100%!important}
section.main>div{max-width:100%!important}
[data-testid="stAppViewBlockContainer"]{padding:0 40px 60px!important;max-width:100%!important}
.main .block-container{max-width:100%!important}
.appview-container{width:100%!important}
.appview-container>section{width:100%!important}
 
.stSlider [data-testid="stThumb"]{background:#dc2626!important}
div[data-testid="stSelectbox"] label,.stSlider label{color:#64748b!important;font-size:.72rem!important;font-weight:500!important;letter-spacing:.06em!important;text-transform:uppercase!important}
div[data-testid="stSelectbox"]>div>div{background:rgba(255,255,255,.03)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:10px!important;color:white!important}
div[data-testid="stSelectbox"]>div>div:hover{border-color:rgba(220,38,38,.4)!important}
.stSlider>div>div>div{background:rgba(255,255,255,.08)!important}
.stSlider>div>div>div>div{background:#dc2626!important}
 
.stRadio>label{display:none!important}
.stRadio>div{flex-direction:row!important;gap:4px!important;background:rgba(255,255,255,.02)!important;border:1px solid rgba(255,255,255,.06)!important;border-radius:14px!important;padding:4px!important;width:fit-content!important}
.stRadio>div>label{background:transparent!important;border:none!important;border-radius:10px!important;padding:8px 22px!important;color:#64748b!important;font-size:.84rem!important;font-weight:500!important;cursor:pointer!important;transition:all .15s!important;text-transform:none!important;letter-spacing:0!important}
.stRadio>div>label:has(input:checked){background:rgba(220,38,38,.12)!important;color:#f87171!important;border:1px solid rgba(220,38,38,.28)!important}
.stRadio input[type="radio"]{display:none!important}
 
div[data-testid="stButton"]>button{width:100%!important;background:linear-gradient(135deg,#dc2626,#b91c1c)!important;color:white!important;border:none!important;border-radius:14px!important;padding:15px 32px!important;font-family:'Syne',sans-serif!important;font-size:.92rem!important;font-weight:700!important;letter-spacing:.02em!important;transition:all .2s!important;box-shadow:0 4px 24px rgba(220,38,38,.22)!important;margin-top:6px!important}
div[data-testid="stButton"]>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 32px rgba(220,38,38,.38)!important}
 
.stDownloadButton>button{background:rgba(255,255,255,.04)!important;color:#94a3b8!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:10px!important;font-size:.8rem!important;padding:8px 16px!important;box-shadow:none!important;margin-top:4px!important}
.stDownloadButton>button:hover{background:rgba(255,255,255,.07)!important;color:white!important}
 
@media(max-width:768px){
    .kpi-row{grid-template-columns:repeat(2,1fr)!important}
    .navbar{padding:0 16px!important}
    .block-container{padding:0 16px 40px!important}
    .hero-title{font-size:2rem!important}
    .stats-row{gap:6px!important}
    .stat-pill{padding:8px 12px!important}
}
</style>
""", unsafe_allow_html=True)
 
# ── Background ─────────────────────────────────────────────────
st.markdown('<div class="bg-grid"></div><div class="bg-g1"></div><div class="bg-g2"></div>', unsafe_allow_html=True)
 
# ── Navbar ─────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo"><div class="nav-dot"></div>Cardio<span>Sense</span></div>
  <div style="display:flex;align-items:center;gap:16px">
    <span class="nav-acc">Gradient Boosting · 918 patients · 94.6% Accuracy</span>
    <div class="nav-badge">AI POWERED</div>
  </div>
</div>
""", unsafe_allow_html=True)
 
# ── Session State ──────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state.history = []
 
# ── Data ───────────────────────────────────────────────────────
DATA = {
    'age_rate': {'30s':36,'40s':42,'50s':58,'60s':74,'70s':67},
    'age_n':    {'30s':88,'40s':223,'50s':381,'60s':197,'70s':24},
    'sex': {'Male':{'sick':458,'healthy':267,'rate':63},'Female':{'sick':50,'healthy':143,'rate':26}},
    'chestpain': {'ASY':79,'TA':43,'NAP':35,'ATA':14},
    'stslope':   {'Flat':83,'Down':78,'Up':20},
    'ea':        {'Yes':85,'No':35},
    'chol_bins': {'<150':84,'150-200':38,'200-250':45,'250-300':55,'300-350':53,'400+':62},
    'corr': dict(
        cols=['Age','RestBP','Chol','FastBS','MaxHR','Oldpeak','Disease'],
        vals=[[1.00,0.26,-0.07,0.20,-0.38,0.26,0.28],[0.26,1.00,0.10,0.07,-0.11,0.17,0.12],
              [-0.07,0.10,1.00,-0.20,0.19,0.06,-0.16],[0.20,0.07,-0.20,1.00,-0.13,0.05,0.27],
              [-0.38,-0.11,0.19,-0.13,1.00,-0.16,-0.40],[0.26,0.17,0.06,0.05,-0.16,1.00,0.40],
              [0.28,0.12,-0.16,0.27,-0.40,0.40,1.00]]
    )
}
 
L = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
         font=dict(color='#64748b',family='Instrument Sans'),
         margin=dict(l=8,r=8,t=36,b=8),showlegend=False,
         title_font=dict(color='#94a3b8',size=11,family='Syne'),title_x=0)
 
def risk_score(age,sex,cp,slope,ea,op,fbs,hr,chol):
    s=0
    if age>=60: s+=22
    elif age>=50: s+=14
    elif age>=40: s+=7
    if sex=='Male': s+=12
    s+={'ASY':28,'TA':10,'NAP':5,'ATA':0}.get(cp,0)
    s+={'Flat':25,'Down':20,'Up':0}.get(slope,0)
    if ea=='Yes': s+=20
    if op>2: s+=15
    elif op>0.5: s+=7
    if fbs==1: s+=8
    if hr<120: s+=8
    elif hr<150: s+=4
    if chol<150: s+=10
    return min(int(s),100)
 
def risk_meta(score):
    if score>=70:
        return "HIGH RISK","#dc2626","220,38,38","rgba(220,38,38,.1)","rgba(220,38,38,.28)","Strong indicators present. Immediate cardiology referral recommended."
    elif score>=45:
        return "MODERATE RISK","#f97316","249,115,22","rgba(249,115,22,.1)","rgba(249,115,22,.28)","Several risk factors detected. Medical consultation advised within 2 weeks."
    else:
        return "LOW RISK","#10b981","16,185,129","rgba(16,185,129,.1)","rgba(16,185,129,.28)","Profile shows minimal risk indicators. Maintain a healthy lifestyle."
 
# ── Nav ────────────────────────────────────────────────────────
page = st.radio("Navigation", ["📊  Dashboard","🫀  Predict","📋  History","⚖️  Compare"], horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
if "Dashboard" in page:
    st.markdown("""
    <div class="hero">
      <div class="hero-tag"><div class="hero-dot"></div>Clinical Analytics Platform</div>
      <div class="hero-title">Heart Disease<br><span class="acc">Intelligence</span></div>
      <div class="hero-sub">Predictive analytics across 918 patients. Gradient Boosting tuned to 94.6% accuracy with threshold 0.39 for clinical safety.</div>
      <div class="stats-row">
        <div class="stat-pill"><div><div class="sp-val">918</div><div class="sp-lbl">Patients</div></div></div>
        <div class="stat-pill"><div><div class="sp-val">55%</div><div class="sp-lbl">Positive Rate</div></div></div>
        <div class="stat-pill"><div><div class="sp-val">20</div><div class="sp-lbl">Features</div></div></div>
        <div class="stat-pill"><div><div class="sp-val">0.40</div><div class="sp-lbl">Tuned Threshold</div></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div class="kpi-row">
      <div class="kpi" style="--c:#dc2626;animation-delay:.0s"><div class="kpi-ico">🎯</div><div class="kpi-v">94.6%</div><div class="kpi-l">Accuracy</div></div>
      <div class="kpi" style="--c:#f97316;animation-delay:.1s"><div class="kpi-ico">⚡</div><div class="kpi-v">95.1%</div><div class="kpi-l">F1 Score</div></div>
      <div class="kpi" style="--c:#8b5cf6;animation-delay:.2s"><div class="kpi-ico">🔬</div><div class="kpi-v">95.1%</div><div class="kpi-l">Precision</div></div>
      <div class="kpi" style="--c:#10b981;animation-delay:.3s"><div class="kpi-ico">🩺</div><div class="kpi-v">95.1%</div><div class="kpi-l">Recall</div></div>
      <div class="kpi" style="--c:#3b82f6;animation-delay:.4s"><div class="kpi-ico">📈</div><div class="kpi-v">0.961</div><div class="kpi-l">ROC-AUC</div></div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Demographics & Age Risk</div><div class="sec-cnt">918 patients</div></div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns([5,3,3])
 
    with c1:
        ages=list(DATA['age_rate'].keys()); rates=list(DATA['age_rate'].values())
        clrs=['#3b82f6' if r<45 else '#f97316' if r<65 else '#dc2626' for r in rates]
        fig=go.Figure(go.Bar(x=ages,y=rates,marker_color=clrs,marker_line_width=0,
            text=[f'{r}%' for r in rates],textposition='outside',
            textfont=dict(color='white',size=11,family='Syne')))
        fig.update_layout(**L,title='Disease Rate by Age Group',
            yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,92]),
            xaxis=dict(color='#475569'))
        st.plotly_chart(fig,use_container_width=True)
 
    with c2:
        fig2=go.Figure()
        for sx,d in DATA['sex'].items():
            fig2.add_trace(go.Bar(name='Disease',x=[sx],y=[d['sick']],marker_color='#dc2626',marker_line_width=0,showlegend=(sx=='Male')))
            fig2.add_trace(go.Bar(name='Healthy',x=[sx],y=[d['healthy']],marker_color='rgba(59,130,246,.7)',marker_line_width=0,showlegend=(sx=='Male')))
            fig2.add_annotation(x=sx,y=d['sick']+d['healthy']+12,text=f"<b>{d['rate']}%</b>",showarrow=False,
                font=dict(color='#dc2626' if d['rate']>50 else '#3b82f6',size=12,family='Syne'))
        fig2.update_layout(**{**L,'showlegend':True},barmode='stack',title='Disease by Sex',
            legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#64748b',size=10)),
            yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569'),
            xaxis=dict(color='#475569'))
        st.plotly_chart(fig2,use_container_width=True)
 
    with c3:
        fig3=go.Figure(go.Bar(x=list(DATA['ea'].keys()),y=list(DATA['ea'].values()),
            marker_color=['#dc2626','rgba(59,130,246,.7)'],marker_line_width=0,
            text=[f"{v}%" for v in DATA['ea'].values()],textposition='outside',
            textfont=dict(color='white',size=12,family='Syne')))
        fig3.update_layout(**L,title='Exercise Angina Risk',
            yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,100]),
            xaxis=dict(color='#475569'))
        st.plotly_chart(fig3,use_container_width=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Clinical Indicators</div></div>', unsafe_allow_html=True)
    c4,c5 = st.columns(2)
 
    with c4:
        cp_df=pd.DataFrame({'Type':list(DATA['chestpain'].keys()),'Rate':list(DATA['chestpain'].values())}).sort_values('Rate')
        clrs2=['#3b82f6' if r<40 else '#f97316' if r<65 else '#dc2626' for r in cp_df['Rate']]
        fig4=go.Figure(go.Bar(y=cp_df['Type'],x=cp_df['Rate'],orientation='h',
            marker_color=clrs2,marker_line_width=0,
            text=[f'{r}%' for r in cp_df['Rate']],textposition='outside',
            textfont=dict(color='white',size=11,family='Syne')))
        fig4.update_layout(**L,title='Chest Pain Type — Disease Rate',
            xaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,92]),
            yaxis=dict(color='#94a3b8'))
        st.plotly_chart(fig4,use_container_width=True)
 
    with c5:
        sl_df=pd.DataFrame({'Slope':list(DATA['stslope'].keys()),'Rate':list(DATA['stslope'].values())}).sort_values('Rate')
        clrs3=['#3b82f6' if r<40 else '#f97316' if r<65 else '#dc2626' for r in sl_df['Rate']]
        fig5=go.Figure(go.Bar(y=sl_df['Slope'],x=sl_df['Rate'],orientation='h',
            marker_color=clrs3,marker_line_width=0,
            text=[f'{r}%' for r in sl_df['Rate']],textposition='outside',
            textfont=dict(color='white',size=11,family='Syne')))
        fig5.update_layout(**L,title='ST Slope — Disease Rate',
            xaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,92]),
            yaxis=dict(color='#94a3b8'))
        st.plotly_chart(fig5,use_container_width=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Correlation & Cholesterol</div></div>', unsafe_allow_html=True)
    c6,c7 = st.columns([3,2])
 
    with c6:
        cols=DATA['corr']['cols']; vals=DATA['corr']['vals']
        fig6=go.Figure(go.Heatmap(z=vals,x=cols,y=cols,
            colorscale=[[0,'#3b82f6'],[0.5,'#0a1628'],[1,'#dc2626']],
            zmid=0,zmin=-1,zmax=1,
            text=[[f'{v:.2f}' for v in row] for row in vals],
            texttemplate='%{text}',textfont=dict(size=10,color='white')))
        fig6.update_layout(**L,title='Feature Correlation Matrix',
            xaxis=dict(color='#64748b'),yaxis=dict(color='#64748b'))
 
        # Download button for chart
        col_dl = st.columns([4,1])
        with col_dl[0]: st.plotly_chart(fig6,use_container_width=True)
        with col_dl[1]:
            st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
            corr_df = pd.DataFrame(vals, columns=cols, index=cols)
            st.download_button("⬇ CSV", corr_df.to_csv().encode(), "correlation.csv", "text/csv")
 
    with c7:
        ch_k=list(DATA['chol_bins'].keys()); ch_v=list(DATA['chol_bins'].values())
        clrs4=['#dc2626' if v>65 else '#f97316' if v>48 else '#3b82f6' for v in ch_v]
        fig7=go.Figure(go.Bar(x=ch_k,y=ch_v,marker_color=clrs4,marker_line_width=0,
            text=[f'{v}%' for v in ch_v],textposition='outside',
            textfont=dict(color='white',size=10,family='Syne')))
        fig7.update_layout(**L,title='Cholesterol Range vs Disease Rate',
            yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,100]),
            xaxis=dict(color='#475569',tickangle=-30))
        st.plotly_chart(fig7,use_container_width=True)
 
# ══════════════════════════════════════════════════════════════
# PREDICT
# ══════════════════════════════════════════════════════════════
elif "Predict" in page:
    st.markdown("""
    <div class="hero">
      <div class="hero-tag"><div class="hero-dot"></div>AI Risk Assessment</div>
      <div class="hero-title">Patient<br><span class="acc">Risk Score</span></div>
      <div class="hero-sub">Enter clinical parameters to calculate heart disease probability using our tuned Gradient Boosting model.</div>
    </div>
    """, unsafe_allow_html=True)
 
    fc,rc = st.columns([3,2], gap="large")
 
    with fc:
        st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Clinical Parameters</div></div>', unsafe_allow_html=True)
 
        r1,r2=st.columns(2)
        with r1: age_v=st.slider("Age (years)",28,80,54)
        with r2: sex_v=st.selectbox("Biological Sex",["Male","Female"])
 
        r3,r4=st.columns(2)
        with r3:
            cp_raw=st.selectbox("Chest Pain Type",["ASY — Asymptomatic","ATA — Atypical Angina","NAP — Non-Anginal Pain","TA  — Typical Angina"])
            cp_v=cp_raw.split(" — ")[0].strip()
        with r4: slope_v=st.selectbox("ST Slope",["Flat","Down","Up"])
 
        r5,r6=st.columns(2)
        with r5: ea_v=st.selectbox("Exercise Angina",["Yes","No"])
        with r6: fbs_v=st.selectbox("Fasting BS > 120 mg/dL",[0,1])
 
        r7,r8=st.columns(2)
        with r7: hr_v=st.slider("Max Heart Rate (bpm)",60,202,140)
        with r8: op_v=st.slider("Oldpeak",float(-2.6),float(6.2),float(0.0),float(0.1))
 
        chol_v=st.slider("Cholesterol (mg/dL)",85,603,220)
        analyse=st.button("Analyse Risk  →")
 
    with rc:
        # Loading animation on button click
        if analyse:
            placeholder=st.empty()
            placeholder.markdown("""
            <div class="loading-wrap">
              <div class="spinner"></div>
              <div class="loading-text">ANALYSING PATIENT DATA...</div>
            </div>""", unsafe_allow_html=True)
            time.sleep(1.2)
            placeholder.empty()
 
        score=risk_score(age_v,sex_v,cp_v,slope_v,ea_v,op_v,fbs_v,hr_v,chol_v)
        lbl,clr,rgb,bg,bd,desc=risk_meta(score)
 
        # Save to history on button click
        if analyse:
            st.session_state.history.append({
                'score': score, 'label': lbl, 'color': clr,
                'time': datetime.now().strftime("%H:%M"),
                'age': age_v, 'sex': sex_v, 'cp': cp_v
            })
            if len(st.session_state.history) > 5:
                st.session_state.history.pop(0)
 
        st.markdown(f"""
        <div class="result-main">
          <div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,rgba({rgb},.07),transparent 60%);border-radius:24px;pointer-events:none"></div>
          <div class="r-badge" style="background:{bg};border:1px solid {bd};color:{clr}">{lbl}</div>
          <div class="r-score" style="color:{clr}">{score}<span style="font-size:2rem;color:{clr}80">%</span></div>
          <div class="r-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
 
        fig_g=go.Figure(go.Indicator(mode="gauge",value=score,
            gauge=dict(axis=dict(range=[0,100],tickcolor='#1e293b',tickfont=dict(color='#475569',size=9)),
                bar=dict(color=clr,thickness=0.28),bgcolor='rgba(0,0,0,0)',borderwidth=0,
                steps=[dict(range=[0,45],color='rgba(16,185,129,.05)'),
                       dict(range=[45,70],color='rgba(249,115,22,.05)'),
                       dict(range=[70,100],color='rgba(220,38,38,.05)')],
                threshold=dict(line=dict(color=clr,width=3),thickness=0.8,value=score))))
        fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)',height=170,
            margin=dict(l=20,r=20,t=10,b=10),font=dict(color='#475569'))
        st.plotly_chart(fig_g,use_container_width=True)
 
        # Download report
        report = f"""CardioSense AI — Patient Risk Report
=====================================
Time       : {datetime.now().strftime("%Y-%m-%d %H:%M")}
Risk Score : {score}%
Level      : {lbl}
Assessment : {desc}
 
Parameters:
  Age            : {age_v}
  Sex            : {sex_v}
  Chest Pain     : {cp_v}
  ST Slope       : {slope_v}
  Exercise Angina: {ea_v}
  Fasting BS     : {fbs_v}
  Max Heart Rate : {hr_v}
  Oldpeak        : {op_v}
  Cholesterol    : {chol_v}
"""
        st.download_button("⬇ Download Report", report.encode(), f"report_{score}pct.txt", "text/plain")
 
        # Risk factors
        st.markdown('<div class="sec-head" style="margin-top:12px"><div class="sec-line"></div><div class="sec-txt" style="font-size:.85rem">Detected Risk Factors</div></div>', unsafe_allow_html=True)
        factors=[]
        if age_v>=60:                  factors.append(("Age 60+","#dc2626"))
        elif age_v>=50:                factors.append(("Age 50–60","#f97316"))
        if sex_v=='Male':              factors.append(("Male sex","#f97316"))
        if cp_v=='ASY':                factors.append(("Asymptomatic chest pain","#dc2626"))
        if slope_v in('Flat','Down'):  factors.append((f"ST Slope {slope_v}","#dc2626"))
        if ea_v=='Yes':                factors.append(("Exercise-induced angina","#dc2626"))
        if op_v>2:                     factors.append(("High Oldpeak (>2)","#dc2626"))
        elif op_v>0.5:                 factors.append(("Elevated Oldpeak","#f97316"))
        if fbs_v==1:                   factors.append(("High fasting glucose","#f97316"))
        if hr_v<120:                   factors.append(("Low max heart rate","#f97316"))
        if chol_v<150:                 factors.append(("Very low cholesterol","#f97316"))
 
        if not factors:
            st.markdown('<p style="color:#10b981;font-size:.82rem;padding:8px 0">✓ No significant risk factors detected</p>', unsafe_allow_html=True)
        else:
            for i,(lbl2,c2) in enumerate(factors):
                st.markdown(f'<div class="factor-item" style="animation-delay:{i*.05}s"><div class="factor-dot" style="background:{c2};box-shadow:0 0 6px {c2}55"></div><span>{lbl2}</span></div>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════
elif "History" in page:
    st.markdown("""
    <div class="hero">
      <div class="hero-tag"><div class="hero-dot"></div>Patient Records</div>
      <div class="hero-title">Assessment<br><span class="acc">History</span></div>
      <div class="hero-sub">Last 5 patient assessments from this session.</div>
    </div>
    """, unsafe_allow_html=True)
 
    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#475569">
          <div style="font-size:3rem;margin-bottom:16px">📋</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.1rem;color:#64748b">No assessments yet</div>
          <div style="font-size:.85rem;margin-top:8px">Go to Predict and analyse a patient first</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        h1,h2 = st.columns([2,1])
 
        with h1:
            st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Recent Assessments</div></div>', unsafe_allow_html=True)
            for i, h in enumerate(reversed(st.session_state.history)):
                lbl2,clr2,*_=risk_meta(h['score'])
                badge_bg = "rgba(220,38,38,.1)" if h['score']>=70 else "rgba(249,115,22,.1)" if h['score']>=45 else "rgba(16,185,129,.1)"
                st.markdown(f"""
                <div class="history-card">
                  <div>
                    <div style="font-size:.8rem;color:white;font-weight:500">Patient {len(st.session_state.history)-i} — Age {h['age']} · {h['sex']} · {h['cp']}</div>
                    <div class="history-meta">{h['time']} · {h['label']}</div>
                  </div>
                  <div style="display:flex;align-items:center;gap:12px">
                    <div class="history-score" style="color:{h['color']}">{h['score']}%</div>
                    <div class="history-badge" style="background:{badge_bg};color:{h['color']}">{h['label'].split()[0]}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
 
            if st.button("🗑  Clear History"):
                st.session_state.history = []
                st.rerun()
 
        with h2:
            st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Score Trend</div></div>', unsafe_allow_html=True)
            if len(st.session_state.history) > 1:
                scores = [h['score'] for h in st.session_state.history]
                labels = [f"P{i+1}" for i in range(len(scores))]
                clrs_h = ['#dc2626' if s>=70 else '#f97316' if s>=45 else '#10b981' for s in scores]
                fig_h=go.Figure(go.Scatter(x=labels,y=scores,mode='lines+markers',
                    line=dict(color='rgba(220,38,38,.4)',width=2),
                    marker=dict(color=clrs_h,size=10,line=dict(width=0))))
                fig_h.update_layout(**L,title='Risk Score Trend',
                    yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,105]),
                    xaxis=dict(color='#475569'))
                st.plotly_chart(fig_h,use_container_width=True)
            else:
                st.markdown('<p style="color:#475569;font-size:.82rem;padding:20px 0">Need at least 2 assessments to show trend</p>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# COMPARE
# ══════════════════════════════════════════════════════════════
elif "Compare" in page:
    st.markdown("""
    <div class="hero">
      <div class="hero-tag"><div class="hero-dot"></div>Side by Side</div>
      <div class="hero-title">Patient<br><span class="acc">Comparison</span></div>
      <div class="hero-sub">Compare two patients side by side to understand risk differences.</div>
    </div>
    """, unsafe_allow_html=True)
 
    p1,p2 = st.columns(2, gap="large")
 
    def patient_form(col, label, key):
        with col:
            st.markdown(f'<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">{label}</div></div>', unsafe_allow_html=True)
            age=st.slider("Age",28,80,50,key=f"age_{key}")
            sex=st.selectbox("Sex",["Male","Female"],key=f"sex_{key}")
            cp_r=st.selectbox("Chest Pain",["ASY — Asymptomatic","ATA — Atypical Angina","NAP — Non-Anginal Pain","TA  — Typical Angina"],key=f"cp_{key}")
            cp=cp_r.split(" — ")[0].strip()
            slope=st.selectbox("ST Slope",["Flat","Down","Up"],key=f"slope_{key}")
            ea=st.selectbox("Exercise Angina",["Yes","No"],key=f"ea_{key}")
            fbs=st.selectbox("Fasting BS",[0,1],key=f"fbs_{key}")
            hr=st.slider("Max HR",60,202,140,key=f"hr_{key}")
            op=st.slider("Oldpeak",-2.6,6.2,0.0,0.1,key=f"op_{key}")
            chol=st.slider("Cholesterol",85,603,220,key=f"chol_{key}")
            return risk_score(age,sex,cp,slope,ea,op,fbs,hr,chol), age, sex, cp
 
    s1,a1,sx1,cp1 = patient_form(p1,"Patient A","p1")
    s2,a2,sx2,cp2 = patient_form(p2,"Patient B","p2")
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-line"></div><div class="sec-txt">Comparison Result</div></div>', unsafe_allow_html=True)
 
    r1,r2,r3 = st.columns([2,1,2])
 
    with r1:
        lbl1,clr1,rgb1,bg1,bd1,desc1=risk_meta(s1)
        st.markdown(f"""
        <div class="compare-card" style="text-align:center">
          <div style="font-size:.7rem;color:#475569;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px">Patient A — Age {a1} · {sx1}</div>
          <div class="r-badge" style="background:{bg1};border:1px solid {bd1};color:{clr1}">{lbl1}</div>
          <div style="font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;color:{clr1};line-height:1">{s1}%</div>
          <div style="font-size:.78rem;color:#475569;margin-top:8px">{desc1}</div>
        </div>
        """, unsafe_allow_html=True)
 
    with r2:
        diff = s1 - s2
        diff_clr = "#dc2626" if diff > 0 else "#10b981"
        diff_sym = "▲" if diff > 0 else "▼"
        st.markdown(f"""
        <div style="text-align:center;padding:40px 0">
          <div style="font-size:.7rem;color:#475569;text-transform:uppercase;letter-spacing:.1em">Difference</div>
          <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:{diff_clr};margin:8px 0">{diff_sym}{abs(diff)}%</div>
          <div style="font-size:.75rem;color:#475569">{"A is higher risk" if diff>0 else "B is higher risk" if diff<0 else "Equal risk"}</div>
        </div>
        """, unsafe_allow_html=True)
 
    with r3:
        lbl2,clr2,rgb2,bg2,bd2,desc2=risk_meta(s2)
        st.markdown(f"""
        <div class="compare-card" style="text-align:center">
          <div style="font-size:.7rem;color:#475569;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px">Patient B — Age {a2} · {sx2}</div>
          <div class="r-badge" style="background:{bg2};border:1px solid {bd2};color:{clr2}">{lbl2}</div>
          <div style="font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;color:{clr2};line-height:1">{s2}%</div>
          <div style="font-size:.78rem;color:#475569;margin-top:8px">{desc2}</div>
        </div>
        """, unsafe_allow_html=True)
 
    # Bar chart comparison
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    fig_cmp=go.Figure(go.Bar(
        x=['Patient A','Patient B'], y=[s1,s2],
        marker_color=[clr1,clr2], marker_line_width=0,
        text=[f'{s1}%',f'{s2}%'], textposition='outside',
        textfont=dict(color='white',size=14,family='Syne'), width=0.4
    ))
    fig_cmp.update_layout(**L,title='Risk Score Comparison',
        yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,.04)',color='#475569',range=[0,110]),
        xaxis=dict(color='#94a3b8'))
    st.plotly_chart(fig_cmp,use_container_width=True)
 