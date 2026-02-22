"""
Nairobi House Price Estimator — Streamlit App
Day 5: Pricing tool built on dataset patterns from 400 Nairobi listings.
"""

import streamlit as st
from predictor import NairobiPricePredictor

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nairobi House Price Estimator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — dark earth aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:      #0f0e0c;
    --surface: #1a1814;
    --card:    #211f1b;
    --border:  #333028;
    --accent:  #c9952a;
    --gold:    #e8b84b;
    --text:    #f0ebe0;
    --muted:   #8a8070;
    --green:   #4caf7d;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }

[data-testid="block-container"] {
    padding: 2rem 4rem !important;
    max-width: 1200px !important;
    margin: 0 auto;
}

/* Hero */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: var(--gold);
    margin: 0 0 0.4rem;
}
.hero p { color: var(--muted); font-size: 1rem; font-weight: 300; margin: 0; }
.hero .tag {
    display: inline-block;
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--accent);
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    color: var(--accent);
    margin-bottom: 1rem;
}

/* Result panel */
.result-panel {
    background: linear-gradient(135deg, #1e1c17 0%, #252118 100%);
    border: 1.5px solid var(--accent);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    text-align: center;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.result-panel::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(201,149,42,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.result-label {
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.result-price {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: var(--gold);
    font-weight: 700;
    line-height: 1.1;
}
.result-range {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.5rem;
}
.result-range span { color: var(--text); font-weight: 500; }

/* Metric row */
.metric-row { display: flex; gap: 0.8rem; margin-bottom: 1rem; }
.metric-box {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem;
    text-align: center;
}
.metric-val { font-family:'Playfair Display',serif; font-size:1.3rem; color:var(--gold); }
.metric-lbl { font-size:0.68rem; color:var(--muted); letter-spacing:1px; text-transform:uppercase; margin-top:2px; }

/* Driver bars */
.driver-wrap { margin: 0.5rem 0; }
.driver-label { font-size:0.8rem; color:var(--muted); display:flex; justify-content:space-between; margin-bottom:3px; }
.bar-bg { background:var(--surface); border-radius:4px; height:7px; overflow:hidden; }
.bar-fill { height:100%; border-radius:4px; background: linear-gradient(90deg, var(--accent), var(--gold)); }

/* Explanation */
.expl-line { font-size:0.86rem; color:#c8c0b0; margin:0.3rem 0; }

/* Empty state */
.empty-state {
    min-height: 380px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border: 1px dashed var(--border);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
}
.empty-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.empty-title { font-family:'Playfair Display',serif; font-size:1.2rem; color:var(--accent); }
.empty-sub { color:var(--muted); font-size:0.88rem; margin-top:0.4rem; }

/* Streamlit widget overrides */
label { color: var(--muted) !important; font-size: 0.82rem !important; }
.stSelectbox > div > div,
.stNumberInput > div { background: var(--surface) !important; border-color: var(--border) !important; border-radius: 8px !important; }
[data-baseweb="multi-select"] { background: var(--surface) !important; border-color: var(--border) !important; }
[data-baseweb="tag"] { background: var(--card) !important; border-color: var(--border) !important; }
[data-testid="stSlider"] .rc-slider-rail { background: var(--border) !important; }
[data-testid="stSlider"] .rc-slider-track { background: var(--accent) !important; }
[data-testid="stSlider"] .rc-slider-handle { border-color: var(--accent) !important; background: var(--gold) !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--gold)) !important;
    color: #0f0e0c !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Predictor
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_predictor():
    return NairobiPricePredictor()

predictor = load_predictor()

# ─────────────────────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="tag">🇰🇪 Nairobi Real Estate · 400 Listings</div>
    <h1>House Price Estimator</h1>
    <p>Pricing based on neighbourhood medians, property type, size, and amenity data from Nairobi listings</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    # Location & type
    st.markdown('<div class="card"><div class="card-title">📍 Location & Property Type</div>', unsafe_allow_html=True)
    location = st.selectbox(
        "Neighbourhood",
        options=predictor.LOCATIONS,
        index=predictor.LOCATIONS.index("Westlands"),
    )
    property_type = st.selectbox("Property Type", options=predictor.PROPERTY_TYPES)
    st.markdown('</div>', unsafe_allow_html=True)

    # Size & rooms
    st.markdown('<div class="card"><div class="card-title">📐 Size & Rooms</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3, step=1)
    with c2:
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2, step=1)
    size_m2 = st.slider("Size (m²)", min_value=30, max_value=1000, value=120, step=10)
    st.markdown('</div>', unsafe_allow_html=True)

    # Amenities
    st.markdown('<div class="card"><div class="card-title">✨ Amenities</div>', unsafe_allow_html=True)
    amenities = st.multiselect(
        "Select all that apply",
        options=predictor.AMENITY_OPTIONS,
        default=[],
    )
    st.markdown('</div>', unsafe_allow_html=True)

    estimate_btn = st.button("Calculate Price Estimate", use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────────────────────────────────────
with col_right:
    if estimate_btn or "result" in st.session_state:
        if estimate_btn:
            result = predictor.predict(
                location=location,
                property_type=property_type,
                bedrooms=int(bedrooms),
                bathrooms=int(bathrooms),
                size_m2=float(size_m2),
                amenities=amenities,
            )
            st.session_state["result"] = result

        r = st.session_state["result"]

        # Price
        st.markdown(f"""
        <div class="result-panel">
            <div class="result-label">Estimated Market Value</div>
            <div class="result-price">KES {r['predicted_price']:,.0f}</div>
            <div class="result-range">
                Range: <span>KES {r['range_low']:,.0f}</span> &ndash; <span>KES {r['range_high']:,.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick metrics
        price_m = r["predicted_price"] / 1_000_000
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-val">KES {price_m:.1f}M</div>
                <div class="metric-lbl">Total Price</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">{r['price_per_m2']:,.0f}</div>
                <div class="metric-lbl">Per m&sup2;</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">&plusmn;{r['mae']/1e6:.1f}M</div>
                <div class="metric-lbl">Typical Range</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Drivers
        st.markdown('<div class="card"><div class="card-title">📊 Price Drivers</div>', unsafe_allow_html=True)
        for label, weight in r["drivers"].items():
            pct = round(weight * 100)
            st.markdown(f"""
            <div class="driver-wrap">
                <div class="driver-label"><span>{label}</span><span>{pct}%</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width:{pct}%"></div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Explanation
        st.markdown('<div class="card"><div class="card-title">💡 What drives this estimate?</div>', unsafe_allow_html=True)
        for line in r["explanation"]:
            st.markdown(f'<p class="expl-line">&bull; {line}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🏘️</div>
            <div class="empty-title">Ready to Estimate</div>
            <div class="empty-sub">Fill in the property details on the left<br>and click <strong>Calculate Price Estimate</strong></div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#555048;font-size:0.76rem;padding:1.5rem 0;border-top:1px solid #222018;margin-top:1rem">
    Estimates based on 400 cleaned Nairobi property listings &nbsp;&middot;&nbsp;
    MAE &asymp; KES 4.6M &nbsp;&middot;&nbsp;
    <em>For indicative purposes only &mdash; consult a licensed valuer for formal appraisals</em>
</div>
""", unsafe_allow_html=True)
