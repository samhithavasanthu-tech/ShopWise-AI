import streamlit as st
import json
import os


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AI Audit Trail - ShopWise AI",
    page_icon="📜",
    layout="wide"
)


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("📜 AI Audit Trail")

st.write(
    "Track important AI decisions and user actions made inside ShopWise AI."
)

st.divider()


# -----------------------------------
# AUDIT LOG FILE
# -----------------------------------

audit_file = "audit_log.json"


# -----------------------------------
# LOAD AUDIT DATA
# -----------------------------------

if not os.path.exists(audit_file):

    st.warning("No audit logs available yet.")

else:

    try:

        with open(audit_file, "r") as file:
            audit_logs = json.load(file)

    except json.JSONDecodeError:

        audit_logs = []


    # -----------------------------------
    # CHECK IF LOGS EXIST
    # -----------------------------------

    if not audit_logs:

        st.info(
            "No actions have been recorded yet. "
            "Go to the Shop page and perform some actions."
        )

    else:

        # Show newest logs first
        audit_logs.reverse()


        # -----------------------------------
        # AUDIT SUMMARY
        # -----------------------------------

        st.header("📊 Audit Summary")

        total_actions = len(audit_logs)

        searches = sum(
            1 for log in audit_logs
            if log.get("action") == "Product Search"
        )

        selections = sum(
            1 for log in audit_logs
            if log.get("action") == "Product Selected"
        )

        orders = sum(
            1 for log in audit_logs
            if log.get("action") == "Order Approved by User"
        )


        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "📜 Total Actions",
            total_actions
        )

        col2.metric(
            "🔍 Searches",
            searches
        )

        col3.metric(
            "🛒 Product Selections",
            selections
        )

        col4.metric(
            "✅ Approved Orders",
            orders
        )


        st.divider()


        # -----------------------------------
        # AUDIT LOGS
        # -----------------------------------

        st.header("🧠 AI Decision & Action History")


        for log in audit_logs:

            timestamp = log.get(
                "timestamp",
                "Unknown Time"
            )

            action = log.get(
                "action",
                "Unknown Action"
            )

            details = log.get(
                "details",
                {}
            )


            with st.expander(
                f"🕒 {timestamp} — {action}"
            ):

                st.subheader("Action Details")

                st.json(details)


        st.divider()


        # -----------------------------------
        # TRANSPARENCY MESSAGE
        # -----------------------------------

        st.header("🔒 AI Transparency")

        st.info(
            """
            ShopWise AI records important actions such as product searches,
            product selections, checkout decisions, and user approvals.

            This audit trail helps make AI-assisted commerce decisions
            transparent, traceable, and trustworthy.
            """
        )