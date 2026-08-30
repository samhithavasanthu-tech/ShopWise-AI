import streamlit as st
import json

from agent.shopping_agent import find_products, analyze_intent
from utils.recommender import get_recommendations
from utils.audit_logger import log_action


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

with open("data/products.json", "r") as file:
    products = json.load(file)


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

st.title("🛍️ ShopWise AI")
st.subheader("AI Product Discovery & Agentic Shopping")

st.write(
    "Find the right products based on your needs and budget."
)


# -----------------------------------
# USER INPUT
# -----------------------------------

st.header("🔍 Find Your Product")

user_query = st.text_input(
    "What are you looking for?",
    placeholder="Example: I am a student and need a laptop for coding"
)

budget = st.number_input(
    "Enter your maximum budget (₹)",
    min_value=0,
    value=60000
)


# -----------------------------------
# SEARCH PRODUCTS
# -----------------------------------

if st.button("🔍 Find Products"):

    st.session_state["ai_intent"] = analyze_intent(
        user_query,
        budget
    )

    st.session_state["results"] = find_products(
        products,
        user_query,
        budget
    )

    log_action(
        "Product Search",
        {
            "user_query": user_query,
            "budget": budget,
            "results_found": len(
                st.session_state["results"]
            )
        }
    )

    st.session_state["selected_product"] = None
    st.session_state["checkout"] = False
    st.session_state["order_confirmed"] = False


# -----------------------------------
# AI INTENT DETECTED
# -----------------------------------

if st.session_state["ai_intent"] is not None:

    intent = st.session_state["ai_intent"]

    st.divider()

    st.header("🧠 AI Intent Detected")

    categories = intent["categories"]

    if categories:
        category_text = ", ".join(categories)
    else:
        category_text = "General Product Search"

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎯 Product Intent",
        category_text
    )

    col2.metric(
        "💡 Use Case",
        intent["use_case"]
    )

    col3.metric(
        "💰 Budget",
        f"₹{intent['budget']}"
    )

    st.info(
        "🤖 ShopWise AI analyzed your request and ranked products based on your intent and budget."
    )


# -----------------------------------
# SEARCH RESULTS WITH IMAGES
# -----------------------------------

if st.session_state["results"]:

    st.divider()

    st.success(
        "🤖 ShopWise AI found the best products for your request!"
    )

    for product in st.session_state["results"]:

        col1, col2 = st.columns([1, 2])

        # Product Image
        with col1:

            if "image" in product:

                st.image(
                    product["image"],
                    use_container_width=True
                )


        # Product Information
        with col2:

            st.subheader(
                product["name"]
            )

            st.write(
                product["description"]
            )

            st.write(
                f"💰 **Price: ₹{product['price']}**"
            )

            # AI Match Score
            match_score = product.get(
                "match_score",
                0
            )

            st.progress(
                match_score
            )

            st.write(
                f"🤖 **AI Match Score: {match_score}%**"
            )


            # Select Product Button
            if st.button(
                f"🛒 Select {product['name']}",
                key=f"select_{product['id']}"
            ):

                st.session_state["selected_product"] = product

                st.session_state["checkout"] = False

                st.session_state["order_confirmed"] = False


                log_action(
                    "Product Selected",
                    {
                        "product_name": product["name"],
                        "price": product["price"],
                        "category": product["category"],
                        "match_score": match_score
                    }
                )

                st.rerun()


        st.divider()


# -----------------------------------
# SELECTED PRODUCT
# -----------------------------------

