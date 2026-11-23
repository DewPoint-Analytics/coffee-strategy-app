"""Coffee Shop Strategy: a business dashboard built from 15 runs of the
Coffee Shop Inc. simulation (Sim Institute / Harvard Business Impact).
Every figure comes from data.json, transcribed from the game's own result screens.
© 2026 Shabnam Mohammed Sameer (DewPoint Analytics). All rights reserved."""

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Coffee Shop Strategy · Business Dashboard", page_icon="☕", layout="wide")

# ---------- palette (validated for colour-vision deficiency) ----------
ROSE, OCHRE, TEAL, SAGE, INDIGO = "#a8502e", "#d39543", "#0f8aa0", "#6f9a4c", "#5b6fae"
RUN_COLORS = [ROSE, OCHRE, TEAL, SAGE, INDIGO]
GAIN, LOSS = TEAL, "#c2502f"
LEVEL_COLORS = {"L1": OCHRE, "L2": ROSE, "L3": TEAL}
INK, MUTED, GRID = "#2e1810", "#7d6656", "#eadcc4"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,600&family=DM+Sans:wght@400;500;700&display=swap');
html, body, [class*="css"], .stMarkdown, p, li, label {font-family:'DM Sans',sans-serif}
h1, h2, h3 {font-family:'Playfair Display',serif !important; color:#3d1a10 !important; font-weight:600 !important}
h1 em, h2 em {color:#b5543a}
.block-container {padding-top:3.4rem; max-width:1240px}
.band {height:12px; margin:4px 0 18px; background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='22' height='14'%3E%3Crect width='22' height='14' fill='%23fbf5ea'/%3E%3Cpath d='M11 2 L18 7 L11 12 L4 7Z' fill='%23ecaaa1'/%3E%3C/svg%3E") repeat-x; background-size:16px 12px}
.kicker {font:700 12px 'DM Sans'; letter-spacing:.2em; text-transform:uppercase; color:#d39543; margin-bottom:-6px}
.lede {font-size:1.05rem; color:#4a3328; max-width:760px}
div[data-testid="stMetric"] {background:#fffaf1; border:1px solid #eadcc4; border-radius:120px 120px 14px 14px / 34px 34px 14px 14px; padding:22px 18px 14px; text-align:center}
div[data-testid="stMetric"] label p {font-weight:700; letter-spacing:.08em; text-transform:uppercase; font-size:.72rem; color:#7d6656}
div[data-testid="stMetricValue"] {font-family:'Playfair Display',serif; color:#7a3320}
div[data-testid="stMetric"] {min-height:132px}
div[data-testid="stMetricDelta"] svg {display:none}
div[data-testid="stMetricDelta"] {background:#f3e6cf !important; color:#7a3320 !important}
.stTabs [data-baseweb="tab"] {font-weight:700}
.card {background:#fffaf1; border:1px solid #eadcc4; border-radius:14px; padding:16px 18px; margin-bottom:12px}
.card b {color:#7a3320}
.note {font-size:.82rem; color:#7d6656}
.explore {line-height:2}
.explore a {color:#7a3320 !important; text-decoration:none; font-weight:600}
.explore a:hover {text-decoration:underline}
footer {visibility:hidden}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load():
    d = json.loads((Path(__file__).parent / "data.json").read_text())
    runs = pd.DataFrame(d["runs"])
    l12 = pd.DataFrame(d["l12"])
    l3 = pd.DataFrame(d["l3"])
    exp = pd.DataFrame(d["experiments"])
    rules = pd.DataFrame(d["rules"])
    runs["Pct"] = runs["% of target"] * 100
    runs["Short"] = runs["Level"] + " R" + runs["Run"].astype(str)
    return runs, l12, l3, exp, rules


runs, l12, l3, exp, rules = load()


def money(v, short=False):
    if short and abs(v) >= 1e6:
        return f"${v/1e6:,.2f}m"
    return f"-${abs(v):,.0f}" if v < 0 else f"${v:,.0f}"


def style(fig, h=380, legend=True):
    fig.update_layout(
        height=h, margin=dict(l=10, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fffaf1",
        font=dict(family="DM Sans, sans-serif", color=INK, size=13), showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#fffaf1", bordercolor=GRID, font=dict(color=INK)),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor="#cdb895", linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor="#cdb895", linecolor=GRID)
    return fig


# ---------- header ----------
st.markdown('<div class="kicker">Coffee Shop Strategy · Business dashboard</div>', unsafe_allow_html=True)
st.markdown("# What 15 runs *taught me*")
st.markdown('<div class="band"></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="lede">I ran the Coffee Shop Inc. simulation 15 times across three levels, from one shop to an '
    "international chain, and treated every run as an experiment. Use the tabs to explore results, the profit "
    "and loss of each run, and what each decision was worth.</p>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Filters")
    levels = st.multiselect("Levels", ["L1", "L2", "L3"], default=["L1", "L2", "L3"])
    st.markdown("---")
    st.markdown(
        '<p class="explore"><b>Explore more</b><br>'
        '<a target="_self" href="https://dewpoint-analytics.github.io/coffee-strategy-dashboard/?ref=streamlit&from=app">☕ Full dashboard</a><br>'
        '<a target="_self" href="https://dewpoint-analytics.github.io/3DCoffeeHub/?ref=streamlit&from=app">🏠 3D Coffee Hub</a><br>'
        '<a target="_self" href="https://dewpoint-analytics.github.io/coffee-strategy-dashboard/report.html?ref=streamlit"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" style="vertical-align:-2px"><g fill="#7a3320"><path fill-rule="evenodd" d="M1 1h5v5H1zM2 2v3h3V2zM10 1h5v5h-5zm1 1v3h3V2zM1 10h5v5H1zm1 1v3h3v-3z"/><rect x="3" y="3" width="1" height="1"/><rect x="12" y="3" width="1" height="1"/><rect x="3" y="12" width="1" height="1"/><rect x="7" y="1" width="2" height="2"/><rect x="7" y="4" width="1" height="3"/><rect x="9" y="7" width="2" height="1"/><rect x="7" y="9" width="2" height="2"/><rect x="10" y="10" width="2" height="2"/><rect x="13" y="9" width="2" height="1"/><rect x="12" y="12" width="3" height="1"/><rect x="10" y="13" width="1" height="2"/><rect x="13" y="14" width="2" height="1"/><rect x="1" y="7" width="3" height="1"/><rect x="5" y="8" width="1" height="1"/></g></svg> Field report</a></p>',
        unsafe_allow_html=True,
    )
    st.markdown('<p class="note">Source: my own runs of Coffee Shop Inc. (Sim Institute / Harvard Business Impact), Oct–Nov 2026. '
                "Figures are from the game's result screens.</p>", unsafe_allow_html=True)

# ---------- KPIs ----------
best = runs.loc[runs.groupby("Level")["Game total ($)"].idxmax()].set_index("Level")
beat = int((runs["Pct"] >= 100).sum())
k = st.columns(4)
k[0].metric("Runs beating target", f"{beat} of {len(runs)}", "93% hit rate", delta_color="off")
k[1].metric("Best · Level 1", money(best.loc["L1", "Game total ($)"]), f"{best.loc['L1','Pct']:.0f}% of target", delta_color="off")
k[2].metric("Best · Level 2", money(best.loc["L2", "Game total ($)"]), f"{best.loc['L2','Pct']:.0f}% of target", delta_color="off")
k[3].metric("Best · Level 3", money(best.loc["L3", "Game total ($)"], True), f"{best.loc['L3','Pct']:.0f}% of target", delta_color="off")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Performance", "🧾 Profit & loss", "🌍 Level 3 growth", "🔬 Decision Lab", "📘 Playbook"])

# ---------- Performance ----------
with tab1:
    sel = runs[runs["Level"].isin(levels)]
    st.markdown("### Five-year profit as a share of target")
    fig = go.Figure()
    for lv in [l for l in ["L1", "L2", "L3"] if l in levels]:
        s = sel[sel["Level"] == lv]
        fig.add_bar(x=s["Short"], y=s["Pct"], name={"L1": "Level 1 · one shop", "L2": "Level 2 · the brand", "L3": "Level 3 · international"}[lv],
                    marker=dict(color=LEVEL_COLORS[lv], cornerradius=4), text=[f"{v:.0f}%" for v in s["Pct"]], textposition="outside",
                    customdata=s[["Strategy (one line)", "Game total ($)"]].values,
                    hovertemplate="<b>%{x}</b><br>%{customdata[0]}<br>Profit $%{customdata[1]:,.0f}<br>%{y:.0f}% of target<extra></extra>")
    fig.add_hline(y=100, line=dict(color=INK, dash="dot", width=1.5), annotation_text="Target", annotation_position="top left")
    fig.update_yaxes(title="% of target", ticksuffix="%", range=[0, max(sel["Pct"].max() * 1.15, 120) if len(sel) else 120])
    fig.update_layout(bargap=.25)
    st.plotly_chart(style(fig, 420), width="stretch")
    st.markdown('<p class="note">Targets: $500,000 at Levels 1 and 2, $5,000,000 at Level 3. The only miss was the low-price Campus run (99% of target).</p>', unsafe_allow_html=True)
    with st.expander("See the table"):
        t = sel[["Short", "Strategy (one line)", "Game total ($)", "Target ($)", "Pct"]].rename(columns={"Short": "Run", "Pct": "% of target"})
        st.dataframe(t, hide_index=True, width="stretch",
                     column_config={"Game total ($)": st.column_config.NumberColumn(format="$%,d"), "Target ($)": st.column_config.NumberColumn(format="$%,d"),
                                    "% of target": st.column_config.NumberColumn(format="%.0f%%")})

# ---------- Profit & loss ----------
with tab2:
    st.markdown("### Inside one shop: Levels 1 and 2")
    c1, c2 = st.columns([1, 2])
    lv = c1.radio("Level", [1, 2], format_func=lambda x: f"Level {x}", horizontal=True)
    opts = runs[runs["Level"] == f"L{lv}"]
    run = c2.selectbox("Run", opts["Run"], format_func=lambda r: f"Run {r} · {opts.set_index('Run').loc[r,'Strategy (one line)']}")
    df = l12[(l12["Level"] == lv) & (l12["Run"] == run)].sort_values("Year")
    m = st.columns(4)
    m[0].metric("Five-year revenue", money(df["Revenue ($)"].sum()))
    m[1].metric("Five-year cost", money(df["Total cost ($)"].sum()))
    m[2].metric("Five-year profit", money(df["Operating profit ($)"].sum()))
    m[3].metric("Margin", f"{df['Operating profit ($)'].sum()/df['Revenue ($)'].sum()*100:.1f}%")
    a, b = st.columns(2)
    with a:
        st.markdown("#### Where each year's revenue went")
        parts = [("COGS ($)", "Coffee & cups", "#c9a06a"), ("Rent ($)", "Rent", INDIGO), ("Salaries ($)", "Salaries", ROSE),
                 ("Training ($)", "Training", SAGE), ("Promotion ($)", "Promotion", OCHRE), ("Admin & depreciation ($)", "Admin & depreciation", "#9a8a7a")]
        fig = go.Figure()
        for col, name, c in parts:
            fig.add_bar(x=df["Year"].map(lambda y: f"Y{y}"), y=df[col], name=name, marker=dict(color=c, line=dict(color="#fffaf1", width=1.5)),
                        hovertemplate=f"{name}: $%{{y:,.0f}}<extra></extra>")
        fig.add_bar(x=df["Year"].map(lambda y: f"Y{y}"), y=df["Operating profit ($)"], name="Operating profit", marker=dict(color=TEAL, line=dict(color="#fffaf1", width=1.5)),
                    hovertemplate="Profit: $%{y:,.0f}<extra></extra>")
        fig.update_layout(barmode="stack", bargap=.3)
        fig.update_yaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(style(fig, 400), width="stretch")
    with b:
        st.markdown("#### Customers and price, year by year")
        fig = go.Figure()
        fig.add_bar(x=df["Year"].map(lambda y: f"Y{y}"), y=df["Drinks/day daytime"], name="Daytime drinks/day", marker=dict(color=OCHRE, cornerradius=3))
        fig.add_bar(x=df["Year"].map(lambda y: f"Y{y}"), y=df["Drinks/day evening"], name="Evening drinks/day", marker=dict(color=ROSE, cornerradius=3))
        fig.update_layout(barmode="stack", bargap=.3)
        fig.update_yaxes(title="Drinks per day")
        st.plotly_chart(style(fig, 400), width="stretch")
    show = df[["Year", "Location", "Roasting", "Coffee", "Competitor price ($)", "My price ($)", "Employee stars", "Customer stars", "Revenue ($)", "Total cost ($)", "Operating profit ($)"]]
    st.dataframe(show, hide_index=True, width="stretch",
                 column_config={c: st.column_config.NumberColumn(format="$%,d") for c in ["Revenue ($)", "Total cost ($)", "Operating profit ($)"]}
                 | {c: st.column_config.NumberColumn(format="$%.2f") for c in ["Competitor price ($)", "My price ($)"]})

# ---------- Level 3 ----------
with tab3:
    st.markdown("### Growing across two markets")
    pick = st.multiselect("Runs", sorted(l3["Run"].unique()), default=[1, 5], format_func=lambda r: f"Run {r}")
    mk = st.radio("Market", ["Both", "Mature", "Emerging"], horizontal=True)
    d3 = l3[l3["Run"].isin(pick)]
    if mk != "Both":
        d3 = d3[d3["Market"] == mk]
    g = d3.groupby(["Run", "Year"], as_index=False)[["Operating profit ($)", "Own stores (end of year)"]].sum()
    a, b = st.columns(2)
    with a:
        st.markdown("#### Operating profit by year")
        fig = go.Figure()
        for i, r in enumerate(pick):
            s = g[g["Run"] == r]
            fig.add_scatter(x=s["Year"].map(lambda y: f"Y{y}"), y=s["Operating profit ($)"], mode="lines+markers", name=f"Run {r}",
                            line=dict(color=RUN_COLORS[(r - 1) % 5], width=2.5), marker=dict(size=9, line=dict(color="#fffaf1", width=2)),
                            hovertemplate=f"Run {r} · %{{x}}: $%{{y:,.0f}}<extra></extra>")
        fig.update_yaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(style(fig, 380), width="stretch")
    with b:
        st.markdown("#### Own stores at year end")
        fig = go.Figure()
        for r in pick:
            s = g[g["Run"] == r]
            fig.add_bar(x=s["Year"].map(lambda y: f"Y{y}"), y=s["Own stores (end of year)"], name=f"Run {r}", marker=dict(color=RUN_COLORS[(r - 1) % 5], cornerradius=3))
        fig.update_layout(bargap=.3)
        st.plotly_chart(style(fig, 380), width="stretch")
    tot = runs[runs["Level"] == "L3"][["Run", "Strategy (one line)", "Game total ($)"]]
    st.dataframe(tot, hide_index=True, width="stretch", column_config={"Game total ($)": st.column_config.NumberColumn("Five-year profit", format="$%,d")})
    st.markdown('<p class="note">Run 5, with a third Emerging store in Year 1, earned the most: $12,501,031. Opening Emerging stores faster added $952,776 (E13).</p>', unsafe_allow_html=True)

# ---------- Decision Lab ----------
with tab4:
    st.markdown("### What each decision was worth")
    c1, c2 = st.columns(2)
    pillars = c1.multiselect("Pillar", sorted(exp["Pillar"].unique()), default=sorted(exp["Pillar"].unique()))
    clean = c2.toggle("Clean one-variable tests only", value=False)
    e = exp[exp["Pillar"].isin(pillars)]
    if clean:
        e = e[e["Evidence quality"].str.startswith("Clean")]
    e = e.sort_values("Profit effect ($)")
    fig = go.Figure(go.Bar(
        y=e["ID"] + " · " + e["What changed"], x=e["Profit effect ($)"], orientation="h",
        marker=dict(color=[GAIN if v >= 0 else LOSS for v in e["Profit effect ($)"]], cornerradius=4),
        text=[money(v) for v in e["Profit effect ($)"]], textposition="outside",
        customdata=e[["Runs compared", "Evidence quality", "Conclusion"]].values,
        hovertemplate="<b>%{y}</b><br>%{customdata[0]} · %{customdata[1]}<br>%{customdata[2]}<extra></extra>"))
    fig.add_vline(x=0, line=dict(color=INK, width=1))
    lo, hi = min(0, e["Profit effect ($)"].min()), max(0, e["Profit effect ($)"].max())
    pad = (hi - lo) * .22 or 1
    fig.update_xaxes(range=[lo - pad, hi + pad])
    fig.update_traces(cliponaxis=False)
    fig.update_xaxes(tickprefix="$", tickformat="~s", title="Five-year profit effect")
    st.plotly_chart(style(fig, max(320, 46 * len(e) + 80), legend=False), width="stretch")
    st.markdown('<p class="note">Teal = the change added profit, terracotta = it cost profit. "Descriptive" comparisons differed in more than one setting, so treat them as indicative.</p>', unsafe_allow_html=True)
    for _, r in e.sort_values("ID", key=lambda s: s.str[1:].astype(int)).iterrows():
        with st.expander(f"{r['ID']} · {r['What changed']}  ({money(r['Profit effect ($)'])})"):
            st.markdown(f"**Question:** {r['Question']}  \n**Runs compared:** {r['Runs compared']}  \n**Evidence:** {r['Evidence quality']}  \n\n{r['Conclusion']}  \n\n*{r['Strategic reading']}*")

# ---------- Playbook ----------
with tab5:
    st.markdown("### Seven decision rules")
    cols = st.columns(2)
    for i, (_, r) in enumerate(rules.iterrows()):
        with cols[i % 2]:
            st.markdown(f'<div class="card"><span class="note">{r["Pillar"]} · {r["Question"]}</span><br><b>{r["What changed"]}</b><br>'
                        f'{r["Conclusion"]}<br><span class="note">Evidence: {r["Runs compared"]}</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="note">The game is a simplification. Read these as decision principles, not forecasts.</p>', unsafe_allow_html=True)

st.markdown('<div class="band"></div>', unsafe_allow_html=True)
st.markdown('<p class="note">© 2026 Shabnam Mohammed Sameer (DewPoint Analytics). All rights reserved. '
            "Built with Python, Streamlit and Plotly.</p>", unsafe_allow_html=True)
