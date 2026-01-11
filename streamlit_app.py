import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Unit Economics Dashboard",
    layout="wide",
)

# ---------- GLOBAL STYLE ----------
st.markdown(
    """
    <style>
    /* Основной фон приложения */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #122720 0, #020308 45%, #020308 100%);
        color: #f9fafb;
    }

    /* Левая панель */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07140f 0%, #020308 60%, #020308 100%);
        color: #f9fafb;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    /* Контейнер контента */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Заголовок страницы */
    .ue-page-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    /* Карточки */
    .glass-card {
        background: rgba(10, 16, 24, 0.9);
        border-radius: 22px;
        padding: 18px 20px 16px 20px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.45);
        border: 1px solid rgba(255,255,255,0.04);
    }
    .glass-card h3 {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .glass-card h4 {
        font-size: 14px;
        font-weight: 500;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }

    /* Небольшой сабтекст */
    .ue-subtle {
        font-size: 12px;
        opacity: 0.75;
    }

    /* KPI цифры */
    .ue-kpi-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.7;
    }
    .ue-kpi-value {
        font-size: 24px;
        font-weight: 700;
        margin-top: 2px;
    }
    .ue-kpi-pill {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        margin-top: 4px;
        background: rgba(16, 185, 129, 0.12);
        color: #6ee7b7;
    }

    /* Таблицы */
    .glass-card table {
        font-size: 13px;
    }

    /* Нижняя карточка (Operating profit) */
    .ue-profit-card {
        margin-top: 12px;
    }

    /* Скрыть стандартный заголовок Streamlit */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR (LEFT NAV) ----------
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

# ---------- CALCULATIONS (same logic as before) ----------

# Inputs (unit / order)
col_left_top, col_right_top = st.columns([3, 2])

with col_left_top:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Unit / order gross margin")

    aov = st.number_input("AOV (average order value)", value=180.0, step=1.0)

    st.markdown('<div class="ue-subtle">Variable costs per order</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        landed_cogs = st.number_input("Landed COGS", value=32.0, step=0.1)
        returns = st.number_input("Returns (cost per order)", value=18.0, step=0.1)
        package = st.number_input("Package", value=2.0, step=0.1)
    with c2:
        processing = st.number_input("Processing (fees)", value=5.99, step=0.01)
        tpl = st.number_input("3PL", value=2.5, step=0.1)
        label = st.number_input("Label", value=8.0, step=0.1)

    variable_costs = landed_cogs + returns + package + processing + tpl + label
    contribution_margin = aov - variable_costs
    contribution_margin_pct = contribution_margin / aov * 100 if aov else 0

    st.markdown("</div>", unsafe_allow_html=True)

with col_right_top:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Monthly view (orders)")

    new_orders = st.number_input("New orders", value=850, step=1)
    returning_orders = st.number_input("Returning orders", value=170, step=1)

    total_orders = new_orders + returning_orders
    returning_share = returning_orders / total_orders * 100 if total_orders else 0

    o1, o2 = st.columns(2)
    with o1:
        st.markdown('<div class="ue-kpi-label">Total orders</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ue-kpi-value">{total_orders:,}</div>', unsafe_allow_html=True)
    with o2:
        st.markdown('<div class="ue-kpi-label">Returning share</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ue-kpi-value">{returning_share:.2f}%</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Margins per order + Contribution (monthly)
row2_col1, row2_col2 = st.columns([3, 3])

with row2_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Margins per order")

    ncac = st.number_input("nCAC (marketing per order)", value=65.0, step=1.0)
    ncac_pct = ncac / aov * 100 if aov else 0

    operation_margin = contribution_margin - ncac
    operation_margin_pct = operation_margin / aov * 100 if aov else 0

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown('<div class="ue-kpi-label">Contribution margin</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ue-kpi-value">{currency}{contribution_margin:,.0f}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ue-kpi-pill">{contribution_margin_pct:.2f}%</div>',
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown('<div class="ue-kpi-label">nCAC</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ue-kpi-value">{currency}{ncac:,.0f}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ue-kpi-pill">{ncac_pct:.2f}%</div>',
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown('<div class="ue-kpi-label">Operating margin per order</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ue-kpi-value">{currency}{operation_margin:,.0f}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ue-kpi-pill">{operation_margin_pct:.2f}%</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Contribution margin (monthly)")

    revenue_m = aov * total_orders
    cogs_m = landed_cogs * total_orders
    returns_m = returns * total_orders
    package_m = package * total_orders
    processing_m = processing * total_orders
    tpl_m = tpl * total_orders
    label_m = label * total_orders

    variable_costs_m = cogs_m + returns_m + package_m + processing_m + tpl_m + label_m
    contribution_m = revenue_m - variable_costs_m

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

# Operating margin (monthly) + Cost breakdown
row3_col1, row3_col2 = st.columns([3, 3])

with row3_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Operating margin (monthly)")

    marketing = st.number_input("Marketing spend (monthly)", value=55250.0, step=100.0)
    warehouse = st.number_input("Warehouse", value=3000.0, step=100.0)
    payroll = st.number_input("Payroll", value=6000.0, step=100.0)
    software = st.number_input("Software", value=3000.0, step=100.0)
    content_misc = st.number_input("Content", value=7000.0, step=100.0)

    fixed_costs = warehouse + payroll + software + content_misc
    operating_profit = contribution_m - marketing - fixed_costs
    operating_profit_pct = operating_profit / revenue_m * 100 if revenue_m else 0

    st.markdown("</div>", unsafe_allow_html=True)

    # Отдельная нижняя карточка для Operating profit
    st.markdown('<div class="glass-card ue-profit-card">', unsafe_allow_html=True)
    st.markdown("#### Operating profit (monthly)")
    st.markdown(
        f'<div class="ue-kpi-value">{currency}{operating_profit:,.0f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="ue-kpi-pill">{operating_profit_pct:.2f}%</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with row3_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Cost breakdown per order")

    if aov > 0:
        data_unit = [
            ("Landed COGS", landed_cogs, landed_cogs / aov * 100),
            ("Returns", returns, returns / aov * 100),
            ("Package", package, package / aov * 100),
            ("Processing", processing, processing / aov * 100),
            ("3PL", tpl, tpl / aov * 100),
            ("Labels", label, label / aov * 100),
        ]
        df_unit = pd.DataFrame(data_unit, columns=["Name", "Amount", "% of AOV"])
        df_unit["Amount"] = df_unit["Amount"].map(lambda x: f"{currency}{x:,.2f}")
        df_unit["% of AOV"] = df_unit["% of AOV"].map(lambda x: f"{x:.2f}%")
        st.table(df_unit)
    else:
        st.info("Set AOV > 0 to see breakdown.")

    st.markdown("</div>", unsafe_allow_html=True)
