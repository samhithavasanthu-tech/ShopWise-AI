import streamlit as st


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="ShopWise AI",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------------
# HOME PAGE
# -----------------------------------

st.title("🤖 Welcome to ShopWise AI")

st.subheader("Your Agentic Commerce & Revenue Growth Assistant")


st.write(
    """
    ShopWise AI is an AI-powered commerce assistant that helps users
    discover products, receive intelligent recommendations, and make
    transparent purchasing decisions.
    """
)


st.divider()


# -----------------------------------
# HOW IT WORKS
# -----------------------------------

st.header("🚀 How ShopWise AI Works")

st.write(
    """
    🔍 **1. Product Discovery**  
    Search for products based on your requirements and budget.

    🤖 **2. AI Recommendation**  
    ShopWise AI identifies suitable products.

    🧠 **3. AI Decision Explanation**  
    The system explains why a product was recommended.

    🛍️ **4. Cross-Selling**  
    AI recommends useful additional products.

    📊 **5. Revenue Impact**  
    The system calculates potential additional revenue.

    🧾 **6. Checkout & Approval**  
    The user reviews and approves the order.

    📜 **7. Audit Trail**  
    Important AI and user actions are recorded.
    """
)


st.divider()


# -----------------------------------
# PROJECT FEATURES
# -----------------------------------

st.header("✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("🤖 AI Agent")

    st.write(
        "Smart product discovery based on user requirements."
    )


with col2:

    st.subheader("📈 Revenue Growth")

    st.write(
        "Cross-selling recommendations to increase order value."
    )


with col3:

    st.subheader("🔒 Transparent AI")

    st.write(
        "User approval and audit logging for trustworthy decisions."
    )


st.divider()


# -----------------------------------
# GET STARTED
# -----------------------------------

st.header("🛍️ Ready to Start?")

st.info(
    "Select **🛍️ Shop** from the sidebar to start your AI-powered shopping experience."
)
st.divider()

st.caption(
    "🤖 ShopWise AI | Agentic Commerce & Revenue Growth Assistant"
)

st.caption(
    "Built for AI Builder Internship / Buildathon Project"
)
