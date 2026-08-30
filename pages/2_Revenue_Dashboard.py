import streamlit as st
import json
import os


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Revenue Dashboard - ShopWise AI",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("📊 Revenue Dashboard")

st.write(
    "Monitor AI-driven shopping activity, orders, and potential revenue."
)

st.divider()


# -----------------------------------
# LOAD AUDIT LOG
# -----------------------------------

audit_file = "audit_log.json"


if not os.path.exists(audit_file):

    st.warning("No audit data available yet.")

else:

    with open(audit_file, "r") as file:

        try:
            audit_logs = json.load(file)

        except json.JSONDecodeError:
            audit_logs = []


    # -----------------------------------
    # INITIAL VALUES
    # -----------------------------------

    searches = 0
    products_selected = 0
    checkouts = 0
    approved_orders = 0

    potential_revenue = 0
    approved_revenue = 0


    # -----------------------------------
    # ANALYZE AUDIT LOGS
    # -----------------------------------

    for log in audit_logs:

        action = log.get("action", "")
        details = log.get("details", {})


        if action == "Product Search":

            searches += 1


        elif action == "Product Selected":

            products_selected += 1


        elif action == "Checkout Started":

            checkouts += 1

            potential_revenue += details.get(
                "potential_cross_sell_revenue",
                0
            )


        elif action == "Order Approved by User":

            approved_orders += 1

            approved_revenue += details.get(
                "total_amount",
                0
            )


    # -----------------------------------
    # MAIN METRICS
    # -----------------------------------

    st.header("📈 Business Metrics")

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "🔍 Product Searches",
        searches
    )


    col2.metric(
        "🛒 Products Selected",
        products_selected
    )


    col3.metric(
        "🧾 Checkout Started",
        checkouts
    )


    col4.metric(
        "✅ Approved Orders",
        approved_orders
    )


    st.divider()


    # -----------------------------------
    # REVENUE METRICS
    # -----------------------------------

    st.header("💰 Revenue Performance")

    col1, col2 = st.columns(2)


    col1.metric(
        "📈 Cross-Sell Revenue Potential",
        f"₹{potential_revenue}"
    )


    col2.metric(
        "💰 Approved Revenue",
        f"₹{approved_revenue}"
    )


    st.divider()


    # -----------------------------------
    # AI PERFORMANCE INSIGHTS
    # -----------------------------------

    st.header("🤖 AI Performance Insights")


    if searches > 0:

        conversion_rate = (
            approved_orders / searches
        ) * 100

    else:

        conversion_rate = 0


    if products_selected > 0:

        selection_rate = (
            products_selected / searches
        ) * 100

    else:

        selection_rate = 0


    col1, col2 = st.columns(2)


    col1.metric(
        "🎯 Product Selection Rate",
        f"{selection_rate:.1f}%"
    )


    col2.metric(
        "🚀 Search to Order Conversion",
        f"{conversion_rate:.1f}%"
    )


    # -----------------------------------
    # BUSINESS SUMMARY
    # -----------------------------------

    st.divider()

    st.header("📋 AI Business Summary")


    st.info(
        f"""
        ShopWise AI has processed **{searches} product searches**.

        Users selected **{products_selected} products** and started
        **{checkouts} checkout sessions**.

        The system has recorded **{approved_orders} approved orders**
        with total approved revenue of **₹{approved_revenue}**.
        """
    )