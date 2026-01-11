import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Unit Economics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- GLOBAL STYLE ----------
st.markdown(
    """
    <style>
    /* Основной фон и текст */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #122720 0, #020308 45%, #020308 100%);
        color: #f9fafb;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Левая панель */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07140f 0%, #020308 60%, #020308 100%);
        color: #f9fafb;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stSidebar"] * {
        color: #f9fafb !important;
    }

    /* Топовый заголовок */
    .ue-page-title {
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        opacity: 0.9;
        margin-bottom: 0.25rem;
    }
    .ue-page-subtitle {
        font-size: 13px;
        opacity: 0.7;
        margin-bottom: 1.2rem;
    }

    /* KPI карточки */
    .ue-kpi-card {
        background: radial-gradient(circle at top left, #111827 0, #020617 55%, #020617 100%);
        border-radius: 20px;
        padding: 14px 16px 12px 16px;
        border: 1px solid rgba(148,163,184,0.25);
        box-shadow: 0 16px 40px rgba(15,23,42,0.65);
    }
    .ue-kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        opacity: 0.7;
        margin-bottom: 2px;
    }
    .ue-kpi-value {
        font-size: 22px;
        font-weight: 700;
        line-height: 1.2;
    }
    .ue-kpi-sub {
        font-size: 11px;
        opacity: 0.75;
        margin-top: 4px;
    }
    .ue-kpi-pill-pos {
        display: inline-block;
        margin-top: 4px;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        background: rgba(34,197,94,0.1);
        color: #4ade80;
    }

    /* Универсальная "стеклянная" карточка */
    .glass-card {
        background: rgba(15,23,42,0.95);
        border-radius: 22px;
        padding: 18px 20px 16px 20px;
        border: 1px solid rgba(148,163,184,0.3);
        box-shadow: 0 18px 40px rgba(15,23,42,0.8);
    }
    .glass-card h3 {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .ue-section-caption {
        font-size: 11px;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin-bottom: 0.4rem;
    }

    /* Подписи внизу */
    .ue-caption {
        font-size: 11px;
        opacity: 0.7;
        margin-top: 6px;
    }

    /* Таблицы чуть меньше шрифтом */
    .glass-card table {
        font-size: 13px;
    }

    /* Чуть скруглить стандартные инпуты */
    input, textarea, select {
        border-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### ecom mode")
    st.markdown("---")

    menu = st.radio(
        "Navigation",
        ["Profile", "Unit Economy", "LTV & Scale", "Finance plan", "Finance track"],
        index=1,
        label_visibility="collapsed",
    )

    st.markdown("---")
    currency = st.selectbox("Currency", ["$", "€", "£"], index=0)
    st.caption("Change inputs below to model different scenarios.")

# Пока реализуем только Unit Economy
if menu != "Unit Economy":
    st.write("This section will be available later. Switch to **Unit Economy** in the left menu.")
    st.stop()

# ---------- INPUTS & CALCULATIONS (логика та же) ----------

# Пер-ордер входные
aov = st.session_state.get("aov", 180.0)  # просто чтобы логика рядом была
# Но читаем всё сразу ниже в карточке — здесь пока только объявления не нужны


# Собираем все входные данные в скрытом блоке (чтобы расчёты были до отрисовки KPI)
with st.container():
    # Unit / order inputs
    aov = st.number_input("AOV (average order value)", value=180.0, step=1.0, key="__hidden_aov__", label_visibility="collapsed")
    landed_cogs = st.number_input("Landed COGS", value=32.0, step=0.1, key="__hidden_cogs__", label_visibility="collapsed")
    returns = st.number_input("Returns (cost per order)", value=18.0, step=0.1, key="__hidden_returns__", label_visibility="collapsed")
    package = st.number_input("Package", value=2.0, step=0.1, key="__hidden_package__", label_visibility="collapsed")
    processing = st.number_input("Processing (fees)", value=5.99, step=0.01, key="__hidden_processing__", label_visibility="collapsed")
    tpl = st.number_input("3PL", value=2.5, step=0.1, key="__hidden_tpl__", label_visibility="collapsed")
    label_cost = st.number_input("Label", value=8.0, step=0.1, key="__hidden_label__", label_visibility="collapsed")

    ncac = st.number_input("nCAC (marketing per order)", value=65.0, step=1.0, key="__hidden_ncac__", label_visibility="collapsed")

    new_orders = st.number_input("New orders", value=850, step=1, key="__hidden_new_orders__", label_visibility="collapsed")
    returning_orders = st.number_input("Returning orders", value=170, step=1, key="__hidden_ret_orders__", label_visibility="collapsed")

    marketing = st.number_input("Marketing spend (monthly)", value=55250.0, step=100.0, key="__hidden_marketing__", label_visibility="collapsed")
    warehouse = st.number_input("Warehouse", value=3000.0, step=100.0, key="__hidden_wh__", label_visibility="collapsed")
    payroll = st.number_input("Payroll", value=6000.0, step=100.0, key="__hidden_pay__", label_visibility="collapsed")
    software = st.number_input("Software", value=3000.0, step=100.0, key="__hidden_soft__", label_visibility="collapsed")
    content_misc = st.number_input("Content + misc", value=7000.0, step=100.0, key="__hidden_content__", label_visibility="collapsed")

# Расчёты
variable_costs = landed_cogs + returns + package + processing + tpl + label_cost
contribution_margin = aov - variable_costs
contribution_margin_pct = contribution_margin / aov * 100 if aov else 0

ncac_pct = ncac / aov * 100 if aov else 0
operation_margin = contribution_margin - ncac
operation_margin_pct = operation_margin / aov * 100 if aov else 0

total_orders = new_orders + returning_orders
returning_share = returning_orders / total_orders * 100 if total_orders else 0

revenue_m = aov * total_orders
cogs_m = landed_cogs * total_orders
returns_m = returns * total_orders
package_m = package * total_orders
processing_m = processing * total_orders
tpl_m = tpl * total_orders
label_m = label_cost * total_orders

variable_costs_m = cogs_m + returns_m + package_m + processing_m + tpl_m + label_m
contribution_m = revenue_m - variable_costs_m

fixed_costs = warehouse + payroll + software + content_misc
operating_profit = contribution_m - marketing - fixed_costs
operating_profit_pct = operating_profit / revenue_m * 100 if revenue_m else 0

# ---------- HEADER ----------
st.markdown('<div class="ue-page-title">UNIT ECONOMY DASHBOARD</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="ue-page-subtitle">Per-order & monthly view: quickly see if your offer is actually profitable.</div>',
    unsafe_allow_html=True,
)

# ---------- TOP KPI ROW ----------
k1, k2, k3, k4 = st.columns(4)

def kpi(col, label, value, sub="", delta=None):
    with col:
        st.markdown(
            f"""
            <div class="ue-kpi-card">
                <div class="ue-kpi-label">{label}</div>
                <div class="ue-kpi-value">{value}</div>
                <div class="ue-kpi-sub">{sub}</div>
                {f'<div class="ue-kpi-pill-pos">{delta}</div>' if delta else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

kpi(
    k1,
    "Monthly revenue",
    f"{currency}{revenue_m:,.0f}",
    f"AOV {currency}{aov:,.0f} · {total_orders:,} orders",
)
kpi(
    k2,
    "Contribution margin per order",
    f"{currency}{contribution_margin:,.0f}",
    f"{contribution_margin_pct:.1f}% of AOV",
)
kpi(
    k3,
    "Operating profit (monthly)",
    f"{currency}{operating_profit:,.0f}",
    f"After marketing & fixed costs",
)
kpi(
    k4,
    "Operating margin %",
    f"{operating_profit_pct:.1f}%",
    f"nCAC {currency}{ncac:,.0f} · {ncac_pct:.1f}% of AOV",
)

st.markdown("")  # небольшой отступ

# ---------- SECOND ROW: LEFT (inputs), RIGHT (monthly contrib) ----------
row2_left, row2_right = st.columns([3, 3])

with row2_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="ue-section-caption">Per order inputs</div>', unsafe_allow_html=True)
    st.markdown("### Unit / order gross margin")

    c1, c2 = st.columns(2)
    with c1:
        aov = st.number_input("AOV (average order value)", value=aov, step=1.0)
        landed_cogs = st.number_input("Landed COGS", value=landed_cogs, step=0.1)
        package = st.number_input("Package", value=package, step=0.1)
        tpl = st.number_input("3PL", value=tpl, step=0.1)
    with c2:
        returns = st.number_input("Returns (cost per order)", value=returns, step=0.1)
        processing = st.number_input("Processing (fees)", value=processing, step=0.01)
        label_cost = st.number_input("Label", value=label_cost, step=0.1)

    variable_costs = landed_cogs + returns + package + processing + tpl + label_cost
    contribution_margin = aov - variable_costs
    contribution_margin_pct = contribution_margin / aov * 100 if aov else 0
    ncac = st.number_input("nCAC (marketing per order)", value=ncac, step=1.0)
    ncac_pct = ncac / aov * 100 if aov else 0
    operation_margin = contribution_margin - ncac
    operation_margin_pct = operation_margin / aov * 100 if aov else 0

    st.markdown('<div class="ue-section-caption" style="margin-top:12px;">Per order margins</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Contribution", f"{currency}{contribution_margin:,.0f}", f"{contribution_margin_pct:.1f}%")
    with m2:
        st.metric("nCAC", f"{currency}{ncac:,.0f}", f"{ncac_pct:.1f}%")
    with m3:
        st.metric("Operating margin", f"{currency}{operation_margin:,.0f}", f"{operation_margin_pct:.1f}%")

    st.markdown('<div class="ue-caption">Tune AOV, costs and nCAC to see when per-order margin becomes healthy.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="ue-section-caption">Monthly volume</div>', unsafe_allow_html=True)
    st.markdown("### Monthly view (orders)")

    o1, o2 = st.columns(2)
    with o1:
        new_orders = st.number_input("New orders", value=new_orders, step=1)
    with o2:
        returning_orders = st.number_input("Returning orders", value=returning_orders, step=1)

    total_orders = new_orders + returning_orders
    returning_share = returning_orders / total_orders * 100 if total_orders else 0

    k_orders, k_ret = st.columns(2)
    with k_orders:
        st.metric("Total orders", f"{total_orders:,}")
    with k_ret:
        st.metric("Returning share", f"{returning_share:.1f}%")

    # Пересчёт месячной contribution
    revenue_m = aov * total_orders
    cogs_m = landed_cogs * total_orders
    returns_m = returns * total_orders
    package_m = package * total_orders
    processing_m = processing * total_orders
    tpl_m = tpl * total_orders
    label_m = label_cost * total_orders
    variable_costs_m = cogs_m + returns_m + package_m + processing_m + tpl_m + label_m
    contribution_m = revenue_m - variable_costs_m

    st.markdown('<div class="ue-section-caption" style="margin-top:12px;">Contribution breakdown</div>', unsafe_allow_html=True)
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

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- THIRD ROW: OPEX + COST BREAKDOWN ----------
row3_left, row3_right = st.columns([3, 3])

with row3_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="ue-section-caption">Operating expenses</div>', unsafe_allow_html=True)
    st.markdown("### Operating margin (monthly)")

    c1, c2 = st.columns(2)
    with c1:
        marketing = st.number_input("Marketing spend", value=marketing, step=100.0)
        warehouse = st.number_input("Warehouse", value=warehouse, step=100.0)
    with c2:
        payroll = st.number_input("Payroll", value=payroll, step=100.0)
        software = st.number_input("Software", value=software, step=100.0)
    content_misc = st.number_input("Content + misc", value=content_misc, step=100.0)

    fixed_costs = warehouse + payroll + software + content_misc
    operating_profit = contribution_m - marketing - fixed_costs
    operating_profit_pct = operating_profit / revenue_m * 100 if revenue_m else 0

    st.markdown('<div class="ue-section-caption" style="margin-top:12px;">Result</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.metric("Operating profit", f"{currency}{operating_profit:,.0f}")
    with p2:
        st.metric("Operating margin %", f"{operating_profit_pct:.1f}%")

    st.markdown('<div class="ue-caption">Use this block to model how overheads and ad spend affect final profit.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row3_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="ue-section-caption">Unit economics detail</div>', unsafe_allow_html=True)
    st.markdown("### Cost breakdown per order")

    if aov > 0:
        data_unit = [
            ("Landed COGS", landed_cogs, landed_cogs / aov * 100),
            ("Returns", returns, returns / aov * 100),
            ("Package", package, package / aov * 100),
            ("Processing", processing, processing / aov * 100),
            ("3PL", tpl, tpl / aov * 100),
            ("Label", label_cost, label_cost / aov * 100),
        ]
        df_unit = pd.DataFrame(data_unit, columns=["Name", "Amount", "% of AOV"])
        df_unit["Amount"] = df_unit["Amount"].map(lambda x: f"{currency}{x:,.2f}")
        df_unit["% of AOV"] = df_unit["% of AOV"].map(lambda x: f"{x:.2f}%")
        st.table(df_unit)
    else:
        st.info("Set AOV > 0 to see breakdown.")

    st.markdown('</div>', unsafe_allow_html=True)
