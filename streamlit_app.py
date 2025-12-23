import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Unit Economics Calculator",
    layout="wide",
)

st.title("Unit Economy – per order & monthly")

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("Scenario settings")

    currency = st.selectbox("Currency", ["$", "€", "£"], index=0)
    st.caption("Change inputs below to model different scenarios.")

# ========== LAYOUT ==========
col_left, col_right = st.columns(2)

# ---------- LEFT: PER ORDER ----------
with col_left:
    st.subheader("Unit / order gross margin")

    aov = st.number_input("AOV (average order value)", value=180.0, step=1.0)

    st.markdown("**Variable costs per order**")
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

    st.markdown("---")
    st.markdown("### Margins per order")

    # nCAC (marketing per order)
    ncac = st.number_input("nCAC (marketing per order)", value=65.0, step=1.0)
    ncac_pct = ncac / aov * 100 if aov else 0

    operation_margin = contribution_margin - ncac
    operation_margin_pct = operation_margin / aov * 100 if aov else 0

    cm_col, ncac_col, opm_col = st.columns(3)
    with cm_col:
        st.metric(
            "Contribution margin",
            f"{currency}{contribution_margin:,.0f}",
            f"{contribution_margin_pct:.2f}%"
        )
    with ncac_col:
        st.metric(
            "nCAC",
            f"{currency}{ncac:,.0f}",
            f"{ncac_pct:.2f}%"
        )
    with opm_col:
        st.metric(
            "Operating margin per order",
            f"{currency}{operation_margin:,.0f}",
            f"{operation_margin_pct:.2f}%"
        )

    # Табличка по юниту (как в Google Sheet)
    st.markdown("#### Cost breakdown per order")

    if aov > 0:
        data = [
            ("Landed COGS", landed_cogs, landed_cogs / aov * 100),
            ("Returns", returns, returns / aov * 100),
            ("Package", package, package / aov * 100),
            ("Processing", processing, processing / aov * 100),
            ("3PL", tpl, tpl / aov * 100),
            ("Label", label, label / aov * 100),
        ]
        df_unit = pd.DataFrame(data, columns=["Item", "Cost", "% of AOV"])
        df_unit["Cost"] = df_unit["Cost"].map(lambda x: f"{currency}{x:,.2f}")
        df_unit["% of AOV"] = df_unit["% of AOV"].map(lambda x: f"{x:.2f}%")
        st.dataframe(df_unit, use_container_width=True)
    else:
        st.info("Set AOV > 0 to see breakdown.")


# ---------- RIGHT: MONTHLY ----------
with col_right:
    st.subheader("Monthly view")

    st.markdown("#### Orders")
    new_orders = st.number_input("New orders", value=850, step=1)
    returning_orders = st.number_input("Returning orders", value=170, step=1)

    total_orders = new_orders + returning_orders
    returning_share = returning_orders / total_orders * 100 if total_orders else 0

    o1, o2 = st.columns(2)
    with o1:
        st.metric("Total orders", f"{total_orders:,}")
    with o2:
        st.metric("Returning share", f"{returning_share:.2f}%")

    st.markdown("#### Contribution margin (monthly)")

    revenue_m = aov * total_orders
    cogs_m = landed_cogs * total_orders
    returns_m = returns * total_orders
    package_m = package * total_orders
    processing_m = processing * total_orders
    tpl_m = tpl * total_orders
    label_m = label * total_orders

    variable_costs_m = cogs_m + returns_m + package_m + processing_m + tpl_m + label_m
    contribution_m = revenue_m - variable_costs_m

    # Таблица, похожая на правый блок contribution в таблице
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
    df_m = pd.DataFrame(data_m, columns=["Item", "Amount"])
    df_m["Amount"] = df_m["Amount"].map(lambda x: f"{currency}{x:,.0f}")
    st.table(df_m)

    st.markdown("#### Operating margin (monthly)")

    marketing = st.number_input("Marketing spend (monthly)", value=55250.0, step=100.0)
    warehouse = st.number_input("Warehouse", value=3000.0, step=100.0)
    payroll = st.number_input("Payroll", value=6000.0, step=100.0)
    software = st.number_input("Software", value=3000.0, step=100.0)
    content_misc = st.number_input("Content + misc", value=7000.0, step=100.0)

    fixed_costs = warehouse + payroll + software + content_misc
    operating_profit = contribution_m - marketing - fixed_costs
    operating_profit_pct = operating_profit / revenue_m * 100 if revenue_m else 0

    st.metric(
        "Operating profit (monthly)",
        f"{currency}{operating_profit:,.0f}",
        f"{operating_profit_pct:.2f}%"
    )

    st.caption("Marketing is treated as variable, other items as fixed costs.")
