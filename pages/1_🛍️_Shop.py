import streamlit as st
import json
import os
import sys


# -----------------------------------
# ADD PROJECT ROOT TO PYTHON PATH
# -----------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


# -----------------------------------
# IMPORT PROJECT FUNCTIONS
# -----------------------------------

from agent.shopping_agent import (
    find_products,
    analyze_intent
)

from agent.trust_recommender import (
    rank_products_by_trust
)

from utils.recommender import (
    get_recommendations
)

from utils.audit_logger import (
    log_action
)

from utils.payment_handoff import (
    save_order_for_payment
)

from blockchain.trust_score import (
    calculate_trust_score
)


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="ShopWise AI - Shop",
    page_icon="🛍️",
    layout="wide"
)


# -----------------------------------
# LOAD PRODUCTS
# -----------------------------------

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

    except FileNotFoundError:

        st.error(
            "❌ products.json file not found."
        )

        return []

    except json.JSONDecodeError:

        st.error(
            "❌ Invalid JSON format in products.json."
        )

        return []


products = load_products()


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "results" not in st.session_state:

    st.session_state["results"] = []


if "selected_product" not in st.session_state:

    st.session_state["selected_product"] = None


if "checkout" not in st.session_state:

    st.session_state["checkout"] = False


if "order_confirmed" not in st.session_state:

    st.session_state["order_confirmed"] = False


if "ai_intent" not in st.session_state:

    st.session_state["ai_intent"] = None


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title(
    "🛍️ ShopWise AI"
)

st.subheader(
    "AI Product Discovery & Trust-Based Agentic Shopping"
)

st.write(
    "Find the right products based on your needs, "
    "budget, AI relevance, and verified product trust."
)


# -----------------------------------
# USER INPUT
# -----------------------------------

st.header(
    "🔍 Find Your Product"
)


user_query = st.text_input(
    "What are you looking for?",
    placeholder=(
        "Example: I am a student and need "
        "a laptop for coding"
    )
)


budget = st.number_input(
    "Enter your maximum budget (₹)",
    min_value=0,
    value=60000
)


# -----------------------------------
# SEARCH PRODUCTS
# -----------------------------------

if st.button(
    "🔍 Find Products",
    use_container_width=True
):

    if not user_query.strip():

        st.warning(
            "⚠️ Please enter what you are looking for."
        )

    else:

        # AI INTENT ANALYSIS

        st.session_state[
            "ai_intent"
        ] = analyze_intent(
            user_query,
            budget
        )


        # FIND PRODUCTS

        search_results = find_products(
            products,
            user_query,
            budget
        )


        # TRUST-BASED RANKING

        st.session_state[
            "results"
        ] = rank_products_by_trust(
            search_results
        )


        # AUDIT LOG

        log_action(
            "Product Search",
            {
                "user_query": user_query,
                "budget": budget,
                "results_found": len(
                    st.session_state[
                        "results"
                    ]
                ),
                "ranking_method": (
                    "70% AI Match Score + "
                    "30% Product Trust Score"
                )
            }
        )


        # RESET SHOPPING STATE

        st.session_state[
            "selected_product"
        ] = None

        st.session_state[
            "checkout"
        ] = False

        st.session_state[
            "order_confirmed"
        ] = False


# -----------------------------------
# AI INTENT DETECTED
# -----------------------------------

if st.session_state[
    "ai_intent"
] is not None:

    intent = st.session_state[
        "ai_intent"
    ]

    st.divider()

    st.header(
        "🧠 AI Intent Detected"
    )


    categories = intent.get(
        "categories",
        []
    )


    if categories:

        category_text = ", ".join(
            categories
        )

    else:

        category_text = (
            "General Product Search"
        )


    col1, col2, col3 = st.columns(
        3
    )


    col1.metric(
        "🎯 Product Intent",
        category_text
    )


    col2.metric(
        "💡 Use Case",
        intent.get(
            "use_case",
            "General"
        )
    )


    col3.metric(
        "💰 Budget",
        f"₹{intent.get('budget', budget):,}"
    )


    st.info(
        "🤖 ShopWise AI analyzed your request "
        "and ranked products using AI relevance "
        "and verified product trust."
    )


# -----------------------------------
# SEARCH RESULTS
# -----------------------------------

