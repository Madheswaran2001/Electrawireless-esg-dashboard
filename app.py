import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ElectraWireless ESG Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background-color: #0D0D12; }
  .block-container { padding-top: 0rem; padding-bottom: 2rem; }

  /* HEADER */
  .hero-header {
    background: linear-gradient(135deg, #1a0a3d 0%, #0D0D12 60%);
    border-bottom: 1px solid rgba(255,255,255,0.14);
    padding: 2rem 2.5rem 1.5rem;
    margin: -1rem -1rem 2rem -1rem;
    border-radius: 0 0 12px 12px;
  }
  .hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem; font-weight: 700;
    color: #F0EEF8; letter-spacing: -0.8px; margin-bottom: 4px;
  }
  .hero-sub { color: #9490B0; font-size: 13px; }
  .hero-badge {
    display: inline-block;
    background: rgba(94,223,168,0.12);
    border: 1px solid rgba(94,223,168,0.3);
    color: #5EDFA8; font-size: 12px; font-weight: 600;
    padding: 5px 14px; border-radius: 20px; margin-top: 10px;
  }

  /* KPI METRIC CARDS */
  .kpi-box {
    background: #15151E;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px 18px;
    margin-bottom: 12px;
    position: relative; overflow: hidden;
  }
  .kpi-box-top { height: 3px; border-radius: 3px 3px 0 0; position: absolute; top:0; left:0; right:0; }
  .kpi-label { font-size: 10px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #9490B0; margin-bottom: 8px; }
  .kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; line-height: 1; }
  .kpi-trend { font-size: 12px; margin-top: 6px; }
  .kpi-sub { font-size: 11px; color: #9490B0; margin-top: 4px; }
  .trend-up { color: #5EDFA8; }
  .trend-dn { color: #FF7B5C; }

  /* SECTION TITLE */
  .section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px; font-weight: 600;
    color: #F0EEF8; margin-bottom: 14px; margin-top: 8px;
    display: flex; align-items: center; gap: 8px;
  }

  /* CARD WRAPPER */
  .card-wrap {
    background: #15151E;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 20px;
    margin-bottom: 16px;
  }
  .card-title {
    font-size: 10px; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
    color: #9490B0; margin-bottom: 14px;
  }

  /* SCORE BARS */
  .score-row { display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
  .score-row:last-child { border-bottom: none; }
  .score-label-text { flex: 1; font-size: 13px; color: #F0EEF8; }
  .score-bar-bg { flex: 2; height: 6px; background: #1C1C2A; border-radius: 3px; overflow: hidden; }
  .score-bar-fill { height: 100%; border-radius: 3px; }
  .score-val-text { font-size: 13px; font-weight: 600; min-width: 36px; text-align: right; }

  /* COMPETITOR ROW */
  .comp-row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
  .comp-name-text { font-size: 12px; color: #F0EEF8; min-width: 130px; }
  .comp-bar-bg { flex: 1; height: 8px; background: #1C1C2A; border-radius: 4px; overflow: hidden; }
  .comp-bar-fill { height: 100%; border-radius: 4px; }
  .comp-val-text { font-size: 12px; font-weight: 600; min-width: 32px; text-align: right; }

  /* IMPACT BOX */
  .impact-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: 10px; }
  .impact-box { background: #1C1C2A; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 16px; text-align: center; }
  .impact-icon { font-size: 26px; margin-bottom: 8px; }
  .impact-val { font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; color: #5EDFA8; }
  .impact-desc { font-size: 11px; color: #9490B0; margin-top: 4px; line-height: 1.4; }

  /* TABLE */
  .gov-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }
  .gov-table th { padding: 9px 12px; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9490B0; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.14); }
  .gov-table td { padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.06); color: #F0EEF8; vertical-align: middle; }
  .gov-table tr:last-child td { border-bottom: none; }
  .pill { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; }
  .pill-green { background: rgba(94,223,168,0.15); color: #5EDFA8; }
  .pill-amber { background: rgba(255,209,102,0.15); color: #FFD166; }
  .pill-red { background: rgba(255,123,92,0.15); color: #FF7B5C; }
  .chk { color: #5EDFA8; font-weight: 700; }
  .cross { color: #FF7B5C; }

  /* TABS */
  .stTabs [data-baseweb="tab-list"] {
    gap: 0; background-color: #15151E;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #9490B0 !important; font-size: 13px;
    padding: 12px 20px; border-radius: 0;
    border-bottom: 2px solid transparent !important;
  }
  .stTabs [aria-selected="true"] {
    color: #7C5CFF !important;
    border-bottom: 2px solid #7C5CFF !important;
    background-color: transparent !important;
  }
  .stTabs [data-baseweb="tab-panel"] { background-color: #0D0D12 !important; padding: 24px 4px; }

  /* Plotly chart bg */
  .js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9490B0", family="Inter"),
    margin=dict(l=30, r=20, t=30, b=30),
)

# Default axis/legend styles reused per chart
_LEGEND = dict(font=dict(size=11, color="#9490B0"), bgcolor="rgba(0,0,0,0)")
_XAXIS  = dict(gridcolor="rgba(255,255,255,0.06)", color="#9490B0")
_YAXIS  = dict(gridcolor="rgba(255,255,255,0.06)", color="#9490B0")

# ── DATA ──────────────────────────────────────────────────────────────────────
years = [2026,2027,2028,2029,2030,2031,2032,2033]
env_traj  = [88,90,91,93,94,95,96,97]
soc_traj  = [82,84,86,87,89,90,91,93]
gov_traj  = [79,81,83,85,86,88,89,91]
comp_traj = [83,85,87,88,90,91,92,94]

competitors = {
    "Company": ["ElectraWireless","WiTricity","Ossia","Resonant Link","Trad. Players"],
    "Overall": [83, 65, 58, 60, 52],
    "Environmental": [88, 60, 52, 55, 40],
    "Social": [82, 58, 55, 52, 65],
    "Governance": [79, 72, 65, 63, 58],
}
df_comp = pd.DataFrame(competitors)

env_bar_labels = ["Copper CO₂ equiv.","Aluminium CO₂ equiv.","Total CO₂ Avoided","Copper Saved (tons)","Aluminium Saved (tons)"]
env_bar_vals   = [17500, 60000, 77500, 5000, 5000]
env_bar_colors = ["#5EDFA8","#7C5CFF","#FF7B5C","#5EDFA8","#7C5CFF"]

finance_years = [f"Y{i}" for i in range(1,11)]
net_profit  = [-0.66,-1.23,1.59,12.67,18.48,28.47,42.85,49.67,33.47,54.34]
cash_inflow = [0, 0.5, 4, 14, 21, 48, 68, 75, 103, 152]

mat_data = [
    (9.2, 9.5, 18, "E-Waste Reduction", "#5EDFA8"),
    (8.5, 8.8, 14, "CO₂ Reduction", "#5EDFA8"),
    (7.2, 7.5, 11, "Supply Chain", "#5EDFA8"),
    (6.0, 6.5, 8,  "Water & Resources", "#5EDFA8"),
    (9.0, 9.2, 16, "Safety Innovation", "#7C5CFF"),
    (7.8, 7.0, 12, "Workforce Diversity","#7C5CFF"),
    (6.5, 6.0, 9,  "Community Impact",  "#7C5CFF"),
    (5.5, 5.5, 8,  "Health (Elly AI)",  "#7C5CFF"),
    (8.0, 8.5, 13, "Regulatory Compliance","#FFD166"),
    (7.5, 8.7, 14, "IP Protection",     "#FFD166"),
    (7.5, 7.0, 10, "Data Privacy",      "#FFD166"),
    (6.0, 7.0, 9,  "Investor Transparency","#FFD166"),
    (8.8, 9.0, 15, "AI Energy Efficiency","#FF7B5C"),
    (8.0, 8.0, 12, "WPT Technology",    "#FF7B5C"),
    (6.5, 7.5, 10, "Foreign Object Safety","#FF7B5C"),
    (5.0, 6.0, 8,  "App Platform (Elly)","#FF7B5C"),
]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
    <div style="width:40px;height:40px;background:#7C5CFF;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;">⚡</div>
    <div>
      <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:#F0EEF8;">ElectraWireless</div>
      <div style="font-size:11px;color:#9490B0;letter-spacing:1.5px;text-transform:uppercase;">ESG Dashboard · 2026</div>
    </div>
    <div style="margin-left:auto;"><span class="hero-badge">✦ ESG Rating: AA</span></div>
  </div>
  <div class="hero-title">Sustainability &amp; ESG Performance</div>
  <div class="hero-sub">Tracking Environmental, Social &amp; Governance impact across all phases — Q1 2026 Stakeholder Report</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Overview", "🌿 Environmental", "🤝 Social", "🏛️ Governance", "🎯 Materiality Map", "⚔️ Competitive"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    kpi_data = [
        (c1, "Environmental Score", "88", "#5EDFA8", "▲ +12 vs industry avg", "MSCI A rating equivalent"),
        (c2, "Social Score", "82", "#7C5CFF", "▲ +8 vs industry avg", "20+ nationalities on team"),
        (c3, "Governance Score", "79", "#FFD166", "▲ +6 vs industry avg", "US-registered, global ops"),
        (c4, "CO₂ Avoided (annual)", "77.5K", "#FF7B5C", "▲ Tons equivalent", "Cu + Al waste elimination"),
    ]
    for col, label, val, color, trend, sub in kpi_data:
        with col:
            st.markdown(f"""
            <div class="kpi-box">
              <div class="kpi-box-top" style="background:{color};"></div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-trend trend-up">{trend}</div>
              <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    # Radar + Score Breakdown
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="card-wrap"><div class="card-title">Overall ESG Radar — ElectraWireless vs. Competitors</div>', unsafe_allow_html=True)
        radar_labels = ["E-Waste Reduction","Energy Efficiency","Safety Innovation","Workforce Diversity","Governance Transparency","Market Coverage"]
        radar_datasets = [
            ("ElectraWireless", [92,85,90,90,79,95], "#7C5CFF"),
            ("WiTricity",       [45,60,50,55,65,45], "#5EDFA8"),
            ("Ossia",           [40,55,45,50,60,40], "#FFD166"),
            ("Resonant Link",   [42,58,48,52,63,38], "#00CFFF"),
            ("Trad. Players",   [30,40,30,60,55,65], "#FF7B5C"),
        ]
        def hex_to_rgba(hex_color, alpha=0.15):
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return f"rgba({r},{g},{b},{alpha})"

        fig_radar = go.Figure()
        for name, vals, color in radar_datasets:
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=radar_labels + [radar_labels[0]],
                fill="toself" if name == "ElectraWireless" else "none",
                fillcolor=hex_to_rgba(color, 0.15) if name == "ElectraWireless" else "rgba(0,0,0,0)",
                line=dict(color=color, width=2 if name=="ElectraWireless" else 1.5,
                          dash="solid" if name=="ElectraWireless" else "dot"),
                name=name
            ))
        fig_radar.update_layout(**PLOT_LAYOUT, height=340,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=9,color="#9490B0"), tickcolor="#9490B0"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=10,color="#9490B0"))
            ),
            legend=dict(font=dict(size=10,color="#9490B0"),bgcolor="rgba(0,0,0,0)",orientation="h",y=-0.15),
            showlegend=True,
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card-wrap"><div class="card-title">ESG Score Breakdown — ElectraWireless</div>', unsafe_allow_html=True)
        scores = [
            ("Carbon Footprint Reduction", 92, "#5EDFA8"),
            ("E-Waste Reduction", 88, "#5EDFA8"),
            ("Energy Efficiency", 85, "#5EDFA8"),
            ("Workforce Diversity", 90, "#7C5CFF"),
            ("Safety Innovation", 87, "#7C5CFF"),
            ("Community Impact", 78, "#7C5CFF"),
            ("Regulatory Compliance", 82, "#FFD166"),
            ("Transparency & Reporting", 76, "#FFD166"),
        ]
        for label, val, color in scores:
            st.markdown(f"""
            <div class="score-row">
              <div class="score-label-text">{label}</div>
              <div class="score-bar-bg"><div class="score-bar-fill" style="width:{val}%;background:{color};"></div></div>
              <div class="score-val-text" style="color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ESG Trajectory
    st.markdown('<div class="card-wrap"><div class="card-title">Projected ESG Score Trajectory (2026–2033)</div>', unsafe_allow_html=True)
    fig_traj = go.Figure()
    traj_sets = [
        ("Environmental", env_traj,  "#5EDFA8"),
        ("Social",        soc_traj,  "#7C5CFF"),
        ("Governance",    gov_traj,  "#FFD166"),
        ("Composite",     comp_traj, "rgba(255,255,255,0.3)"),
    ]
    for name, data, color in traj_sets:
        dash = "dot" if name == "Composite" else "solid"
        fill = "tozeroy" if name != "Composite" else "none"
        fillcol = color.replace(")", ",0.08)").replace("rgba(","rgba(") if "#" in color else "rgba(0,0,0,0)"
        if "#" in color:
            r,g,b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
            fillcol = f"rgba({r},{g},{b},0.08)"
        fig_traj.add_trace(go.Scatter(x=years, y=data, name=name,
            line=dict(color=color, width=2, dash=dash),
            fill=fill if name != "Composite" else "none",
            fillcolor=fillcol if name != "Composite" else "rgba(0,0,0,0)",
            mode="lines+markers", marker=dict(size=5, color=color)))
    fig_traj.update_layout(**PLOT_LAYOUT, height=280, xaxis=_XAXIS, yaxis=dict(range=[70,100],gridcolor="rgba(255,255,255,0.06)",color="#9490B0"), legend=_LEGEND)
    st.plotly_chart(fig_traj, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — ENVIRONMENTAL
# ════════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    c1, c2, c3, c4 = st.columns(4)
    env_kpis = [
        (c1,"Annual CO₂ Avoided","77.5K tons","#5EDFA8","Cu + Al waste elimination"),
        (c2,"Copper Saved","5K tons","#5EDFA8","Annual material preservation"),
        (c3,"Aluminium Saved","5K tons","#5EDFA8","Annual material preservation"),
        (c4,"WPT Efficiency",">80%","#5EDFA8","vs cable energy loss"),
    ]
    for col,label,val,color,sub in env_kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-box">
              <div class="kpi-box-top" style="background:{color};"></div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="card-wrap"><div class="card-title">Annual Material & CO₂ Savings</div>', unsafe_allow_html=True)
        fig_env = go.Figure(go.Bar(
            x=env_bar_labels, y=env_bar_vals,
            marker_color=env_bar_colors, marker_line_width=0,
            text=[f"{v:,}" for v in env_bar_vals], textposition="outside",
            textfont=dict(color="#9490B0", size=10)
        ))
        fig_env.update_layout(**PLOT_LAYOUT, height=300, legend=_LEGEND,
            xaxis=dict(tickfont=dict(size=10),gridcolor="rgba(0,0,0,0)",color="#9490B0"),
            yaxis=dict(tickformat=",", gridcolor="rgba(255,255,255,0.06)", color="#9490B0")
        )
        st.plotly_chart(fig_env, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card-wrap"><div class="card-title">Carbon Footprint Reduction by Phase</div>', unsafe_allow_html=True)
        fig_donut = go.Figure(go.Pie(
            labels=["Kitchen (P1)","E-bikes (P2)","Robotics (P3)","Furniture (P4)","EV (P5)"],
            values=[20,25,22,15,18],
            hole=0.65,
            marker=dict(colors=["#5EDFA8","#7C5CFF","#FFD166","#FF7B5C","#A0A0FF"],
                        line=dict(color="#15151E", width=2))
        ))
        fig_donut.update_layout(**PLOT_LAYOUT, height=300,
            legend=dict(font=dict(size=10,color="#9490B0"),bgcolor="rgba(0,0,0,0)",orientation="v",x=1.0),
            showlegend=True)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card-wrap"><div class="card-title">10-Year Environmental Impact Projection</div>', unsafe_allow_html=True)
    ten_years = [f"Y{i}" for i in range(1,11)]
    fig_env10 = go.Figure()
    fig_env10.add_trace(go.Scatter(x=ten_years, y=[5,8,12,18,28,42,55,68,78,92],
        name="CO₂ Avoided (K tons)", line=dict(color="#5EDFA8",width=2), fill="tozeroy",
        fillcolor="rgba(94,223,168,0.1)", mode="lines+markers", marker=dict(size=5)))
    fig_env10.add_trace(go.Scatter(x=ten_years, y=[80,81,82,83,84,85,86,87,87,88],
        name="Efficiency %", line=dict(color="#FFD166",width=2,dash="dot"),
        mode="lines+markers", marker=dict(size=4), yaxis="y2"))
    fig_env10.update_layout(**PLOT_LAYOUT, height=280, xaxis=_XAXIS, yaxis=_YAXIS, legend=_LEGEND,
        yaxis2=dict(overlaying="y", side="right", showgrid=False, color="#FFD166",
                    ticksuffix="%", range=[75,95]))
    st.plotly_chart(fig_env10, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🌱 Environmental Initiatives</div>', unsafe_allow_html=True)
    impacts = [
        ("⚡",">80%","Wireless Power Transfer efficiency — reduces energy loss vs traditional cables"),
        ("♻️","10K tons","Annual metal waste eliminated — aluminium & copper preserved from landfill"),
        ("🛡️","Zero","Short-circuit risk eliminated — reduces hazardous e-waste from cable failures"),
        ("🤖","AI-managed","Real-time energy management system — AI optimises power delivery dynamically"),
        ("🚲","$15B","Sustainable e-bike market supported — clean transport wireless charging"),
        ("🏙️","Phase 5","EV wireless charging infra — zero-cable cities & public transport hubs"),
    ]
    st.markdown('<div class="impact-grid">', unsafe_allow_html=True)
    for icon, val, desc in impacts:
        st.markdown(f"""
        <div class="impact-box">
          <div class="impact-icon">{icon}</div>
          <div class="impact-val">{val}</div>
          <div class="impact-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — SOCIAL
# ════════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    c1, c2, c3, c4 = st.columns(4)
    soc_kpis = [
        (c1,"Team Nationalities","20+","#7C5CFF","Global diverse team"),
        (c2,"Women in Leadership","33%","#7C5CFF","Leadership diversity"),
        (c3,"Safety Improvement","100%","#7C5CFF","Zero short-circuit risk"),
        (c4,"Households Impacted","80%","#7C5CFF","Cable clutter resolved"),
    ]
    for col,label,val,color,sub in soc_kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-box">
              <div class="kpi-box-top" style="background:{color};"></div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="card-wrap"><div class="card-title">Team Composition by Department</div>', unsafe_allow_html=True)
        fig_team = go.Figure(go.Pie(
            labels=["Engineering (9)","Biz Dev & Mktg (8)","Finance (5)","App Dev (4)"],
            values=[9,8,5,4], hole=0.65,
            marker=dict(colors=["#7C5CFF","#5EDFA8","#FFD166","#FF7B5C"],
                        line=dict(color="#15151E",width=2))
        ))
        fig_team.update_layout(**PLOT_LAYOUT, height=300, legend=_LEGEND)
        st.plotly_chart(fig_team, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card-wrap"><div class="card-title">Academic & Innovation Partners</div>', unsafe_allow_html=True)
        partners = [
            ("Hong Kong Polytechnic (R&D)", "Active", "#7C5CFF"),
            ("RMIT University, Australia",  "Active", "#7C5CFF"),
            ("TALim Belgium (Youth)",        "Active", "#7C5CFF"),
            ("MIT (Research Ally)",          "Target", "#5EDFA8"),
            ("Kaggle AI Competition Rank",   "#4",     "#FFD166"),
            ("Global Media Coverage",        "10+",    "#5EDFA8"),
            ("Countries Active In",          "9",      "#5EDFA8"),
        ]
        for label, val, color in partners:
            st.markdown(f"""
            <div class="score-row">
              <div class="score-label-text">{label}</div>
              <div class="score-val-text" style="color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card-wrap"><div class="card-title">Social Impact — Problem Solved for End Users</div>', unsafe_allow_html=True)
    prob_labels = ["Cable Clutter","E-Waste","Electrical Hazards","Adapter Incompatibility","Metal Disposal","Energy Inefficiency"]
    affected    = [80, 65, 55, 70, 45, 60]
    ew_impact   = [95, 88, 97, 92, 85, 84]
    fig_social = go.Figure()
    fig_social.add_trace(go.Bar(name="Users Affected (%)", x=prob_labels, y=affected,
        marker_color="rgba(124,92,255,0.7)", marker_cornerradius=4))
    fig_social.add_trace(go.Bar(name="EW Solution Impact Score", x=prob_labels, y=ew_impact,
        marker_color="rgba(94,223,168,0.5)", marker_cornerradius=4))
    fig_social.update_layout(**PLOT_LAYOUT, height=300, barmode="group", xaxis=_XAXIS, yaxis=_YAXIS,
        legend=dict(orientation="h", y=-0.2, bgcolor="rgba(0,0,0,0)", font=dict(size=10,color="#9490B0")))
    st.plotly_chart(fig_social, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — GOVERNANCE
# ════════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    c1, c2, c3, c4 = st.columns(4)
    gov_kpis = [
        (c1, "Registration", "🇺🇸 USA", "#FFD166", "Delaware C-Corp"),
        (c2, "Board Advisors", "6", "#FFD166", "Expert advisory board"),
        (c3, "IP Protection", "US Patents", "#FFD166", "Filed & pending"),
        (c4, "Governance Score", "79/100", "#FFD166", "▲ +6 vs industry avg"),
    ]
    for col,label,val,color,sub in gov_kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-box">
              <div class="kpi-box-top" style="background:{color};"></div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color};font-size:1.8rem;">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="card-wrap"><div class="card-title">Governance Checklist</div>', unsafe_allow_html=True)
        gov_checks = [
            ("SEC-Reg CF Compliant", "✔", "chk"),
            ("US Patent Filed", "✔", "chk"),
            ("GDPR Data Policy", "✔", "chk"),
            ("Audited Financials", "In Progress", "pill-amber"),
            ("Independent Directors", "✔", "chk"),
            ("Anti-Corruption Policy", "✔", "chk"),
            ("ESG Reporting Framework", "GRI Aligned", "pill-green"),
            ("Whistleblower Policy", "✔", "chk"),
        ]
        st.markdown("""<table class="gov-table"><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>""", unsafe_allow_html=True)
        for item, status, cls in gov_checks:
            if cls == "chk":
                st.markdown(f'<tr><td>{item}</td><td class="chk">✔ Done</td></tr>', unsafe_allow_html=True)
            else:
                st.markdown(f'<tr><td>{item}</td><td><span class="pill {cls}">{status}</span></td></tr>', unsafe_allow_html=True)
        st.markdown("</tbody></table></div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card-wrap"><div class="card-title">Funding Allocation Transparency ($5M Seed)</div>', unsafe_allow_html=True)
        fig_fund = go.Figure(go.Pie(
            labels=["Marketing & Sales 25%","Tech Development 20%","Mfg & Supply 20%","R&D 15%","Contingency 10%","Operations 10%"],
            values=[25,20,20,15,10,10], hole=0.6,
            marker=dict(colors=["#7C5CFF","#5EDFA8","#FFD166","#FF7B5C","#A0A0FF","#F0A0FF"],
                        line=dict(color="#15151E",width=2))
        ))
        fig_fund.update_layout(**PLOT_LAYOUT, height=300, legend=_LEGEND)
        st.plotly_chart(fig_fund, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card-wrap"><div class="card-title">10-Year Financial Forecast & Governance Milestones</div>', unsafe_allow_html=True)
    fig_fin = go.Figure()
    bar_colors = ["rgba(255,123,92,0.7)" if v < 0 else "rgba(94,223,168,0.7)" for v in net_profit]
    fig_fin.add_trace(go.Bar(x=finance_years, y=net_profit, name="Net Profit/Loss ($M)",
        marker_color=bar_colors, marker_line_width=0))
    fig_fin.add_trace(go.Scatter(x=finance_years, y=cash_inflow, name="Cash Inflow ($M)",
        line=dict(color="#FFD166",width=2), mode="lines+markers", marker=dict(size=5)))
    fig_fin.update_layout(**PLOT_LAYOUT, height=300, xaxis=_XAXIS,
        yaxis=dict(ticksuffix="M", tickprefix="$", gridcolor="rgba(255,255,255,0.06)", color="#9490B0"),
        legend=dict(orientation="h",y=-0.2,bgcolor="rgba(0,0,0,0)",font=dict(size=10,color="#9490B0")))
    st.plotly_chart(fig_fin, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — MATERIALITY MAP
# ════════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""
    <div class="card-wrap">
      <div class="card-title">What is a Materiality Map?</div>
      <p style="color:#9490B0;font-size:13px;line-height:1.6;">
        A materiality map shows which ESG topics matter most — both to stakeholders (X-axis) and to the business (Y-axis).
        Bubble size represents the combined priority weight. Topics in the top-right corner are the highest priority.
        Each color represents a category: <span style="color:#5EDFA8;">■ Environmental</span>
        <span style="color:#7C5CFF;"> ■ Social</span>
        <span style="color:#FFD166;"> ■ Governance</span>
        <span style="color:#FF7B5C;"> ■ Technology</span>
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_stats, col_map = st.columns([1, 3])
    with col_stats:
        st.markdown("""
        <div class="kpi-box" style="text-align:center;">
          <div class="kpi-box-top" style="background:#5EDFA8;"></div>
          <div class="kpi-label">High Priority Topics</div>
          <div class="kpi-value" style="color:#5EDFA8;font-size:2.5rem;">6</div>
        </div>
        <div class="kpi-box" style="text-align:center;">
          <div class="kpi-box-top" style="background:#7C5CFF;"></div>
          <div class="kpi-label">Topics Tracked</div>
          <div class="kpi-value" style="color:#7C5CFF;font-size:2.5rem;">16</div>
        </div>
        <div class="kpi-box" style="text-align:center;">
          <div class="kpi-box-top" style="background:#FFD166;"></div>
          <div class="kpi-label">Categories</div>
          <div class="kpi-value" style="color:#FFD166;font-size:2.5rem;">4</div>
        </div>
        """, unsafe_allow_html=True)

    with col_map:
        st.markdown('<div class="card-wrap"><div class="card-title">Materiality Bubble Map — ElectraWireless 2026</div>', unsafe_allow_html=True)
        fig_mat = go.Figure()
        for x, y, r, label, color in mat_data:
            fig_mat.add_trace(go.Scatter(
                x=[x], y=[y], mode="markers+text",
                marker=dict(size=r*2, color=color+"AA", line=dict(color=color,width=1.5)),
                text=[label], textposition="top center",
                textfont=dict(size=9, color="#F0EEF8"),
                name=label, showlegend=False,
                hovertemplate=f"<b>{label}</b><br>Stakeholder Importance: {x}<br>Business Impact: {y}<extra></extra>"
            ))
        fig_mat.update_layout(**PLOT_LAYOUT, height=480, legend=_LEGEND,
            xaxis=dict(range=[4,10.5], title="Importance to Stakeholders →",
                       titlefont=dict(size=11), gridcolor="rgba(255,255,255,0.06)", color="#9490B0"),
            yaxis=dict(range=[4,10.5], title="Business Impact →",
                       titlefont=dict(size=11), gridcolor="rgba(255,255,255,0.06)", color="#9490B0"))
        st.plotly_chart(fig_mat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 6 — COMPETITIVE
# ════════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.markdown('<div class="card-wrap"><div class="card-title">Overall ESG Score Comparison</div>', unsafe_allow_html=True)
        comp_entries = [
            ("ElectraWireless", 83, "linear-gradient(90deg,#5EDFA8,#7C5CFF)", "#5EDFA8", True),
            ("WiTricity",       65, "#555555", "#F0EEF8", False),
            ("Ossia",           58, "#555555", "#F0EEF8", False),
            ("Resonant Link",   60, "#555555", "#F0EEF8", False),
            ("Trad. Players",   52, "#444444", "#F0EEF8", False),
        ]
        for name, val, bg, color, bold in comp_entries:
            bstyle = "font-weight:600;" if bold else ""
            st.markdown(f"""
            <div class="comp-row">
              <div class="comp-name-text" style="color:{color};{bstyle}">{name}</div>
              <div class="comp-bar-bg"><div class="comp-bar-fill" style="width:{val}%;background:{bg};"></div></div>
              <div class="comp-val-text" style="color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="card-title">Sub-Score Breakdown</div>', unsafe_allow_html=True)
        fig_comp = go.Figure()
        bar_data = [
            ("ElectraWireless", [88,82,79], "rgba(94,223,168,0.8)"),
            ("WiTricity",       [60,58,72], "rgba(100,100,120,0.7)"),
            ("Ossia",           [52,55,65], "rgba(80,80,100,0.6)"),
            ("Trad. Players",   [40,65,58], "rgba(60,60,80,0.5)"),
        ]
        for name, vals, color in bar_data:
            fig_comp.add_trace(go.Bar(name=name, x=["Environmental","Social","Governance"], y=vals,
                marker_color=color, marker_line_width=0))
        fig_comp.update_layout(**PLOT_LAYOUT, height=240, barmode="group", xaxis=_XAXIS,
            yaxis=dict(range=[0,100],gridcolor="rgba(255,255,255,0.06)",color="#9490B0"),
            legend=dict(orientation="h",y=-0.25,bgcolor="rgba(0,0,0,0)",font=dict(size=10,color="#9490B0")))
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card-wrap"><div class="card-title">Feature Matrix — ElectraWireless vs. Competitors</div>', unsafe_allow_html=True)
        feature_matrix = [
            ("Wireless Power",        True,  True,  True,  True,  False),
            ("Heating Capability",    True,  False, False, False, True),
            ("Smart App & Data",      True,  False, True,  False, True),
            ("Foreign Object Detect", True,  False, False, False, False),
            ("OEM Customization",     True,  True,  True,  True,  True),
            ("Kitchen Appliances",    True,  False, False, False, True),
            ("E-Bikes",               True,  False, False, False, True),
            ("Robotics",              True,  True,  False, False, True),
            ("EV Charging",           True,  True,  False, False, True),
            ("Medical Devices",       True,  False, False, True,  False),
        ]
        cols_h = ["Feature","EW","WiTri","Ossia","ResLink","Trad."]
        header_row = "".join(f'<th style="color:{"#5EDFA8" if h=="EW" else "#9490B0"}">{h}</th>' for h in cols_h)
        st.markdown(f'<table class="gov-table"><thead><tr>{header_row}</tr></thead><tbody>', unsafe_allow_html=True)
        for row in feature_matrix:
            cells = f'<td style="color:#F0EEF8;">{row[0]}</td>'
            for val in row[1:]:
                cells += f'<td class="{"chk" if val else "cross"}">{"✔" if val else "✗"}</td>'
            st.markdown(f"<tr>{cells}</tr>", unsafe_allow_html=True)
        st.markdown("</tbody></table></div>", unsafe_allow_html=True)

    st.markdown('<div class="card-wrap"><div class="card-title">Market Opportunity by Sector — ElectraWireless vs. Best Competitor ($B TAM)</div>', unsafe_allow_html=True)
    sectors = ["Kitchen Appliances","E-Bikes","Robotics","EV Charging","IoT/Office","Medical Devices"]
    fig_mkt = go.Figure()
    fig_mkt.add_trace(go.Bar(name="ElectraWireless", x=sectors, y=[200,20,80,200,140,50],
        marker_color="rgba(94,223,168,0.8)", marker_line_width=0))
    fig_mkt.add_trace(go.Bar(name="Best Competitor", x=sectors, y=[0,0,80,200,0,50],
        marker_color="rgba(100,100,120,0.5)", marker_line_width=0))
    fig_mkt.update_layout(**PLOT_LAYOUT, height=280, barmode="group", xaxis=_XAXIS,
        yaxis=dict(tickprefix="$", ticksuffix="B", gridcolor="rgba(255,255,255,0.06)", color="#9490B0"),
        legend=dict(orientation="h", y=-0.2, bgcolor="rgba(0,0,0,0)", font=dict(size=10,color="#9490B0")))
    st.plotly_chart(fig_mkt, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:#6a6888;font-size:11px;border-top:1px solid rgba(255,255,255,0.06);margin-top:2rem;">
  ElectraWireless · ESG Dashboard 2026 · Q1 Stakeholder Report · Confidential
</div>
""", unsafe_allow_html=True)
