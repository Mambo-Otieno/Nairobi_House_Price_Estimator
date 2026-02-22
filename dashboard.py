"""
Nairobi Property Market Dashboard
Business intelligence dashboard built from clean_feature_listings.csv
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nairobi Property Market",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Design tokens
# ─────────────────────────────────────────────────────────────────────────────
TEAL      = "#00B4A6"
TEAL_DARK = "#007A70"
AMBER     = "#F5A623"
CORAL     = "#E8604C"
NAVY      = "#0D1B2A"
SLATE     = "#1C2B3A"
SLATE2    = "#243344"
BORDER    = "#2E4057"
TEXT      = "#E8F0F7"
MUTED     = "#7A96AD"
GREEN     = "#3DDC84"
CHART_BG  = "rgba(0,0,0,0)"
PALETTE   = [TEAL, AMBER, CORAL, GREEN, "#A78BFA", "#FB923C", "#34D399", "#F472B6"]

PLOTLY_LAYOUT = dict(
    paper_bgcolor=CHART_BG,
    plot_bgcolor=CHART_BG,
    font=dict(family="Sora, sans-serif", color=TEXT, size=12),
    margin=dict(l=0, r=0, t=40, b=0),
)

# Default legend style — apply via update_layout(legend=LEGEND_STYLE) per figure
LEGEND_STYLE = dict(bgcolor="rgba(13,27,42,0.6)", bordercolor=BORDER, borderwidth=1)
# Default axis style
AXIS_STYLE = dict(gridcolor=BORDER, linecolor=BORDER, tickcolor=BORDER, zeroline=False)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

:root {{
    --navy:{NAVY}; --slate:{SLATE}; --slate2:{SLATE2}; --border:{BORDER};
    --teal:{TEAL}; --amber:{AMBER}; --coral:{CORAL}; --text:{TEXT}; --muted:{MUTED};
}}
html, body, [data-testid="stAppViewContainer"] {{
    background-color: var(--navy) !important;
    color: var(--text);
    font-family: 'Sora', sans-serif;
}}
[data-testid="stHeader"] {{ background: transparent !important; }}
#MainMenu, footer {{ visibility: hidden; }}

[data-testid="stSidebar"] {{
    background: var(--slate) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] * {{ color: var(--text) !important; }}
[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: var(--slate2) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] label {{
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
}}
[data-testid="block-container"] {{
    padding: 1.5rem 2.5rem !important;
    max-width: 1400px !important;
}}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}}
.kpi-card {{
    background: var(--slate);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, {TEAL});
}}
.kpi-label {{
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}}
.kpi-value {{
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    color: var(--text);
    line-height: 1.1;
}}
.kpi-sub {{ font-size: 0.75rem; color: var(--muted); margin-top: 0.3rem; }}

.section-header {{
    display: flex;
    align-items: baseline;
    gap: 0.8rem;
    margin: 1.5rem 0 0.8rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.6rem;
}}
.section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: var(--text);
}}
.section-sub {{ font-size: 0.78rem; color: var(--muted); }}

.insight {{
    background: rgba(0, 180, 166, 0.08);
    border-left: 3px solid {TEAL};
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    margin: 0.6rem 0;
    font-size: 0.84rem;
    color: var(--text);
    line-height: 1.5;
}}
.insight strong {{ color: {TEAL}; }}

.note-box {{
    background: rgba(245, 166, 35, 0.07);
    border-left: 3px solid {AMBER};
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    font-size: 0.76rem;
    color: var(--muted);
    margin-top: 0.6rem;
}}

[data-testid="stRadio"] > div {{ flex-direction: column; gap: 4px; }}
[data-testid="stRadio"] label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    font-size: 0.85rem !important;
    cursor: pointer !important;
    color: var(--muted) !important;
    transition: all 0.15s !important;
}}
[data-testid="stRadio"] label:hover {{
    background: var(--slate2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}}
[data-testid="stRadio"] > label {{
    font-size: 0.72rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 4px !important;
}}
[data-testid="stSlider"] .rc-slider-rail {{ background: var(--border) !important; }}
[data-testid="stSlider"] .rc-slider-track {{ background: {TEAL} !important; }}
[data-testid="stSlider"] .rc-slider-handle {{
    border-color: {TEAL} !important;
    background: {TEAL} !important;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("clean_feature_listings.csv")
    df["amenity_tier"] = pd.cut(
        df["amenity_score"],
        bins=[-1, 0, 2, 4, 100],
        labels=["None (0)", "Basic (1–2)", "Good (3–4)", "Premium (5+)"],
    )
    # Distance bands for proximity page
    df["dist_band"] = pd.cut(
        df["distance_to_cbd_km"],
        bins=[0, 3, 6, 10, 15, 60],
        labels=["0–3 km", "3–6 km", "6–10 km", "10–15 km", "15 km+"],
        include_lowest=True,
    )
    return df

df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0 1.4rem;">
        <div style="font-size:2rem">🏙️</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.1rem;color:{TEXT};margin-top:0.3rem">
            Nairobi Property
        </div>
        <div style="font-size:0.72rem;letter-spacing:2px;color:{MUTED};text-transform:uppercase">
            Market Dashboard
        </div>
    </div>
    <hr style="border-color:{BORDER}; margin:0 0 1.2rem"/>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "📍 Median Price by Location",
            "📈 Price Trend by Proximity",
            "📐 Price per m² Comparison",
            "✨ Amenity Impact",
        ],
    )

    st.markdown(f"<hr style='border-color:{BORDER};margin:1.2rem 0'/>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.72rem;letter-spacing:1.5px;text-transform:uppercase;color:{MUTED};margin-bottom:0.5rem'>Filters</div>", unsafe_allow_html=True)

    all_types   = ["All"] + sorted(df["Property Type"].unique().tolist())
    prop_filter = st.selectbox("Property Type", all_types)

    loc_counts  = df["Location"].value_counts()
    major_locs  = ["All"] + sorted(loc_counts[loc_counts >= 4].index.tolist())
    loc_filter  = st.selectbox("Location", major_locs)

    bed_range   = st.slider("Bedrooms", 1, 8, (1, 8))

    mask = (df["Bedrooms"] >= bed_range[0]) & (df["Bedrooms"] <= bed_range[1])
    if prop_filter != "All":
        mask &= df["Property Type"] == prop_filter
    if loc_filter != "All":
        mask &= df["Location"] == loc_filter
    dff = df[mask].copy()

    st.markdown(f"""
    <div style="margin-top:1rem;padding:0.7rem 0.9rem;background:{SLATE2};border-radius:8px;
                border:1px solid {BORDER};font-size:0.8rem;color:{MUTED};">
        <span style="color:{TEAL};font-weight:600">{len(dff):,}</span> listings match filters<br>
        <span style="color:{MUTED};font-size:0.72rem">of {len(df):,} total</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:auto;padding-top:2rem;font-size:0.68rem;color:{MUTED};text-align:center">
        Source: Nairobi Listings Dataset<br>
        462 cleaned records · 2026
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────
def fmt_kes(val):
    return f"KES {val/1_000_000:.1f}M" if val >= 1_000_000 else f"KES {val:,.0f}"


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "Overview":
    st.markdown(f"""
    <div style="margin-bottom:1.4rem;">
        <div style="font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;color:{MUTED};margin-bottom:0.3rem">
            Nairobi Real Estate · 2026
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:2rem;color:{TEXT}">
            Property Market Overview
        </div>
        <div style="color:{MUTED};font-size:0.88rem;margin-top:0.3rem">
            {len(dff):,} listings across {dff['Location'].nunique()} neighbourhoods
        </div>
    </div>
    """, unsafe_allow_html=True)

    median_price = dff["Price (KES)"].median()
    median_ppsf  = dff["price_per_sqft"].median()
    median_size  = dff["Size (m2)"].median()
    luxury_pct   = dff["is_luxury"].mean() * 100

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:{TEAL}">
            <div class="kpi-label">Median Price</div>
            <div class="kpi-value">{median_price/1e6:.1f}M</div>
            <div class="kpi-sub">KES · all property types</div>
        </div>
        <div class="kpi-card" style="--accent:{AMBER}">
            <div class="kpi-label">Median Price / m²</div>
            <div class="kpi-value">{median_ppsf:,.0f}</div>
            <div class="kpi-sub">KES per square metre</div>
        </div>
        <div class="kpi-card" style="--accent:{CORAL}">
            <div class="kpi-label">Median Size</div>
            <div class="kpi-value">{median_size:.0f} m²</div>
            <div class="kpi-sub">built area</div>
        </div>
        <div class="kpi-card" style="--accent:{GREEN}">
            <div class="kpi-label">Luxury Listings</div>
            <div class="kpi-value">{luxury_pct:.1f}%</div>
            <div class="kpi-sub">premium amenity score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="section-header"><span class="section-title">Price Distribution</span><span class="section-sub">log scale</span></div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=np.log10(dff["Price (KES)"].dropna()),
            nbinsx=40, marker_color=TEAL, marker_line_width=0, opacity=0.85,
        ))
        fig.add_vline(
            x=np.log10(median_price), line_color=AMBER, line_dash="dash", line_width=2,
            annotation_text=f"Median {fmt_kes(median_price)}",
            annotation_font_color=AMBER, annotation_position="top right",
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=False,
                          xaxis_title="Price (log₁₀ KES)", yaxis_title="Count")
        fig.update_xaxes(**AXIS_STYLE)
        fig.update_yaxes(**AXIS_STYLE)
        fig.update_xaxes(tickvals=[6,7,7.5,8,8.5], ticktext=["1M","10M","30M","100M","300M"])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<div class="section-header"><span class="section-title">Listings by Property Type</span></div>', unsafe_allow_html=True)
        pt = dff["Property Type"].value_counts().reset_index()
        pt.columns = ["type", "count"]
        fig2 = go.Figure(go.Bar(
            y=pt["type"], x=pt["count"], orientation="h",
            marker_color=PALETTE[:len(pt)],
            text=pt["count"], textposition="auto", textfont=dict(color=TEXT, size=11),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=False)
        fig2.update_yaxes(autorange="reversed", **AXIS_STYLE)
        fig2.update_xaxes(**AXIS_STYLE)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header"><span class="section-title">Price vs Size</span><span class="section-sub">by property category</span></div>', unsafe_allow_html=True)
        sdf = dff.dropna(subset=["Size (m2)", "Price (KES)"])
        fig3 = go.Figure()
        for i, cat in enumerate(sdf["property_category"].unique()):
            s = sdf[sdf["property_category"] == cat]
            fig3.add_trace(go.Scatter(
                x=s["Size (m2)"], y=s["Price (KES)"] / 1e6, mode="markers", name=cat,
                marker=dict(color=PALETTE[i], size=6, opacity=0.65, line=dict(width=0)),
            ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=270,
                           xaxis_title="Size (m²)", yaxis_title="Price (M KES)")
        fig3.update_xaxes(**AXIS_STYLE)
        fig3.update_yaxes(**AXIS_STYLE)
        fig3.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.01,
                                       xanchor="left", x=0, bgcolor="rgba(0,0,0,0)", borderwidth=0))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with col4:
        st.markdown('<div class="section-header"><span class="section-title">Median Price by Bedrooms</span></div>', unsafe_allow_html=True)
        bed_df = dff[dff["Bedrooms"] <= 6].groupby("Bedrooms")["Price (KES)"].median().reset_index()
        fig4 = go.Figure(go.Bar(
            x=bed_df["Bedrooms"].astype(str) + " bed",
            y=bed_df["Price (KES)"] / 1e6,
            marker_color=PALETTE,
            text=(bed_df["Price (KES)"] / 1e6).map(lambda v: f"{v:.1f}M"),
            textposition="outside", textfont=dict(color=TEXT, size=10),
        ))
        fig4.update_layout(**PLOTLY_LAYOUT, height=270, showlegend=False)
        fig4.update_xaxes(**AXIS_STYLE)
        fig4.update_yaxes(title_text="Median Price (M KES)", **AXIS_STYLE)#, zeroline=False)
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header"><span class="section-title">Key Market Insights</span></div>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"""<div class="insight">
            The market median of <strong>{fmt_kes(df['Price (KES)'].median())}</strong> is pulled
            upward by a small number of luxury listings — the mean is
            <strong>{fmt_kes(df['Price (KES)'].mean())}</strong>, reflecting high skew.
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""<div class="insight">
            <strong>Apartments</strong> (40% of listings) dominate supply but have the lowest
            median price at <strong>~KES 9.9M</strong>. Houses and Villas command 3–6× more.
        </div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"""<div class="insight">
            5-bedroom properties show a <strong>7× price jump</strong> over 1-bedroom units,
            suggesting large-format homes sit predominantly in premium areas like Runda and Karen.
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: MEDIAN PRICE BY LOCATION  (rebuilt)
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📍 Median Price by Location":

    st.markdown(f"""
    <div style="margin-bottom:1.2rem">
        <div style="font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;color:{MUTED};margin-bottom:0.3rem">
            Nairobi Real Estate · 2026
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:1.9rem;color:{TEXT}">
            Median Price by Location
        </div>
        <div style="color:{MUTED};font-size:0.88rem">
            Neighbourhood benchmarks — locations with ≥4 listings
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Build location stats ──────────────────────────────────────────────────
    loc_min = 4
    lc      = dff["Location"].value_counts()
    bl      = lc[lc >= loc_min].index
    loc_df  = (
        dff[dff["Location"].isin(bl)]
        .groupby("Location")
        .agg(
            median_price = ("Price (KES)",       "median"),
            mean_price   = ("Price (KES)",       "mean"),
            count        = ("Price (KES)",       "count"),
            median_ppsf  = ("price_per_sqft",    "median"),
            dist_km      = ("distance_to_cbd_km","mean"),
        )
        .reset_index()
        .sort_values("median_price", ascending=False)
        .reset_index(drop=True)
    )

    if loc_df.empty:
        st.warning("Not enough data with current filters — broaden your selection.")
        st.stop()

    # ── KPIs ──────────────────────────────────────────────────────────────────
    top_loc   = loc_df.iloc[0]
    bot_loc   = loc_df.iloc[-1]
    spread    = top_loc["median_price"] / bot_loc["median_price"]
    overall_m = dff["Price (KES)"].median()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:{TEAL}">
            <div class="kpi-label">Most Expensive</div>
            <div class="kpi-value">{top_loc['Location']}</div>
            <div class="kpi-sub">{fmt_kes(top_loc['median_price'])} median</div>
        </div>
        <div class="kpi-card" style="--accent:{AMBER}">
            <div class="kpi-label">Most Affordable</div>
            <div class="kpi-value">{bot_loc['Location']}</div>
            <div class="kpi-sub">{fmt_kes(bot_loc['median_price'])} median</div>
        </div>
        <div class="kpi-card" style="--accent:{CORAL}">
            <div class="kpi-label">Price Spread</div>
            <div class="kpi-value">{spread:.1f}×</div>
            <div class="kpi-sub">top vs bottom neighbourhood</div>
        </div>
        <div class="kpi-card" style="--accent:{GREEN}">
            <div class="kpi-label">Neighbourhoods Tracked</div>
            <div class="kpi-value">{len(loc_df)}</div>
            <div class="kpi-sub">with ≥{loc_min} listings each</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: ranked bar + summary table ────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Ranked Median Price</span><span class="section-sub">teal = top third · amber = middle · grey = lower third</span></div>', unsafe_allow_html=True)

    col_bar, col_tbl = st.columns([1.55, 1])

    with col_bar:
        n       = len(loc_df)
        t1      = int(n * 0.33)
        t2      = int(n * 0.66)
        bar_col = [
            TEAL  if i < t1 else
            AMBER if i < t2 else
            MUTED
            for i in range(n)
        ]
        # ascending for horizontal bar (bottom = highest)
        ld_asc = loc_df.sort_values("median_price", ascending=True)
        bar_col_asc = bar_col[::-1]

        fig_bar = go.Figure(go.Bar(
            y  = ld_asc["Location"],
            x  = ld_asc["median_price"] / 1e6,
            orientation = "h",
            marker_color = bar_col_asc,
            marker_line_width = 0,
            text = (ld_asc["median_price"] / 1e6).map(lambda v: f"{v:.1f}M"),
            textposition = "outside",
            textfont = dict(color=TEXT, size=10),
            customdata = ld_asc[["count", "dist_km", "median_ppsf"]].values,
            hovertemplate = (
                "<b>%{y}</b><br>"
                "Median: KES %{x:.1f}M<br>"
                "Listings: %{customdata[0]:.0f}<br>"
                "Dist CBD: %{customdata[1]:.1f} km<br>"
                "KES/m²: %{customdata[2]:,.0f}<extra></extra>"
            ),
        ))
        # reference line — overall median
        fig_bar.add_vline(
            x=overall_m / 1e6, line_color=CORAL, line_dash="dash", line_width=1.5,
            annotation_text=f"Overall median {fmt_kes(overall_m)}",
            annotation_font_color=CORAL, annotation_position="top right",
        )
        fig_bar.update_layout(
            **PLOTLY_LAYOUT,
            height=max(420, n * 30),
            xaxis_title="Median Price (M KES)",
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_tbl:
        st.markdown(f"<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        tbl = loc_df[["Location","median_price","count","median_ppsf","dist_km"]].copy()
        tbl.columns = ["Location","Median Price","Listings","KES / m²","Dist to CBD"]
        tbl["Median Price"] = tbl["Median Price"].map(lambda v: f"KES {v/1e6:.1f}M")
        tbl["KES / m²"]     = tbl["KES / m²"].map(lambda v: f"{v:,.0f}")
        tbl["Dist to CBD"]  = tbl["Dist to CBD"].map(lambda v: f"{v:.1f} km")
        st.dataframe(tbl.reset_index(drop=True),
                     use_container_width=True, hide_index=True,
                     height=min(600, n * 35 + 38))

        top3 = loc_df.head(3)["Location"].tolist()
        top3_avg = loc_df.head(3)["median_price"].mean()
        bot3_avg = loc_df.tail(3)["median_price"].mean()
        st.markdown(f"""
        <div class="insight" style="margin-top:1rem">
            <strong>{", ".join(top3)}</strong> average <strong>{fmt_kes(top3_avg)}</strong>
            — {top3_avg/bot3_avg:.1f}× higher than the three most affordable
            neighbourhoods in this dataset.
        </div>
        """, unsafe_allow_html=True)

    # ── Row 2: box plot spread ────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Price Spread per Neighbourhood</span><span class="section-sub">interquartile range · dot = mean · ordered by median</span></div>', unsafe_allow_html=True)

    order = loc_df["Location"].tolist()  # high → low median
    box_df = dff[dff["Location"].isin(order)].copy()
    box_df["Location"] = pd.Categorical(box_df["Location"], categories=order, ordered=True)

    fig_box = go.Figure()
    for i, loc in enumerate(order):
        sub = box_df[box_df["Location"] == loc]["Price (KES)"] / 1e6
        fig_box.add_trace(go.Box(
            y    = sub,
            name = loc,
            marker_color = PALETTE[i % len(PALETTE)],
            line_color   = PALETTE[i % len(PALETTE)],
            fillcolor    = f"rgba({int(PALETTE[i%len(PALETTE)][1:3],16)},"
                           f"{int(PALETTE[i%len(PALETTE)][3:5],16)},"
                           f"{int(PALETTE[i%len(PALETTE)][5:7],16)},0.15)",
            boxmean=True,
            showlegend=False,
        ))
    fig_box.update_layout(
        **PLOTLY_LAYOUT,
        height=340,
        yaxis_title="Price (M KES)",
        xaxis_tickangle=-35,
    )
    st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    # ── Row 3: median price vs KES/m² bubble ─────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Median Price vs KES/m²</span><span class="section-sub">bubble size = listing count</span></div>', unsafe_allow_html=True)

    fig_bub = go.Figure(go.Scatter(
        x    = loc_df["median_ppsf"],
        y    = loc_df["median_price"] / 1e6,
        mode = "markers+text",
        text = loc_df["Location"],
        textposition = "top center",
        textfont = dict(size=9, color=MUTED),
        marker = dict(
            size  = np.sqrt(loc_df["count"]) * 5,
            color = loc_df["median_price"],
            colorscale=[[0, NAVY], [0.3, TEAL_DARK], [0.7, TEAL], [1, AMBER]],
            opacity=0.85,
            line=dict(color=BORDER, width=1),
            colorbar=dict(title="Median KES", thickness=12,
                          tickfont=dict(color=TEXT), title_font_color=TEXT),
        ),
        customdata=loc_df[["count","dist_km"]].values,
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Median: KES %{y:.1f}M<br>"
            "KES/m²: %{x:,.0f}<br>"
            "Listings: %{customdata[0]:.0f}<br>"
            "Dist CBD: %{customdata[1]:.1f} km<extra></extra>"
        ),
    ))
    fig_bub.update_layout(
        **PLOTLY_LAYOUT,
        height=370,
        xaxis_title="Median KES / m²",
        yaxis_title="Median Price (M KES)",
        showlegend=False,
    )
    st.plotly_chart(fig_bub, use_container_width=True, config={"displayModeBar": False})

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Location Insights</span></div>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    # Highest ppsf location
    hi_ppsf_row = loc_df.loc[loc_df["median_ppsf"].idxmax()]
    # Biggest mean/median gap (most skewed)
    loc_df["gap"] = loc_df["mean_price"] - loc_df["median_price"]
    skewed_row   = loc_df.loc[loc_df["gap"].idxmax()]
    with ic1:
        st.markdown(f"""<div class="insight">
            <strong>{hi_ppsf_row['Location']}</strong> commands the highest density value at
            <strong>KES {hi_ppsf_row['median_ppsf']:,.0f}/m²</strong> —
            {hi_ppsf_row['dist_km']:.1f} km from the CBD, proving that
            proximity alone doesn't determine value.
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""<div class="insight">
            <strong>{skewed_row['Location']}</strong> has the widest mean–median gap
            (<strong>{fmt_kes(skewed_row['gap'])}</strong>), indicating a
            few ultra-premium listings that skew the average well above typical prices.
        </div>""", unsafe_allow_html=True)
    with ic3:
        prem_locs = loc_df[loc_df["median_price"] >= 5e7]
        st.markdown(f"""<div class="insight">
            <strong>{len(prem_locs)} out of {len(loc_df)} neighbourhoods</strong>
            exceed the KES 50M median threshold — the premium segment is concentrated
            but commands prices up to <strong>{spread:.1f}×</strong> above the
            most affordable areas.
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PRICE TREND BY PROXIMITY TO CBD  (replaces Monthly Trend)
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📈 Price Trend by Proximity":

    st.markdown(f"""
    <div style="margin-bottom:1.2rem">
        <div style="font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;color:{MUTED};margin-bottom:0.3rem">
            Nairobi Real Estate · 2026
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:1.9rem;color:{TEXT}">
            Price Trend by Proximity to CBD
        </div>
        <div style="color:{MUTED};font-size:0.88rem">
            How distance from Nairobi city centre shapes listing prices and value density
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Distance band stats ───────────────────────────────────────────────────
    bands_order = ["0–3 km", "3–6 km", "6–10 km", "10–15 km", "15 km+"]
    band_df = (
        dff.groupby("dist_band", observed=True)
        .agg(
            median_price = ("Price (KES)",       "median"),
            mean_price   = ("Price (KES)",       "mean"),
            count        = ("Price (KES)",       "count"),
            median_ppsf  = ("price_per_sqft",    "median"),
            mean_ppsf    = ("price_per_sqft",    "mean"),
            median_size  = ("Size (m2)",         "median"),
            median_beds  = ("Bedrooms",          "median"),
        )
        .reindex(bands_order)
        .reset_index()
        .dropna(subset=["median_price"])
    )

    # ── KPIs ──────────────────────────────────────────────────────────────────
    # Find the band with the peak absolute price (not necessarily innermost)
    peak_band   = band_df.loc[band_df["median_price"].idxmax()]
    inner_band  = band_df.iloc[0]  # 0–3 km
    outer_band  = band_df.dropna().iloc[-1]
    ppsf_peak   = band_df.loc[band_df["median_ppsf"].idxmax()]

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:{TEAL}">
            <div class="kpi-label">Inner City Median (0–3 km)</div>
            <div class="kpi-value">{inner_band['median_price']/1e6:.1f}M</div>
            <div class="kpi-sub">KES · {inner_band['count']:.0f} listings</div>
        </div>
        <div class="kpi-card" style="--accent:{AMBER}">
            <div class="kpi-label">Peak Price Zone</div>
            <div class="kpi-value">{peak_band['dist_band']}</div>
            <div class="kpi-sub">{fmt_kes(peak_band['median_price'])} median</div>
        </div>
        <div class="kpi-card" style="--accent:{CORAL}">
            <div class="kpi-label">Highest KES/m² Zone</div>
            <div class="kpi-value">{ppsf_peak['dist_band']}</div>
            <div class="kpi-sub">KES {ppsf_peak['median_ppsf']:,.0f}/m²</div>
        </div>
        <div class="kpi-card" style="--accent:{GREEN}">
            <div class="kpi-label">Outer Rim Median (15 km+)</div>
            <div class="kpi-value">{outer_band['median_price']/1e6:.1f}M</div>
            <div class="kpi-sub">KES · {outer_band['count']:.0f} listings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: price trend line + bar ─────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Median & Mean Price by Distance Band</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1])

    with col1:
        fig_line = go.Figure()
        # Shaded area under median
        fig_line.add_trace(go.Scatter(
            x=band_df["dist_band"], y=band_df["median_price"] / 1e6,
            mode="lines+markers", name="Median Price",
            line=dict(color=TEAL, width=3),
            marker=dict(size=10, color=TEAL, symbol="circle",
                        line=dict(color=NAVY, width=2)),
            fill="tozeroy", fillcolor="rgba(0,180,166,0.09)",
        ))
        fig_line.add_trace(go.Scatter(
            x=band_df["dist_band"], y=band_df["mean_price"] / 1e6,
            mode="lines+markers", name="Mean Price",
            line=dict(color=AMBER, width=2, dash="dot"),
            marker=dict(size=7, color=AMBER),
        ))
        # Annotate each point
        for _, row in band_df.iterrows():
            fig_line.add_annotation(
                x=row["dist_band"], y=row["median_price"] / 1e6,
                text=f"{row['median_price']/1e6:.1f}M",
                showarrow=False, yshift=14,
                font=dict(size=9, color=TEAL),
            )
        fig_line.update_layout(
            **PLOTLY_LAYOUT,
            height=310,
            yaxis_title="Price (M KES)",
            xaxis_title="Distance from CBD",
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="left", x=0, bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Listing count per band
        fig_cnt = go.Figure(go.Bar(
            x=band_df["dist_band"],
            y=band_df["count"],
            marker_color=PALETTE[:len(band_df)],
            marker_line_width=0,
            text=band_df["count"].astype(int),
            textposition="outside",
            textfont=dict(color=TEXT, size=11),
        ))
        fig_cnt.update_layout(
            **PLOTLY_LAYOUT,
            height=310,
            yaxis_title="Listing Count",
            xaxis_title="Distance Band",
            showlegend=False,
        )
        st.plotly_chart(fig_cnt, use_container_width=True, config={"displayModeBar": False})

    # ── Row 2: KES/m² trend + median size ────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Value Density & Property Size by Distance</span></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        fig_ppsf = go.Figure()
        fig_ppsf.add_trace(go.Bar(
            x=band_df["dist_band"],
            y=band_df["median_ppsf"],
            name="Median KES/m²",
            marker_color=CORAL, marker_line_width=0,
            text=band_df["median_ppsf"].map(lambda v: f"{v:,.0f}"),
            textposition="outside", textfont=dict(color=TEXT, size=10),
        ))
        fig_ppsf.add_trace(go.Scatter(
            x=band_df["dist_band"],
            y=band_df["mean_ppsf"],
            name="Mean KES/m²",
            mode="lines+markers",
            line=dict(color=AMBER, width=2, dash="dot"),
            marker=dict(size=7, color=AMBER),
        ))
        fig_ppsf.update_layout(
            **PLOTLY_LAYOUT,
            height=280,
            yaxis_title="KES / m²",
            barmode="overlay",
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
        st.plotly_chart(fig_ppsf, use_container_width=True, config={"displayModeBar": False})

    with col4:
        fig_size = go.Figure()
        fig_size.add_trace(go.Scatter(
            x=band_df["dist_band"],
            y=band_df["median_size"],
            mode="lines+markers",
            line=dict(color=GREEN, width=3),
            marker=dict(size=10, color=GREEN, symbol="diamond",
                        line=dict(color=NAVY, width=2)),
            fill="tozeroy", fillcolor="rgba(61,220,132,0.08)",
            name="Median Size (m²)",
        ))
        for _, row in band_df.iterrows():
            fig_size.add_annotation(
                x=row["dist_band"], y=row["median_size"],
                text=f"{row['median_size']:.0f} m²",
                showarrow=False, yshift=14,
                font=dict(size=9, color=GREEN),
            )
        fig_size.update_layout(
            **PLOTLY_LAYOUT,
            height=280,
            yaxis_title="Median Size (m²)",
            xaxis_title="Distance from CBD",
            showlegend=False,
        )
        st.plotly_chart(fig_size, use_container_width=True, config={"displayModeBar": False})

    # ── Row 3: property category mix per band ─────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Property Category Mix by Distance Band</span></div>', unsafe_allow_html=True)

    cat_band = (
        dff.groupby(["dist_band", "property_category"], observed=True)
        .size()
        .reset_index(name="count")
    )
    cat_band["dist_band"] = pd.Categorical(cat_band["dist_band"],
                                            categories=bands_order, ordered=True)
    cat_band = cat_band.sort_values("dist_band")

    fig_stack = go.Figure()
    for i, cat in enumerate(cat_band["property_category"].unique()):
        sub = cat_band[cat_band["property_category"] == cat]
        fig_stack.add_trace(go.Bar(
            x=sub["dist_band"].astype(str),
            y=sub["count"],
            name=cat,
            marker_color=PALETTE[i % len(PALETTE)],
            marker_line_width=0,
        ))
    fig_stack.update_layout(
        **PLOTLY_LAYOUT,
        height=270,
        barmode="stack",
        yaxis_title="Listings",
        xaxis_title="Distance from CBD",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
    )
    st.plotly_chart(fig_stack, use_container_width=True, config={"displayModeBar": False})

    # ── Row 4: scatter — distance vs price, coloured by bedrooms ─────────────
    st.markdown('<div class="section-header"><span class="section-title">Individual Listings: Distance vs Price</span><span class="section-sub">colour = bedrooms</span></div>', unsafe_allow_html=True)

    sc = dff.dropna(subset=["distance_to_cbd_km", "Price (KES)"])
    sc = sc[sc["Price (KES)"] < sc["Price (KES)"].quantile(0.97)]  # clip outliers
    fig_sc = go.Figure(go.Scatter(
        x=sc["distance_to_cbd_km"],
        y=sc["Price (KES)"] / 1e6,
        mode="markers",
        marker=dict(
            color=sc["Bedrooms"],
            colorscale=[[0, TEAL_DARK], [0.25, TEAL], [0.5, AMBER], [0.75, CORAL], [1, "#A78BFA"]],
            size=6, opacity=0.6, line=dict(width=0),
            colorbar=dict(title="Beds", thickness=12,
                          tickfont=dict(color=TEXT), title_font_color=TEXT),
        ),
        text=sc["Location"],
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Dist CBD: %{x:.1f} km<br>"
            "Price: KES %{y:.1f}M<extra></extra>"
        ),
    ))
    # Trend line via rolling average
    sc_sorted = sc.sort_values("distance_to_cbd_km")
    roll_x = sc_sorted["distance_to_cbd_km"].values
    roll_y = sc_sorted["Price (KES)"].rolling(30, min_periods=5, center=True).median().values / 1e6
    fig_sc.add_trace(go.Scatter(
        x=roll_x, y=roll_y,
        mode="lines", name="Rolling median",
        line=dict(color=CORAL, width=2.5, dash="dash"),
        showlegend=True,
    ))
    fig_sc.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        xaxis_title="Distance from CBD (km)",
        yaxis_title="Price (M KES)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
    )
    st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-title">Proximity Insights</span></div>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)

    mid_peak = band_df.loc[band_df["median_price"].idxmax(), "dist_band"]
    inner_m  = band_df.iloc[0]["median_price"] / 1e6
    peak_m   = peak_band["median_price"] / 1e6

    with ic1:
        st.markdown(f"""<div class="insight">
            The <strong>10–15 km band</strong> (Karen, Roysambu, Langata) commands
            the <strong>highest median price</strong> at KES {band_df.loc[band_df['median_price'].idxmax(),'median_price']/1e6:.1f}M —
            outperforming inner-city areas where apartments dominate supply.
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""<div class="insight">
            <strong>KES/m² stays relatively flat</strong> from 0–10 km (100K–108K range),
            then drops in the outer ring — meaning inner-city buyers pay <em>similar density value</em>
            but for much smaller properties.
        </div>""", unsafe_allow_html=True)
    with ic3:
        outer_size = band_df.dropna().iloc[-1]["median_size"]
        inner_size = band_df.iloc[0]["median_size"]
        st.markdown(f"""<div class="insight">
            Properties get <strong>larger as you move outward</strong> — median size grows from
            <strong>{inner_size:.0f} m²</strong> near the CBD to
            <strong>{outer_size:.0f} m²</strong> beyond 15 km —
            reflecting the shift from apartments to houses and land parcels.
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PRICE PER M² COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📐 Price per m² Comparison":
    st.markdown(f"""
    <div style="margin-bottom:1.2rem">
        <div style="font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;color:{MUTED};margin-bottom:0.3rem">
            Nairobi Real Estate · 2026
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:1.9rem;color:{TEXT}">
            Price per m² Comparison
        </div>
        <div style="color:{MUTED};font-size:0.88rem">
            Standardised density metric for comparing value across size, location and type
        </div>
    </div>
    """, unsafe_allow_html=True)

    overall_ppsf = dff["price_per_sqft"].median()
    max_loc      = (dff.groupby("Location")["price_per_sqft"].median().idxmax()
                    if dff["Location"].nunique() > 1 else "—")
    max_loc_val  = (dff.groupby("Location")["price_per_sqft"].median().max()
                    if dff["Location"].nunique() > 1 else 0)
    max_type     = dff.groupby("Property Type")["price_per_sqft"].median().idxmax()
    max_type_val = dff.groupby("Property Type")["price_per_sqft"].median().max()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:{TEAL}">
            <div class="kpi-label">Overall Median KES/m²</div>
            <div class="kpi-value">{overall_ppsf:,.0f}</div>
            <div class="kpi-sub">across filtered listings</div>
        </div>
        <div class="kpi-card" style="--accent:{AMBER}">
            <div class="kpi-label">Highest Location</div>
            <div class="kpi-value">{max_loc}</div>
            <div class="kpi-sub">KES {max_loc_val:,.0f}/m²</div>
        </div>
        <div class="kpi-card" style="--accent:{CORAL}">
            <div class="kpi-label">Highest Property Type</div>
            <div class="kpi-value">{max_type}</div>
            <div class="kpi-sub">KES {max_type_val:,.0f}/m²</div>
        </div>
        <div class="kpi-card" style="--accent:{GREEN}">
            <div class="kpi-label">Price Range</div>
            <div class="kpi-value">{dff['price_per_sqft'].min():,.0f}–{dff['price_per_sqft'].quantile(0.95):,.0f}</div>
            <div class="kpi-sub">KES/m² (5th–95th pct)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header"><span class="section-title">Median KES/m² by Location</span><span class="section-sub">≥4 listings</span></div>', unsafe_allow_html=True)
        lc2 = dff["Location"].value_counts()
        bl2 = lc2[lc2 >= 4].index
        ppsf_loc = (dff[dff["Location"].isin(bl2)]
                    .groupby("Location")["price_per_sqft"]
                    .median().sort_values(ascending=True))
        colors_loc = [TEAL if v >= ppsf_loc.quantile(0.7) else
                      AMBER if v >= ppsf_loc.quantile(0.4) else
                      MUTED for v in ppsf_loc.values]
        fig = go.Figure(go.Bar(
            y=ppsf_loc.index, x=ppsf_loc.values, orientation="h",
            marker_color=colors_loc, marker_line_width=0,
            text=ppsf_loc.values.astype(int).astype(str),
            textposition="outside", textfont=dict(color=TEXT, size=10),
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=420,
                          xaxis_title="Median KES / m²", showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<div class="section-header"><span class="section-title">KES/m² by Property Type</span></div>', unsafe_allow_html=True)
        ppsf_type = (dff.groupby("Property Type")["price_per_sqft"]
                     .agg(["median","mean","count"]).reset_index()
                     .sort_values("median", ascending=False))
        ppsf_type = ppsf_type[ppsf_type["count"] >= 3]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=ppsf_type["Property Type"], y=ppsf_type["median"],
                              name="Median", marker_color=TEAL, marker_line_width=0))
        fig2.add_trace(go.Bar(x=ppsf_type["Property Type"], y=ppsf_type["mean"],
                              name="Mean", marker_color=AMBER, marker_line_width=0))
        fig2.update_layout(**PLOTLY_LAYOUT, height=270, barmode="group",
                           yaxis_title="KES / m²")
        fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                       bgcolor="rgba(0,0,0,0)", borderwidth=0))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-header"><span class="section-title">KES/m² vs Property Size</span></div>', unsafe_allow_html=True)
        sc2 = dff.dropna(subset=["Size (m2)","price_per_sqft"])
        sc2 = sc2[sc2["price_per_sqft"] < sc2["price_per_sqft"].quantile(0.97)]
        fig3 = go.Figure(go.Scatter(
            x=sc2["Size (m2)"], y=sc2["price_per_sqft"], mode="markers",
            marker=dict(color=sc2["Bedrooms"],
                        colorscale=[[0,NAVY],[0.33,TEAL],[0.66,AMBER],[1,CORAL]],
                        size=6, opacity=0.65, line=dict(width=0),
                        colorbar=dict(title="Beds", thickness=12,
                                      tickfont=dict(color=TEXT), title_font_color=TEXT)),
            hovertemplate="Size: %{x:.0f} m²<br>KES/m²: %{y:,.0f}<extra></extra>",
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=230, showlegend=False,
                           xaxis_title="Size (m²)", yaxis_title="KES / m²")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header"><span class="section-title">KES/m² Distribution by Property Type</span></div>', unsafe_allow_html=True)
    fig4 = go.Figure()
    types_s = (dff.groupby("Property Type")["price_per_sqft"]
               .median().sort_values(ascending=False).index.tolist())
    for i, pt in enumerate(types_s):
        sub = dff[dff["Property Type"] == pt]["price_per_sqft"].dropna()
        sub = sub[sub < sub.quantile(0.97)]
        if len(sub) >= 3:
            fig4.add_trace(go.Box(
                x=sub, name=pt,
                marker_color=PALETTE[i % len(PALETTE)],
                line_color=PALETTE[i % len(PALETTE)],
                fillcolor=f"rgba({int(PALETTE[i%len(PALETTE)][1:3],16)},"
                          f"{int(PALETTE[i%len(PALETTE)][3:5],16)},"
                          f"{int(PALETTE[i%len(PALETTE)][5:7],16)},0.15)",
                boxmean=True, orientation="h",
            ))
    fig4.update_layout(**PLOTLY_LAYOUT, height=280,
                       xaxis_title="KES / m²", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: AMENITY IMPACT
# ─────────────────────────────────────────────────────────────────────────────
elif page == "✨ Amenity Impact":
    st.markdown(f"""
    <div style="margin-bottom:1.2rem">
        <div style="font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;color:{MUTED};margin-bottom:0.3rem">
            Nairobi Real Estate · 2026
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:1.9rem;color:{TEXT}">
            Amenity Impact Analysis
        </div>
        <div style="color:{MUTED};font-size:0.88rem">
            How specific amenities shift listing prices relative to the market median
        </div>
    </div>
    """, unsafe_allow_html=True)

    global_median = dff["Price (KES)"].median()
    keywords = {
        "Swimming Pool":"Swimming Pool","Gym":"Gym","Generator":"Generator",
        "Borehole":"Borehole","Garden":"Garden","CCTV":"CCTV","Parking":"Parking",
        "SQ":"SQ","En Suite":"En Suite","Solar":"Solar","Lift":"Lift",
        "Electric Fence":"Electric Fence","Security":"Security",
    }
    uplift_rows = []
    for label, kw in keywords.items():
        mask = dff["Amenities"].str.contains(kw, case=False, na=False)
        n = mask.sum()
        if n >= 4:
            with_kw    = dff.loc[mask,  "Price (KES)"].median()
            without_kw = dff.loc[~mask, "Price (KES)"].median()
            uplift_pct = (with_kw / without_kw - 1) * 100 if without_kw > 0 else 0
            uplift_rows.append({"Amenity":label,"Uplift (%)":round(uplift_pct,1),
                                 "Median w/":with_kw,"Median w/o":without_kw,"n":int(n)})
    uplift_df = pd.DataFrame(uplift_rows).sort_values("Uplift (%)", ascending=True)

    best_amenity   = uplift_df.loc[uplift_df["Uplift (%)"].idxmax(), "Amenity"]
    best_uplift    = uplift_df["Uplift (%)"].max()
    luxury_premium = ((dff[dff["is_luxury"]==1]["Price (KES)"].mean() /
                       dff[dff["is_luxury"]==0]["Price (KES)"].mean()) - 1) * 100
    premium_n      = int(dff["is_luxury"].sum())
    tier_stats     = (dff.groupby("amenity_tier", observed=True)["Price (KES)"]
                      .agg(["median","count"]).reset_index())
    prem_m = tier_stats.loc[tier_stats["amenity_tier"]=="Premium (5+)","median"].values
    prem_m = float(prem_m[0]) if len(prem_m) else 0
    bas_m  = tier_stats.loc[tier_stats["amenity_tier"]=="Basic (1–2)","median"].values
    bas_m  = float(bas_m[0]) if len(bas_m) else 1
    tier_mult = prem_m / bas_m if bas_m else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:{TEAL}">
            <div class="kpi-label">Market Median</div>
            <div class="kpi-value">{global_median/1e6:.1f}M</div>
            <div class="kpi-sub">KES baseline</div>
        </div>
        <div class="kpi-card" style="--accent:{AMBER}">
            <div class="kpi-label">Top Amenity Uplift</div>
            <div class="kpi-value">+{best_uplift:.0f}%</div>
            <div class="kpi-sub">{best_amenity}</div>
        </div>
        <div class="kpi-card" style="--accent:{CORAL}">
            <div class="kpi-label">Luxury Premium</div>
            <div class="kpi-value">+{luxury_premium:.0f}%</div>
            <div class="kpi-sub">avg vs non-luxury · n={premium_n}</div>
        </div>
        <div class="kpi-card" style="--accent:{GREEN}">
            <div class="kpi-label">Premium vs Basic Tier</div>
            <div class="kpi-value">{tier_mult:.1f}×</div>
            <div class="kpi-sub">median price multiplier</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown('<div class="section-header"><span class="section-title">Price Uplift vs Market Median</span><span class="section-sub">% change in median price for listings featuring each amenity</span></div>', unsafe_allow_html=True)
        bar_colors_u = [GREEN if v > 0 else CORAL for v in uplift_df["Uplift (%)"]]
        fig = go.Figure(go.Bar(
            y=uplift_df["Amenity"], x=uplift_df["Uplift (%)"], orientation="h",
            marker_color=bar_colors_u, marker_line_width=0,
            text=uplift_df["Uplift (%)"].map(lambda v: f"{'+' if v>0 else ''}{v:.0f}%"),
            textposition="outside", textfont=dict(color=TEXT, size=10),
            customdata=uplift_df[["n","Median w/"]].values,
            hovertemplate=("<b>%{y}</b><br>Uplift: %{x:.1f}%<br>"
                           "Median with: KES %{customdata[1]:,.0f}<br>"
                           "n listings: %{customdata[0]}<extra></extra>"),
        ))
        fig.add_vline(x=0, line_color=MUTED, line_width=1)
        fig.update_layout(**PLOTLY_LAYOUT, height=420,
                          xaxis_title="Price Uplift vs Without (%)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<div class="section-header"><span class="section-title">Price by Amenity Tier</span></div>', unsafe_allow_html=True)
        tier_order = ["Basic (1–2)","Good (3–4)","Premium (5+)"]
        tier_plot  = tier_stats[tier_stats["amenity_tier"].isin(tier_order)].copy()
        tier_plot["amenity_tier"] = pd.Categorical(tier_plot["amenity_tier"],
                                                    categories=tier_order, ordered=True)
        tier_plot = tier_plot.sort_values("amenity_tier")
        fig2 = go.Figure(go.Bar(
            x=tier_plot["amenity_tier"].astype(str), y=tier_plot["median"] / 1e6,
            marker_color=[MUTED,AMBER,TEAL], marker_line_width=0,
            text=(tier_plot["median"]/1e6).map(lambda v: f"{v:.1f}M"),
            textposition="outside", textfont=dict(color=TEXT, size=11),
            customdata=tier_plot["count"].values,
            hovertemplate="<b>%{x}</b><br>Median: KES %{y:.1f}M<br>n=%{customdata}<extra></extra>",
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=250,
                           yaxis_title="Median Price (M KES)", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-header"><span class="section-title">Luxury Amenity Premium</span></div>', unsafe_allow_html=True)
        lux_df = (dff.groupby("is_luxury")["Price (KES)"]
                  .agg(["mean","median","count"]).reset_index())
        lux_df["label"] = lux_df["is_luxury"].map({0:"Standard",1:"Luxury"})
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=lux_df["label"], y=lux_df["mean"]/1e6, name="Mean",
                              marker_color=[MUTED,CORAL], marker_line_width=0,
                              text=(lux_df["mean"]/1e6).map(lambda v: f"{v:.1f}M"),
                              textposition="outside", textfont=dict(color=TEXT, size=11)))
        fig3.add_trace(go.Bar(x=lux_df["label"], y=lux_df["median"]/1e6, name="Median",
                              marker_color=[BORDER,TEAL], marker_line_width=0,
                              text=(lux_df["median"]/1e6).map(lambda v: f"{v:.1f}M"),
                              textposition="outside", textfont=dict(color=TEXT, size=11)))
        fig3.update_layout(**PLOTLY_LAYOUT, height=220, barmode="group",
                           yaxis_title="Price (M KES)")
        fig3.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                       bgcolor="rgba(0,0,0,0)", borderwidth=0))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header"><span class="section-title">Amenity Prevalence by Location</span><span class="section-sub">% of listings in each neighbourhood featuring each amenity</span></div>', unsafe_allow_html=True)
    top_kws    = ["Swimming Pool","Gym","Generator","Garden","CCTV","Parking","SQ","En Suite"]
    top_locs_h = dff["Location"].value_counts().head(8).index.tolist()
    hm_data    = []
    for loc in top_locs_h:
        sub_loc = dff[dff["Location"] == loc]
        for kw in top_kws:
            n   = sub_loc["Amenities"].str.contains(kw, case=False, na=False).sum()
            pct = n / len(sub_loc) * 100 if len(sub_loc) > 0 else 0
            hm_data.append({"Location":loc,"Amenity":kw,"pct":pct,"n":n})
    hm_df = pd.DataFrame(hm_data)
    pivot  = hm_df.pivot(index="Location", columns="Amenity", values="pct").fillna(0)
    fig_hm = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,NAVY],[0.3,TEAL_DARK],[0.6,TEAL],[1,AMBER]],
        text=pivot.values.round(0).astype(int).astype(str) + "%",
        texttemplate="%{text}", textfont=dict(size=10, color=TEXT),
        hovertemplate="<b>%{y}</b> · %{x}<br>%{z:.0f}% of listings<extra></extra>",
        colorbar=dict(title="% listings", thickness=12,
                      tickfont=dict(color=TEXT), title_font_color=TEXT),
    ))
    fig_hm.update_layout(**PLOTLY_LAYOUT, height=300)
    fig_hm.update_xaxes(side="bottom", gridcolor="rgba(0,0,0,0)")
    fig_hm.update_yaxes(gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header"><span class="section-title">Amenity Insights</span></div>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"""<div class="insight">
            <strong>Electric Fence & Solar</strong> show the largest raw uplifts —
            but these are present in very few listings, often in already-premium areas.
            They signal neighbourhood quality more than individual value-add.
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""<div class="insight">
            Surprisingly, <strong>Swimming Pool and En Suite</strong> show a slight
            negative correlation — they are heavily present in <strong>apartments</strong>
            which sit at the lower end of the price range.
        </div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"""<div class="insight">
            <strong>SQ (Service Quarter)</strong> appears in 63% of all listings and
            corresponds with a <strong>+37% uplift</strong> — the most
            democratically distributed premium amenity in the Nairobi market.
        </div>""", unsafe_allow_html=True)