if st.session_state[
    "results"
]:

    st.divider()

    st.success(
        "🤖 ShopWise AI found and ranked the "
        "best products for your request!"
    )


    for rank, product in enumerate(
        st.session_state["results"],
        start=1
    ):

        st.markdown(
            f"## 🏆 Recommendation #{rank}"
        )


        col1, col2 = st.columns(
            [1, 2]
        )


        # PRODUCT IMAGE

        with col1:

            if product.get("image"):

                st.image(
                    product["image"],
                    use_container_width=True
                )


        # PRODUCT INFORMATION

        with col2:

            st.subheader(
                product.get(
                    "name",
                    "Unknown Product"
                )
            )


            st.write(
                product.get(
                    "description",
                    ""
                )
            )


            st.write(
                f"💰 **Price: "
                f"₹{product.get('price', 0):,}**"
            )


            # AI MATCH SCORE

            match_score = product.get(
                "match_score",
                0
            )


            progress_value = min(
                max(
                    match_score / 100,
                    0
                ),
                1
            )


            st.progress(
                progress_value
            )


            st.write(
                f"🤖 **AI Match Score: "
                f"{match_score}%**"
            )


            # TRUST DATA

            trust_data = product.get(
                "trust_data"
            )


            if trust_data is None:

                trust_data = calculate_trust_score(
                    product["id"]
                )


            trust_score = product.get(
                "trust_score",
                trust_data.get(
                    "trust_score",
                    0
                )
            )


            # FINAL SCORE

            final_score = product.get(
                "final_score",
                round(
                    (
                        match_score * 0.7
                    )
                    +
                    (
                        trust_score * 0.3
                    ),
                    2
                )
            )


            # RECOMMENDATION INTELLIGENCE

            st.markdown(
                "### 🧠 Recommendation Intelligence"
            )


            score_col1, score_col2, score_col3 = (
                st.columns(3)
            )


            with score_col1:

                st.metric(
                    "🤖 AI Match",
                    f"{match_score}%"
                )


            with score_col2:

                st.metric(
                    "🛡️ Trust Score",
                    f"{trust_score}/100"
                )


            with score_col3:

                st.metric(
                    "🏆 Final Score",
                    f"{final_score}/100"
                )


            # TRUST DETAILS

            detail_col1, detail_col2 = (
                st.columns(2)
            )


            with detail_col1:

                st.metric(
                    "⭐ Verified Rating",
                    f"{trust_data.get('average_rating', 0)}/5"
                )


            with detail_col2:

                st.metric(
                    "💬 Verified Reviews",
                    trust_data.get(
                        "verified_reviews",
                        0
                    )
                )


            # TRUST LEVEL

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


            st.caption(
                "Final Score = 70% AI Relevance "
                "+ 30% Product Trust"
            )


            # SELECT PRODUCT

            if st.button(
                f"🛒 Select {product['name']}",
                key=f"select_{product['id']}",
                use_container_width=True
            ):

                st.session_state[
                    "selected_product"
                ] = product

                st.session_state[
                    "checkout"
                ] = False

                st.session_state[
                    "order_confirmed"
                ] = False


                log_action(
                    "Product Selected",
                    {
                        "product_name": product[
                            "name"
                        ],
                        "price": product[
                            "price"
                        ],
                        "category": product.get(
                            "category",
                            "Unknown"
                        ),
                        "match_score": match_score,
                        "trust_score": trust_score,
                        "final_recommendation_score":
                            final_score
                    }
                )

                st.rerun()


        st.divider()


# -----------------------------------
# SELECTED PRODUCT
# -----------------------------------

if st.session_state[
    "selected_product"
] is not None:

    selected_product = st.session_state[
        "selected_product"
    ]


    st.header(
        "🛒 Your Selected Product"
    )


    # TRUST DATA

    selected_trust_data = (
        calculate_trust_score(
            selected_product["id"]
        )
    )


    selected_trust_score = (
        selected_trust_data.get(
            "trust_score",
            0
        )
    )


    selected_match_score = (
        selected_product.get(
            "match_score",
            0
        )
    )


    selected_final_score = (
        selected_product.get(
            "final_score",
            round(
                (
                    selected_match_score * 0.7
                )
                +
                (
                    selected_trust_score * 0.3
                ),
                2
            )
        )
    )


    # PRODUCT SCORES

    col1, col2, col3, col4 = st.columns(
        4
    )


    col1.metric(
        "🤖 AI Match",
        f"{selected_match_score}%"
    )


    col2.metric(
        "🛡️ Trust Score",
        f"{selected_trust_score}/100"
    )


    col3.metric(
        "⭐ Verified Rating",
        (
            f"{selected_trust_data.get('average_rating', 0)}"
            "/5"
        )
    )


    col4.metric(
        "🏆 Final Score",
        f"{selected_final_score}/100"
    )


    # PRODUCT DETAILS

    col1, col2 = st.columns(
        [1, 2]
    )


    with col1:

        if selected_product.get(
            "image"
        ):

            st.image(
                selected_product[
                    "image"
                ],
                use_container_width=True
            )


    with col2:

        st.subheader(
            selected_product[
                "name"
            ]
        )


        st.write(
            selected_product.get(
                "description",
                ""
            )
        )


        st.write(
            f"💰 **Price: "
            f"₹{selected_product['price']:,}**"
        )


        st.subheader(
            "🧠 Why ShopWise AI Recommended This"
        )


        st.markdown(
            f"""
### AI Decision Explanation

- 🎯 Matches your detected product intent
- 📦 Product category: **{selected_product.get('category', 'Unknown')}**
- 💰 Price is within your budget of **₹{budget:,}**
- 🤖 AI relevance score: **{selected_match_score}%**
- 🛡️ Product trust score: **{selected_trust_score}/100**
- 🏆 Final recommendation score: **{selected_final_score}/100**

**Decision:** ShopWise AI recommends this product based on
both relevance and verified trust signals.
"""
        )


    # -----------------------------------
    # CROSS-SELL RECOMMENDATIONS
    # -----------------------------------

    recommendations = get_recommendations(
        selected_product,
        products
    )


    recommendation_total = 0


    if recommendations:

        st.divider()

        st.header(
            "🤖 You May Also Like"
        )


        st.write(
            "ShopWise AI recommends these "
            "complementary products:"
        )


        recommendation_columns = st.columns(
            len(recommendations)
        )


        for index, product in enumerate(
            recommendations
        ):

            with recommendation_columns[
                index
            ]:

                if product.get(
                    "image"
                ):

                    st.image(
                        product[
                            "image"
                        ],
                        use_container_width=True
                    )


                st.write(
                    f"### {product['name']}"
                )


                st.write(
                    f"💰 ₹{product['price']:,}"
                )


                recommendation_total += (
                    product[
                        "price"
                    ]
                )


    # -----------------------------------
    # REVENUE IMPACT
    # -----------------------------------

    st.divider()

    st.header(
        "📊 Revenue Impact"
    )


    base_price = selected_product[
        "price"
    ]


    additional_revenue = (
        recommendation_total
    )


    maximum_order_value = (
        base_price
        + additional_revenue
    )


    col1, col2, col3 = st.columns(
        3
    )


    col1.metric(
        "Base Product",
        f"₹{base_price:,}"
    )


    col2.metric(
        "Cross-Sell Potential",
        f"₹{additional_revenue:,}"
    )


    col3.metric(
        "Maximum Order Value",
        f"₹{maximum_order_value:,}"
    )


    # -----------------------------------
    # CHECKOUT
    # -----------------------------------

    if not st.session_state[
        "checkout"
    ]:

        if st.button(
            "Proceed to Checkout 🛒",
            use_container_width=True
        ):

            st.session_state[
                "checkout"
            ] = True


            log_action(
                "Checkout Started",
                {
                    "selected_product":
                        selected_product[
                            "name"
                        ],
                    "price":
                        selected_product[
                            "price"
                        ],
                    "potential_cross_sell_revenue":
                        additional_revenue,
                    "final_recommendation_score":
                        selected_final_score
                }
            )


            st.rerun()