if st.session_state["selected_product"] is not None:

    selected_product = st.session_state[
        "selected_product"
    ]

    st.header(
        "🛒 Your Selected Product"
    )

    col1, col2 = st.columns([1, 2])


    # Selected Product Image
    with col1:

        if "image" in selected_product:

            st.image(
                selected_product["image"],
                use_container_width=True
            )


    # Product Details
    with col2:

        st.subheader(
            selected_product["name"]
        )

        st.write(
            selected_product["description"]
        )

        st.write(
            f"💰 **Price: ₹{selected_product['price']}**"
        )

        st.subheader(
            "🧠 Why ShopWise AI Recommended This"
        )

        st.write(
            f"""
            **AI Decision:**

            - Matches your detected product intent
            - Product category: **{selected_product['category']}**
            - Price is within your budget of **₹{budget}**
            - Product is ranked based on relevance

            **Decision:** Recommended as a suitable product.
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
            "🤖 You may also like"
        )

        st.write(
            "ShopWise AI recommends these complementary products:"
        )


        # Show recommendation cards
        recommendation_columns = st.columns(
            len(recommendations)
        )


        for index, product in enumerate(
            recommendations
        ):

            with recommendation_columns[index]:

                if "image" in product:

                    st.image(
                        product["image"],
                        use_container_width=True
                    )

                st.write(
                    f"### {product['name']}"
                )

                st.write(
                    f"💰 ₹{product['price']}"
                )

                recommendation_total += product["price"]


    # -----------------------------------
    # REVENUE IMPACT
    # -----------------------------------

    st.divider()

    st.header(
        "📊 Revenue Impact"
    )


    base_price = selected_product["price"]

    additional_revenue = recommendation_total

    maximum_order_value = (
        base_price + additional_revenue
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Base Product",
        f"₹{base_price}"
    )


    col2.metric(
        "Cross-Sell Potential",
        f"₹{additional_revenue}"
    )


    col3.metric(
        "Maximum Order Value",
        f"₹{maximum_order_value}"
    )


    # -----------------------------------
    # CHECKOUT
    # -----------------------------------

    if not st.session_state["checkout"]:

        if st.button(
            "Proceed to Checkout 🛒"
        ):

            st.session_state["checkout"] = True


            log_action(
                "Checkout Started",
                {
                    "selected_product": selected_product["name"],
                    "price": selected_product["price"],
                    "potential_cross_sell_revenue": additional_revenue
                }
            )

            st.rerun()


# -----------------------------------
# CHECKOUT SUMMARY
# -----------------------------------

if st.session_state["checkout"]:

    selected_product = st.session_state[
        "selected_product"
    ]

    st.divider()

    st.header(
        "🧾 Checkout Summary"
    )


    col1, col2 = st.columns([1, 2])

    with col1:

        if "image" in selected_product:

            st.image(
                selected_product["image"],
                use_container_width=True
            )


    with col2:

        st.subheader(
            selected_product["name"]
        )

        st.write(
            f"💰 Price: ₹{selected_product['price']}"
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

            with recommendation_columns[index]:

                if "image" in product:

                    st.image(
                        product["image"],
                        use_container_width=True
                    )

                st.write(
                    f"**{product['name']}**"
                )

                st.write(
                    f"₹{product['price']}"
                )

    else:

        st.write(
            "No additional products recommended."
        )


    total_amount = (
        selected_product["price"]
        + recommendation_total
    )


    st.divider()


    st.subheader(
        f"Total Potential Order Value: ₹{total_amount}"
    )


    # -----------------------------------
    # USER APPROVAL
    # -----------------------------------

    if not st.session_state["order_confirmed"]:

        st.warning(
            "⚠️ Please review the order before approving."
        )


        if st.button(
            "✅ Approve and Confirm Order"
        ):

            st.session_state["order_confirmed"] = True


            log_action(
                "Order Approved by User",
                {
                    "product": selected_product["name"],
                    "total_amount": total_amount
                }
            )

            st.rerun()


# -----------------------------------
# ORDER CONFIRMATION
# -----------------------------------

if st.session_state["order_confirmed"]:

    st.success(
        "🎉 Order Approved Successfully!"
    )

    st.balloons()

    st.write(
        "Your ShopWise AI agent received your approval. "
        "The order is ready for payment processing."
    )