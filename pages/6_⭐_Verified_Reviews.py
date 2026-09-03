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
# IMPORT REVIEW FUNCTIONS
# -------------------------------------------------

from blockchain.review_verification import (
    submit_review,
    get_reviews_by_product,
    calculate_average_rating
)

from blockchain.payment_service import (
    has_verified_purchase
)

from blockchain.trust_score import (
    calculate_trust_score
)

from utils.audit_logger import (
    log_action
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Verified Reviews | ShopWise AI",
    page_icon="⭐",
    layout="wide"
)


# -------------------------------------------------
# PAGE TITLE
# -------------------------------------------------

st.title("⭐ Verifiable Product Reviews")

st.markdown("""
Welcome to the **ShopWise AI Verified Review System**.

Users can submit a review only after the system verifies that
their wallet has a confirmed purchase for the selected product.
""")

st.divider()


# -------------------------------------------------
# LOAD PRODUCTS
# -------------------------------------------------

PRODUCTS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "products.json"
)


def load_products():

    if not os.path.exists(PRODUCTS_FILE):
        return []

    try:

        with open(
            PRODUCTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


products = load_products()


# -------------------------------------------------
# WALLET ADDRESS
# -------------------------------------------------

st.subheader("👛 Step 1: Enter Your Wallet Address")

wallet_address = st.text_input(
    "Wallet Address",
    placeholder="Enter the wallet used for payment"
)


# -------------------------------------------------
# PRODUCT SELECTION
# -------------------------------------------------

st.subheader("🛍️ Step 2: Select Product")


selected_product = None


if not products:

    st.error(
        "No products found. Please check data/products.json"
    )

else:

    product_names = [
        product["name"]
        for product in products
    ]

    selected_product_name = st.selectbox(
        "Select a Product",
        product_names
    )

    selected_product = next(
        (
            product
            for product in products
            if product["name"] == selected_product_name
        ),
        None
    )


# -------------------------------------------------
# PRODUCT TRUST SCORE
# -------------------------------------------------

if selected_product:

    st.divider()

    st.subheader(
        "🛡️ Product Trust Score"
    )

    trust_data = calculate_trust_score(
        selected_product["id"]
    )

    trust_score = trust_data[
        "trust_score"
    ]

    average_trust_rating = trust_data[
        "average_rating"
    ]

    verified_reviews_count = trust_data[
        "verified_reviews"
    ]

    verified_purchases_count = trust_data[
        "verified_purchases"
    ]


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "🛡️ Trust Score",
        f"{trust_score}/100"
    )


    col2.metric(
        "⭐ Average Rating",
        f"{average_trust_rating}/5"
    )


    col3.metric(
        "💬 Verified Reviews",
        verified_reviews_count
    )


    col4.metric(
        "🔗 Verified Purchases",
        verified_purchases_count
    )


    # ---------------------------------------------
    # TRUST LEVEL
    # ---------------------------------------------

    if trust_score >= 80:

        st.success(
            "🟢 High Trust Product"
        )

    elif trust_score >= 50:

        st.info(
            "🟡 Medium Trust Product"
        )

    else:

        st.warning(
            "🔴 Building Trust"
        )


# -------------------------------------------------
# VERIFIED PURCHASE CHECK
# -------------------------------------------------

st.divider()

st.subheader("🔍 Step 3: Check Purchase Verification")


verified_purchase = False


if wallet_address.strip() and selected_product:

    verified_purchase = has_verified_purchase(
        selected_product["id"],
        wallet_address.strip()
    )

    if verified_purchase:

        st.success(
            "✅ Verified Purchase Found!"
        )

        st.markdown(
            "### 🟢 VERIFIED PURCHASER"
        )

        st.caption(
            "You are eligible to submit a verified review."
        )

    else:

        st.warning(
            "⚠️ No verified purchase found for this "
            "product and wallet address."
        )

        st.caption(
            "Please purchase this product first "
            "using the Blockchain Payments page."
        )

else:

    st.info(
        "Enter your wallet address and select a "
        "product to check verification."
    )


# -------------------------------------------------
# SUBMIT VERIFIED REVIEW
# -------------------------------------------------

st.divider()

st.subheader("⭐ Step 4: Submit Your Review")


if verified_purchase:

    rating = st.slider(
        "Rating",
        min_value=1,
        max_value=5,
        value=5
    )

    review_text = st.text_area(
        "Write your review",
        placeholder=(
            "Share your experience with this product..."
        )
    )

    if st.button(
        "⭐ Submit Verified Review",
        use_container_width=True
    ):

        if not review_text.strip():

            st.warning(
                "Please write a review before submitting."
            )

        else:

            result = submit_review(
                product_id=selected_product["id"],
                wallet_address=wallet_address.strip(),
                rating=rating,
                review_text=review_text.strip()
            )

            if result["success"]:

                review = result["review"]

                # -----------------------------------------
                # AUDIT LOG
                # -----------------------------------------

                log_action(
                    "Verified Review Submitted",
                    {
                        "product_id": selected_product["id"],
                        "product_name": selected_product["name"],
                        "wallet_address": wallet_address.strip(),
                        "rating": rating,
                        "verified_purchase": True,
                        "review_id": review["review_id"],
                        "verification_method": review[
                            "verification_method"
                        ]
                    }
                )

                st.success(
                    "🎉 Verified Review Submitted Successfully!"
                )

                st.balloons()

                # Refresh page so Trust Score updates
                st.rerun()

            else:

                st.error(
                    result["message"]
                )

else:

    st.info(
        "Review submission will unlock after "
        "purchase verification."
    )


# -------------------------------------------------
# PRODUCT REVIEWS
# -------------------------------------------------

st.divider()

st.subheader("💬 Product Reviews")


if selected_product:

    reviews = get_reviews_by_product(
        selected_product["id"]
    )

    average_rating = calculate_average_rating(
        selected_product["id"]
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "⭐ Average Rating",
            f"{average_rating} / 5"
        )


    with col2:

        st.metric(
            "💬 Total Verified Reviews",
            len(reviews)
        )


    # ---------------------------------------------
    # DISPLAY REVIEWS
    # ---------------------------------------------

    if reviews:

        st.markdown(
            "### ⭐ Verified Customer Reviews"
        )

        for review in reversed(reviews):

            with st.container():

                st.markdown(
                    f"### {'⭐' * review['rating']}"
                )

                st.write(
                    review["review"]
                )

                st.success(
                    "✅ Verified Purchase"
                )

                st.caption(
                    f"Wallet: "
                    f"{review['wallet_address'][:8]}..."
                )

                st.caption(
                    f"Reviewed on: "
                    f"{review['timestamp']}"
                )

                st.divider()

    else:

        st.info(
            "No verified reviews yet for this product."
        )


# -------------------------------------------------
# TRUST SCORE EXPLANATION
# -------------------------------------------------

st.divider()

st.subheader(
    "🛡️ How the Product Trust Score Works"
)

st.markdown("""
The ShopWise AI Trust Score is calculated out of **100 points**:

- ⭐ **Average Verified Rating** → Maximum **60 points**
- 💬 **Number of Verified Reviews** → Maximum **20 points**
- 🔗 **Confirmed Blockchain Purchases** → Maximum **20 points**

Only verified purchase data is used to calculate the score.
This helps create a more transparent and trustworthy commerce platform.
""")


# -------------------------------------------------
# INFORMATION
# -------------------------------------------------

st.divider()

st.caption(
    "🔗 Phase 1 Demo: Trust scores are calculated using "
    "verified reviews and confirmed blockchain payment records."
)