# -----------------------------------
# CHECKOUT SUMMARY
# -----------------------------------

if st.session_state[
    "checkout"
]:

    selected_product = st.session_state[
        "selected_product"
    ]


    st.divider()

    st.header(
        "🧾 Checkout Summary"
    )


    col1, col2 = st.columns(
        [1, 2]
    )


    with col1:

        if selected_product.get(
            "image"
        ):

            st.image(
                selected_product[
                    "image"
                ],
                use_container_width=True
            )


    with col2:

        st.subheader(
            selected_product[
                "name"
            ]
        )


        st.write(
            f"💰 Price: "
            f"₹{selected_product['price']:,}"
        )


    recommendations = get_recommendations(
        selected_product,
        products
    )


    recommendation_total = sum(
        product["price"]
        for product in recommendations
    )


    st.subheader(
        "🤖 AI Recommended Add-ons"
    )


    if recommendations:

        recommendation_columns = st.columns(
            len(recommendations)
        )


        for index, product in enumerate(
            recommendations
        ):

            with recommendation_columns[
                index
            ]:

                if product.get(
                    "image"
                ):

                    st.image(
                        product[
                            "image"
                        ],
                        use_container_width=True
                    )


                st.write(
                    f"**{product['name']}**"
                )


                st.write(
                    f"₹{product['price']:,}"
                )


    else:

        st.info(
            "No additional products recommended."
        )


    # TOTAL AMOUNT

    total_amount = (
        selected_product["price"]
        + recommendation_total
    )


    st.divider()


    st.subheader(
        f"💰 Total Potential Order Value: "
        f"₹{total_amount:,}"
    )


    # -----------------------------------
    # USER APPROVAL
    # -----------------------------------

    if not st.session_state[
        "order_confirmed"
    ]:

        st.warning(
            "⚠️ Please review the order "
            "before approving."
        )


        if st.button(
            "✅ Approve and Confirm Order",
            use_container_width=True
        ):

            # ORDER CONFIRMATION

            st.session_state[
                "order_confirmed"
            ] = True


            # SAVE ORDER FOR BLOCKCHAIN PAYMENT

            save_order_for_payment(
                selected_product=selected_product,
                total_amount=total_amount,
                recommendations=recommendations
            )


            # AUDIT LOG

            log_action(
                "Order Approved by User",
                {
                    "product":
                        selected_product[
                            "name"
                        ],
                    "total_amount":
                        total_amount,
                    "payment_status":
                        "Pending Blockchain Payment"
                }
            )


            st.rerun()


# -----------------------------------
# ORDER CONFIRMATION
# -----------------------------------

if st.session_state[
    "order_confirmed"
]:

    st.divider()

    st.success(
        "🎉 Order Approved Successfully!"
    )

    st.balloons()


    st.write(
        "Your ShopWise AI agent received your approval."
    )


    st.info(
        "💳 Your approved order has been prepared "
        "for Blockchain Payment."
    )


    st.success(
        "🔗 Go to the Blockchain Payments page "
        "to complete your payment."
    )