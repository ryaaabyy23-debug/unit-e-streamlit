import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Unit Economics Dashboard", layout="wide")

# ---------------- GLOBAL STYLES ----------------
st.markdown(
    """
    <style>
    /* App background */
    [data-testid="stAppViewContainer"]{
        background: radial-gradient(circle at 15% 10%, #1a3a2a 0%, #0b0f12 35%, #07090b 100%);
        color: #e9edf2;
    }

    /* Remove top padding a bit */
    .block-container{
        padding-top: 22px !important;
        padding-bottom: 42px !important;
        max-width: 1200px;
    }

    /* Sidebar */
    [data-testid="stSidebar"]{
        background: linear-gradient(180deg, #1a3a2a 0%, #0b0f12 55%, #07090b 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] *{
        color: #e9edf2 !important;
    }

    /* Headings */
    h1,h2,h3{
        letter-spacing: 0.2px;
    }
    .page-title{
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 0.6px;
        margin: 4px 0 18px 0;
        text-transform: uppercase;
    }

    /* Cards */
    .card{
        background: #ffffff;
        border-radius: 18px;
        padding: 16px 16px 14px 16px;
        box-shadow: 0 14px 40px rgba(0,0,0,0.35);
        border: 1px solid rgba(0,0,0,0.06);
    }
    .card-title{
        color: #151a1f;
        font-weight: 800;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .card-subtitle{
        color: rgba(21,26,31,0.70);
        font-size: 12px;
        margin-top: -4px;
        margin-bottom: 10px;
    }

    /* Labels */
    label{
        color: rgba(21,26,31,0.85) !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }

    /* Inputs (Number) */
    div[data-baseweb="input"] input{
        background: #f3f1ea !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0,0,0,0.10) !important;
        color: #151a1f !important;
        font-weight: 600 !important;
        height: 40px !important;
    }
    div[data-baseweb="input"] input:focus{
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(34,197,94,0.20) !important;
        border: 1px solid rgba(34,197,94,0.45) !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div{
        background: #0b0f12 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
    }

    /* “Pill” for percents */
    .pill{
        display:inline-flex;
        align-items:center;
        gap:6px;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(34,197,94,0.12);
        color: #16a34a;
        font-weight: 800;
        font-size: 12px;
        border: 1px solid rgba(34,197,94,0.22);
        margin-top: 6px;
    }

    /* Big number metric in white card */
    .big-metric{
        color:#151a1f;
        font-weight: 900;
        font-size: 28px;
        line-height: 1.0;
        margin: 2px 0 2px 0;
    }
    .metric-label{
        color: rgba(21,26,31,0.60);
        font-weight: 800;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 8px;
    }

    /* Tables inside cards */
    .stTable, .stDataFrame{
        color:#151a1f !important;
    }
    .stTable table{
        border-collapse: collapse !important;
        width: 100% !important;
    }
    .stTable th{
        text-align: left !important;
        font-size: 12px !important;
        color: rgba(21,26,31,0.65) !important;
        border-bottom: 1px solid rgba(0,0,0,0.12) !important;
        padding: 8px 6px !important;
    }
    .stTable td{
        font-size: 13px !important;
        padding: 8px 6px !important;
        border-bottom: 1px solid rgba(0,0,0,0.06) !important;
    }

    /* Hide Streamlit default menu/footer spacing a bit */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### ecom mode")
    st.write("")
    nav = st.radio(
        "Navigation",
        ["Profile", "Unit Economy", "LTV & Scale", "Finance plan", "Finance track"],
        index=1,
        label_visibility="collapsed"
    )
    st.write("---")
    currency = st.selectbox("Currency", ["$", "€", "£"], index=0)
    st.caption("Change inputs below to model different scenarios.")

# ---------------- HEADER ----------------
st.markdown('<div class="page-title">UNIT ECONOMY</div>', unsafe_allow_html=True)

# ---------------- INPUTS / CALCS (same logic) ----------------
# Base inputs (left top)
aov = 0.0
landed_cogs = 0.0
returns = 0.0
package = 0.0
processing = 0.0
tpl = 0.0
label = 0.0

# Monthly inputs (right top)
new_orders = 0
returning_orders = 0

# nCAC per order (left mid)
ncac = 0.0

# Monthly fixed costs (left bottom)
marketing = 0.0
warehouse = 0.0
payroll = 0.0
software = 0.0
content_misc = 0.0

# ---------------- GRID LAYOUT (matches your PDF) ----------------
row1_left, row1_right = st.columns(2, gap="large")

# ===== CARD 1: Unit/order gross margin =====
with row1_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Unit/order gross margin</div>', unsafe_allow_html=True)

    aov = st.number_input("AOV (average order value)", value=320.0, step=1.0)

    st.markdown('<div class="card-subtitle">Variable costs per order</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        landed_cogs = st.number_input("Landed COGS", value=160.0, step=0.1)
        returns = st.number_input("Returns (cost per order)", value=0.0, step=0.1)
        package = st.number_input("Package", value=0.0, step=0.1)
    with c2:
        processing = st.number_input("Processing (fees)", value=4.0, step=0.01)
        tpl = st.number_input("3PL", value=0.0, step=0.1)
        label = st.number_input("Label", value=0.0, step=0.1)

    st.markdown("</div>", unsafe_allow_html=True)

# ===== CARD 2: Monthly view (orders) =====
with row1_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Monthly view (orders)</div>', unsafe_allow_html=True)

    new_orders = st.number_input("New orders", value=135, step=1)
    returning_orders = st.number_input("Returning orders", value=10, step=1)

    total_orders = new_orders + returning_orders
    returning_share = (returning_orders / total_orders * 100) if total_orders else 0.0

    m1, m2 = st.columns(2, gap="medium")
    with m1:
        st.markdown('<div class="metric-label">Total orders</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-metric">{total_orders:,}</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-label">Returning share</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-metric">{returning_share:.2f}%</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CALCS ----------------
variable_costs = landed_cogs + returns + package + processing + tpl + label
contribution_margin = aov - variable_costs
contribution_margin_pct = (contribution_margin / aov * 100) if aov else 0.0

ncac = 75.0  # default like your design
# We will render the input in the “Margins per order” card (and overwrite it)
# Operation per order will be computed after ncac input is read.

# Monthly contribution
revenue_m = aov * total_orders
cogs_m = landed_cogs * total_orders
returns_m = returns * total_orders
package_m = package * total_orders
processing_m = processing * total_orders
tpl_m = tpl * total_orders
label_m = label * total_orders
variable_costs_m = cogs_m + returns_m + package_m + processing_m + tpl_m + label_m
contribution_m = revenue_m - variable_costs_m

# ---------------- SECOND ROW ----------------
row2_left, row2_right = st.columns(2, gap="large")

# ===== CARD 3: Margins per order =====
with row2_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Margins per order</div>', unsafe_allow_html=True)

    ncac = st.number_input("nCAC (marketing per order)", value=75.0, step=1.0)
    ncac_pct = (ncac / aov * 100) if aov else 0.0

    operation_margin = contribution_margin - ncac
    operation_margin_pct = (operation_margin / aov * 100) if aov else 0.0

    k1, k2, k3 = st.columns(3, gap="medium")

    with k1:
        st.markdown('<div class="metric-label">Contribution margin</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-metric">{currency}{contribution_margin:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pill">↗ {contribution_margin_pct:.2f}%</div>', unsafe_allow_html=True)

    with k2:
        st.markdown('<div class="metric-label">nCAC</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-metric">{currency}{ncac:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pill">↗ {ncac_pct:.2f}%</div>', unsafe_allow_html=True)

    with k3:
        st.markdown('<div class="metric-label">Operating margin per order</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-metric">{currency}{operation_margin:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pill">↗ {operation_margin_pct:.2f}%</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ===== CARD 4: Contribution margin (monthly) =====
with row2_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Contribution margin (monthly)</div>', unsafe_allow_html=True)

    data_m = [
        ("Revenue", revenue_m),
        ("COGS", cogs_m),
        ("Returns", returns_m),
        ("Processing", processing_m),
        ("Package", package_m),
        ("3PL", tpl_m),
        ("Labels", label_m),
        ("Contribution", contribution_m),
    ]
    df_m = pd.DataFrame(data_m, columns=["Name", "Amount"])
    df_m["Amount"] = df_m["Amount"].map(lambda x: f"{currency}{x:,.0f}")

    st.table(df_m)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- THIRD ROW ----------------
row3_left, row3_right = st.columns(2, gap="large")

# ===== CARD 5: Operating margin (monthly) =====
with row3_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Operating margin (monthly)</div>', unsafe_allow_html=True)

    marketing = st.number_input("Marketing spend (monthly)", value=10000.0, step=100.0)
    warehouse = st.number_input("Warehouse", value=0.0, step=100.0)
    payroll = st.number_input("Payroll", value=1000.0, step=100.0)
    software = st.number_input("Software", value=500.0, step=50.0)
    content_misc = st.number_input("Content", value=620.0, step=50.0)

    fixed_costs = warehouse + payroll + software + content_misc
    operating_profit = contribution_m - marketing - fixed_costs
    operating_profit_pct = (operating_profit / revenue_m * 100) if revenue_m else 0.0

    st.write("")
    st.markdown('<div class="metric-label">Operating profit (monthly)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-metric">{currency}{operating_profit:,.0f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pill">↗ {operating_profit_pct:.2f}%</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ===== CARD 6: Cost breakdown per order =====
with row3_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Cost breakdown per order</div>', unsafe_allow_html=True)

    if aov > 0:
        data = [
            ("Landed COGS", landed_cogs, landed_cogs / aov * 100),
            ("Returns", returns, returns / aov * 100),
            ("Package", package, package / aov * 100),
            ("Processing", processing, processing / aov * 100),
            ("3PL", tpl, tpl / aov * 100),
            ("Labels", label, label / aov * 100),
        ]
        df_unit = pd.DataFrame(data, columns=["Name", "Amount", "% of AOV"])
        df_unit["Amount"] = df_unit["Amount"].map(lambda x: f"{currency}{x:,.2f}")
        df_unit["% of AOV"] = df_unit["% of AOV"].map(lambda x: f"{x:.2f}%")
        st.table(df_unit)
    else:
        st.info("Set AOV > 0 to see breakdown.")

    st.markdown("</div>", unsafe_allow_html=True)
