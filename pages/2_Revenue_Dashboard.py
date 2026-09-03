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
    "Monitor AI-driven shopping activity, revenue, blockchain "
    "payments, and verified customer reviews."
)

st.divider()


# -----------------------------------
# PROJECT FILES
# -----------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

AUDIT_FILE = os.path.join(
    PROJECT_ROOT,
    "audit_log.json"
)

PAYMENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "blockchain_payments.json"
)

REVIEWS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "reviews.json"
)


# -----------------------------------
# LOAD JSON DATA
# -----------------------------------

def load_json(file_path):

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


# -----------------------------------
# LOAD DATA
# -----------------------------------

audit_logs = load_json(
    AUDIT_FILE
)

payments = load_json(
    PAYMENTS_FILE
)

reviews = load_json(
    REVIEWS_FILE
)


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
# ANALYZE AI AUDIT LOGS
# -----------------------------------

for log in audit_logs:

    action = log.get(
        "action",
        ""
    )

    details = log.get(
        "details",
        {}
    )


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
# BLOCKCHAIN PAYMENT ANALYSIS
# -----------------------------------

total_blockchain_payments = len(
    payments
)

confirmed_payments = [

    payment
    for payment in payments
    if payment.get(
        "status"
    ) == "confirmed"

]

verified_purchases = len(
    confirmed_payments
)

blockchain_revenue = sum(

    payment.get(
        "amount",
        0
    )

    for payment in confirmed_payments

)


# -----------------------------------
# REVIEW ANALYSIS
# -----------------------------------

total_verified_reviews = len(

    [
        review
        for review in reviews
        if review.get(
            "verified_purchase",
            False
        )
    ]

)


if total_verified_reviews > 0:

    total_rating = sum(

        review.get(
            "rating",
            0
        )

        for review in reviews

        if review.get(
            "verified_purchase",
            False
        )

    )


    average_rating = (
        total_rating
        / total_verified_reviews
    )

else:

    average_rating = 0


# -----------------------------------
# MAIN BUSINESS METRICS
# -----------------------------------

st.header(
    "📈 AI Commerce Metrics"
)

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

st.header(
    "💰 Revenue Performance"
)

col1, col2, col3 = st.columns(3)


col1.metric(
    "📈 Cross-Sell Revenue Potential",
    f"₹{potential_revenue:,}"
)


col2.metric(
    "💰 Approved Revenue",
    f"₹{approved_revenue:,}"
)


col3.metric(
    "🔗 Blockchain Revenue",
    f"₹{blockchain_revenue:,}"
)


st.divider()


# -----------------------------------
# BLOCKCHAIN METRICS
# -----------------------------------

st.header(
    "💳 Blockchain Payment Metrics"
)

col1, col2, col3 = st.columns(3)


col1.metric(
    "💳 Total Payments",
    total_blockchain_payments
)


col2.metric(
    "🔗 Verified Purchases",
    verified_purchases
)


col3.metric(
    "✅ Payment Success Rate",
    (
        f"{(verified_purchases / total_blockchain_payments * 100):.1f}%"
        if total_blockchain_payments > 0
        else "0.0%"
    )
)


st.divider()


# -----------------------------------
# VERIFIED REVIEW METRICS
# -----------------------------------

st.header(
    "⭐ Verified Review Metrics"
)

col1, col2 = st.columns(2)


col1.metric(
    "💬 Verified Reviews",
    total_verified_reviews
)


col2.metric(
    "⭐ Average Rating",
    f"{average_rating:.1f} / 5"
)


st.divider()


# -----------------------------------
# AI PERFORMANCE INSIGHTS
# -----------------------------------

st.header(
    "🤖 AI Performance Insights"
)


if searches > 0:

    selection_rate = (
        products_selected
        / searches
    ) * 100


    conversion_rate = (
        approved_orders
        / searches
    ) * 100

else:

    selection_rate = 0
    conversion_rate = 0


col1, col2 = st.columns(2)


col1.metric(
    "🎯 Product Selection Rate",
    f"{selection_rate:.1f}%"
)


col2.metric(
    "🚀 Search to Order Conversion",
    f"{conversion_rate:.1f}%"
)


st.divider()


# -----------------------------------
# BUSINESS & TRUST INSIGHTS
# -----------------------------------

st.header(
    "📋 AI + Blockchain Business Summary"
)


st.info(
    f"""
### 🤖 AI Commerce Activity

ShopWise AI has processed **{searches} product searches**.

Users selected **{products_selected} products** and started
**{checkouts} checkout sessions**.

The system has recorded **{approved_orders} approved orders**
with total approved revenue of **₹{approved_revenue:,}**.

---

### 🔗 Blockchain Commerce

The platform has processed
**{total_blockchain_payments} blockchain payment records**.

There are currently
**{verified_purchases} verified purchases**.

Total blockchain payment revenue is
**₹{blockchain_revenue:,}**.

---

### ⭐ Customer Trust

Customers have submitted
**{total_verified_reviews} verified product reviews**.

The current average verified rating is
**{average_rating:.1f} / 5 ⭐**.
"""
)


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "ShopWise AI combines AI-powered product discovery, "
    "revenue analytics, blockchain payment verification, "
    "and verified customer reviews."
)