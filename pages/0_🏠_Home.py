import streamlit as st
import json
import os
import sys


# -------------------------------------------------
# ADD PROJECT ROOT TO PYTHON PATH
# -------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


# -------------------------------------------------
# IMPORT PROJECT FUNCTIONS
# -------------------------------------------------

from blockchain.trust_score import (
    calculate_trust_score
)

from blockchain.review_verification import (
    get_reviews_by_product
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="ShopWise AI",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------------------------
# LOAD PRODUCTS
# -------------------------------------------------

PRODUCTS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "products.json"
)


def load_products():

    try:

        with open(
            PRODUCTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        return []


products = load_products()


# -------------------------------------------------
# PAGE HERO
# -------------------------------------------------

st.title(
    "🤖 Welcome to ShopWise AI"
)

st.subheader(
    "AI-Powered Agentic Commerce with Blockchain Trust"
)

st.write(
    """
    ShopWise AI helps users discover products using artificial
    intelligence, verifies purchases through a blockchain-inspired
    payment system, and builds product trust using verified reviews.
    """
)

st.divider()


# -------------------------------------------------
# PLATFORM STATISTICS
# -------------------------------------------------

st.header(
    "📊 ShopWise AI Platform Overview"
)


total_products = len(
    products
)


total_reviews = 0

trust_scores = []


for product in products:

    product_id = product.get(
        "id"
    )


    # VERIFIED REVIEWS

    reviews = get_reviews_by_product(
        product_id
    )


    total_reviews += len(
        reviews
    )


    # TRUST SCORE

    trust_data = calculate_trust_score(
        product_id
    )


    trust_scores.append(
        trust_data.get(
            "trust_score",
            0
        )
    )


# -------------------------------------------------
# AVERAGE TRUST
# -------------------------------------------------

if trust_scores:

    average_trust = (
        sum(trust_scores)
        / len(trust_scores)
    )

else:

    average_trust = 0


# -------------------------------------------------
# METRICS
# -------------------------------------------------

col1, col2, col3 = st.columns(
    3
)


with col1:

    st.metric(
        "🛍️ Products Available",
        total_products
    )


with col2:

    st.metric(
        "⭐ Verified Reviews",
        total_reviews
    )


with col3:

    st.metric(
        "🛡️ Average Trust Score",
        f"{average_trust:.1f}/100"
    )


st.divider()


# -------------------------------------------------
# PROJECT FEATURES
# -------------------------------------------------

st.header(
    "🚀 What Can ShopWise AI Do?"
)


col1, col2, col3 = st.columns(
    3
)


# -------------------------------------------------
# FEATURE 1
# -------------------------------------------------

with col1:

    st.subheader(
        "🤖 AI Shopping Agent"
    )

    st.write(
        """
        • Understands user shopping intent

        • Searches products based on needs

        • Considers user budget

        • Calculates AI product match scores
        """
    )


# -------------------------------------------------
# FEATURE 2
# -------------------------------------------------

with col2:

    st.subheader(
        "🛡️ Trust-Based Recommendations"
    )

    st.write(
        """
        • Uses verified customer reviews

        • Calculates product trust scores

        • Combines AI relevance with trust

        • Ranks products intelligently
        """
    )


# -------------------------------------------------
# FEATURE 3
# -------------------------------------------------

with col3:

    st.subheader(
        "💳 Blockchain Payments"
    )

    st.write(
        """
        • Generates transaction hashes

        • Verifies purchase records

        • Tracks wallet payment history

        • Enables verified reviews
        """
    )


st.divider()


# -------------------------------------------------
# COMPLETE USER JOURNEY
# -------------------------------------------------

st.header(
    "🔄 How ShopWise AI Works"
)


st.markdown(
    """
### 🛍️ 1. Discover Products

The user enters their requirements and budget.

⬇️

### 🧠 2. AI Understands Intent

ShopWise AI analyzes what the user needs.

⬇️

### 🏆 3. Products Are Ranked

Products are ranked using:

**70% AI Relevance + 30% Trust Score**

⬇️

### 🛒 4. User Selects a Product

The AI provides recommendations and cross-sell suggestions.

⬇️

### 💳 5. Blockchain Payment

A blockchain-inspired transaction record is created.

⬇️

### ⭐ 6. Verified Review

Only verified purchasers can submit reviews.

⬇️

### 🛡️ 7. Trust Score Updates

Verified reviews improve the product's reputation and
future AI recommendations.
"""
)


st.divider()


# -------------------------------------------------
# QUICK NAVIGATION
# -------------------------------------------------

st.header(
    "⚡ Explore ShopWise AI"
)


st.info(
    """
Use the sidebar to explore all ShopWise AI modules:

🛍️ Shop → Find AI-powered product recommendations

📊 Revenue Dashboard → View shopping and revenue metrics

📜 AI Audit Trail → View AI decisions and user actions

💳 Blockchain Payments → Create and verify payments

⭐ Verified Reviews → Submit reviews after purchase verification

🏆 Trust & Reputation → Explore product trust rankings
"""
)


# -------------------------------------------------
# TECHNOLOGY OVERVIEW
# -------------------------------------------------

st.divider()

st.header(
    "⚙️ Technology Stack"
)


col1, col2, col3, col4 = st.columns(
    4
)


with col1:

    st.metric(
        "Frontend",
        "Streamlit"
    )


with col2:

    st.metric(
        "AI Layer",
        "Python Agent"
    )


with col3:

    st.metric(
        "Trust Layer",
        "Verified Reviews"
    )


with col4:

    st.metric(
        "Payments",
        "Blockchain Demo"
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "🚀 ShopWise AI — Building trustworthy, "
    "transparent, and intelligent agentic commerce."
)