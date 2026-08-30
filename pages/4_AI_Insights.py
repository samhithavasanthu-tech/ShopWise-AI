import streamlit as st
import json
import os


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AI Insights - ShopWise AI",
    page_icon="📈",
    layout="wide"
)


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("📈 AI Insights")

st.write(
    "AI-powered insights based on customer searches, selections, "
    "checkouts, and approved orders."
)

st.divider()


# -----------------------------------
# LOAD AUDIT LOG
# -----------------------------------

audit_file = "audit_log.json"

if not os.path.exists(audit_file):

    st.warning(
        "No data available yet. Use the Shop page first to generate AI insights."
    )

else:

    try:

        with open(audit_file, "r") as file:
            audit_logs = json.load(file)

    except json.JSONDecodeError:

        audit_logs = []


    # -----------------------------------
    # CHECK DATA
    # -----------------------------------

    if not audit_logs:

        st.info(
            "No customer activity found yet. "
            "Go to the Shop page and search for products."
        )

    else:

        # -----------------------------------
        # INITIAL VALUES
        # -----------------------------------

        searches = 0
        selections = 0
        checkouts = 0
        approved_orders = 0

        approved_revenue = 0
        cross_sell_revenue = 0

        search_queries = []


        # -----------------------------------
        # ANALYZE DATA
        # -----------------------------------

        for log in audit_logs:

            action = log.get("action", "")
            details = log.get("details", {})


            # Product Search
            if action == "Product Search":

                searches += 1

                query = details.get(
                    "user_query",
                    ""
                )

                if query:
                    search_queries.append(query)


            # Product Selected
            elif action == "Product Selected":

                selections += 1


            # Checkout Started
            elif action == "Checkout Started":

                checkouts += 1

                cross_sell_revenue += details.get(
                    "potential_cross_sell_revenue",
                    0
                )


            # Order Approved
            elif action == "Order Approved by User":

                approved_orders += 1

                approved_revenue += details.get(
                    "total_amount",
                    0
                )


        # -----------------------------------
        # AI ACTIVITY OVERVIEW
        # -----------------------------------

        st.header("🤖 AI Activity Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🔍 Searches",
            searches
        )

        col2.metric(
            "🛒 Product Selections",
            selections
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
        # CONVERSION INSIGHTS
        # -----------------------------------

        st.header("🎯 Conversion Insights")

        if searches > 0:

            selection_rate = (
                selections / searches
            ) * 100

            order_conversion = (
                approved_orders / searches
            ) * 100

        else:

            selection_rate = 0
            order_conversion = 0


        col1, col2 = st.columns(2)

        col1.metric(
            "🛍️ Search → Selection Rate",
            f"{selection_rate:.1f}%"
        )

        col2.metric(
            "🚀 Search → Order Rate",
            f"{order_conversion:.1f}%"
        )


        st.divider()


        # -----------------------------------
        # REVENUE INSIGHTS
        # -----------------------------------

        st.header("💰 Revenue Insights")

        col1, col2 = st.columns(2)

        col1.metric(
            "📈 Cross-Sell Revenue Potential",
            f"₹{cross_sell_revenue}"
        )

        col2.metric(
            "💰 Approved Revenue",
            f"₹{approved_revenue}"
        )


        st.divider()


        # -----------------------------------
        # CUSTOMER SEARCH INSIGHTS
        # -----------------------------------

        st.header("🔍 Customer Search Insights")

        if search_queries:

            st.write(
                "Recent customer product searches:"
            )

            # Show latest searches first
            recent_searches = list(
                reversed(search_queries)
            )

            for index, query in enumerate(
                recent_searches[:5],
                start=1
            ):

                st.write(
                    f"{index}. 🤖 {query}"
                )

        else:

            st.info(
                "No product search queries available yet."
            )


        st.divider()


        # -----------------------------------
        # AI BUSINESS INSIGHT
        # -----------------------------------

        st.header("🧠 AI Business Insight")


        if approved_orders > 0:

            st.success(
                f"""
                ShopWise AI has successfully helped convert
                customer activity into **{approved_orders} approved order(s)**.

                The total approved revenue is currently
                **₹{approved_revenue}**.

                AI-powered cross-selling has identified
                **₹{cross_sell_revenue}** in additional revenue potential.
                """
            )

        elif selections > 0:

            st.info(
                """
                Customers are selecting products, which indicates
                interest in AI recommendations.

                The next opportunity is improving checkout conversion
                and encouraging users to approve their orders.
                """
            )

        else:

            st.warning(
                """
                More customer interactions are needed to generate
                meaningful AI insights.

                Go to the Shop page and perform product searches.
                """
            )


        st.divider()


        # -----------------------------------
        # AI RECOMMENDATION
        # -----------------------------------

        st.header("💡 AI Growth Recommendation")


        if searches > 0 and selections == 0:

            recommendation = (
                "Improve product matching because users are searching "
                "but not selecting products."
            )

        elif selections > 0 and approved_orders == 0:

            recommendation = (
                "Improve checkout experience and user confidence "
                "to increase order approvals."
            )

        elif approved_orders > 0:

            recommendation = (
                "Continue using personalized recommendations and "
                "cross-selling to increase average order value."
            )

        else:

            recommendation = (
                "Collect more customer interactions to generate "
                "better AI-powered insights."
            )


        st.info(
            f"🤖 **ShopWise AI Recommendation:** {recommendation}"
        )