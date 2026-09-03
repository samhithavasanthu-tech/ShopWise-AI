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
# PROJECT ROOT
# -----------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

AUDIT_FILE = os.path.join(
    PROJECT_ROOT,
    "audit_log.json"
)


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("📜 AI + Blockchain Audit Trail")

st.write(
    "Track AI decisions, user actions, blockchain payments, "
    "and verified product reviews inside ShopWise AI."
)

st.divider()


# -----------------------------------
# LOAD AUDIT DATA
# -----------------------------------

def load_audit_logs():

    if not os.path.exists(AUDIT_FILE):
        return []

    try:

        with open(
            AUDIT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


audit_logs = load_audit_logs()


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
    audit_logs = list(
        reversed(audit_logs)
    )


    # -----------------------------------
    # AUDIT SUMMARY
    # -----------------------------------

    st.header("📊 Audit Summary")

    total_actions = len(
        audit_logs
    )


    searches = sum(
        1
        for log in audit_logs
        if log.get("action") == "Product Search"
    )


    selections = sum(
        1
        for log in audit_logs
        if log.get("action") == "Product Selected"
    )


    orders = sum(
        1
        for log in audit_logs
        if log.get("action") == "Order Approved by User"
    )


    blockchain_payments = sum(
        1
        for log in audit_logs
        if log.get("action")
        == "Blockchain Payment Created"
    )


    blockchain_verified = sum(
        1
        for log in audit_logs
        if log.get("action")
        == "Blockchain Payment Verified"
    )


    verified_reviews = sum(
        1
        for log in audit_logs
        if log.get("action")
        == "Verified Review Submitted"
    )


    # -----------------------------------
    # METRICS
    # -----------------------------------

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


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💳 Blockchain Payments",
        blockchain_payments
    )

    col2.metric(
        "🔗 Payments Verified",
        blockchain_verified
    )

    col3.metric(
        "⭐ Verified Reviews",
        verified_reviews
    )


    st.divider()


    # -----------------------------------
    # EVENT TYPE LEGEND
    # -----------------------------------

    st.header(
        "🏷️ Event Categories"
    )

    st.markdown(
        """
🔍 **Product Search** — User searches for products

🛒 **Product Selected** — User selects an AI recommendation

🧾 **Checkout Started** — User begins checkout

✅ **Order Approved** — User approves an order

💳 **Blockchain Payment Created** — Payment record created

🔗 **Blockchain Payment Verified** — Transaction verified

⭐ **Verified Review Submitted** — Review confirmed from a verified purchaser
"""
    )


    st.divider()


    # -----------------------------------
    # AUDIT LOGS
    # -----------------------------------

    st.header(
        "🧠 AI + Blockchain Activity Timeline"
    )


    # Event icons
    event_icons = {

        "Product Search": "🔍",

        "Product Selected": "🛒",

        "Checkout Started": "🧾",

        "Order Approved by User": "✅",

        "Blockchain Payment Created": "💳",

        "Blockchain Payment Verified": "🔗",

        "Verified Review Submitted": "⭐"

    }


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


        icon = event_icons.get(
            action,
            "📌"
        )


        with st.expander(
            f"{icon} {timestamp} — {action}"
        ):

            st.subheader(
                f"{icon} Event Details"
            )

            st.json(
                details
            )


    st.divider()


    # -----------------------------------
    # TRANSPARENCY SECTION
    # -----------------------------------

    st.header(
        "🔒 AI + Blockchain Transparency"
    )

    st.info(
        f"""
ShopWise AI has recorded **{total_actions} traceable events**.

The system tracks AI-driven shopping activity, including
**{searches} searches**, **{selections} product selections**,
and **{orders} approved orders**.

For commerce transparency, the system also records
**{blockchain_payments} blockchain payments** and
**{blockchain_verified} verified transactions**.

Customer trust is supported through
**{verified_reviews} verified product reviews**.

This creates a transparent and traceable commerce workflow
from AI recommendation to payment and verified feedback.
"""
    )


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "ShopWise AI Audit Trail | AI Transparency • "
    "Blockchain Traceability • Verified Commerce"
)