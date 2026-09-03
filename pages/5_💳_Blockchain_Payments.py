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
# IMPORT BLOCKCHAIN PAYMENT FUNCTIONS
# -------------------------------------------------

from blockchain.payment_service import (
    create_payment,
    verify_payment,
    get_payments_by_wallet
)

from utils.payment_handoff import (
    get_pending_payment_order,
    clear_pending_payment_order
)

from utils.audit_logger import (
    log_action
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Blockchain Payments | ShopWise AI",
    page_icon="💳",
    layout="wide"
)


# -------------------------------------------------
# PAGE TITLE
# -------------------------------------------------

st.title("💳 Blockchain Payments")

st.write(
    "Complete your approved ShopWise AI order using "
    "the blockchain-inspired payment system."
)

st.divider()


# -------------------------------------------------
# GET APPROVED ORDER
# -------------------------------------------------

pending_order = get_pending_payment_order()


# -------------------------------------------------
# SHOW APPROVED ORDER
# -------------------------------------------------

if pending_order:

    st.success(
        "🛒 Approved order detected from ShopWise AI!"
    )

    st.subheader(
        "📦 Your Approved Order"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Product",
            pending_order.get(
                "product_name",
                "Unknown"
            )
        )

    with col2:

        st.metric(
            "Product Price",
            f"₹{pending_order.get('product_price', 0):,}"
        )

    with col3:

        st.metric(
            "Total Order Amount",
            f"₹{pending_order.get('total_amount', 0):,}"
        )


    # -------------------------------------------------
    # ADD-ONS
    # -------------------------------------------------

    recommendations = pending_order.get(
        "recommendations",
        []
    )


    if recommendations:

        st.markdown(
            "### 🤖 AI Recommended Add-ons"
        )

        for product in recommendations:

            st.write(
                f"• {product.get('name', 'Product')} "
                f"— ₹{product.get('price', 0):,}"
            )


    st.info(
        "This order was prepared automatically "
        "after your approval on the Shop page."
    )


else:

    st.warning(
        "⚠️ No approved order found."
    )

    st.info(
        "Go to the 🛍️ Shop page, select a product, "
        "complete checkout, and approve the order first."
    )


st.divider()


# -------------------------------------------------
# WALLET ADDRESS
# -------------------------------------------------

st.subheader(
    "👛 Step 1: Enter Wallet Address"
)

wallet_address = st.text_input(
    "Wallet Address",
    placeholder="Example: 0x123456789abcdef"
)

st.caption(
    "For this project demo, you can enter "
    "any sample wallet address."
)


# -------------------------------------------------
# PAYMENT CREATION
# -------------------------------------------------

st.divider()

st.subheader(
    "💳 Step 2: Create Blockchain Payment"
)


if pending_order:

    if st.button(
        "🔗 Pay Approved Order",
        use_container_width=True
    ):

        if not wallet_address.strip():

            st.warning(
                "Please enter a wallet address first."
            )

        else:

            # -----------------------------------------
            # CREATE PRODUCT OBJECT
            # -----------------------------------------

            payment_product = {
                "id": pending_order.get(
                    "product_id"
                ),
                "name": pending_order.get(
                    "product_name"
                ),
                "price": pending_order.get(
                    "total_amount",
                    0
                )
            }


            # -----------------------------------------
            # CREATE PAYMENT
            # -----------------------------------------

            payment = create_payment(
                product=payment_product,
                wallet_address=wallet_address.strip()
            )


            # -----------------------------------------
            # UPDATE SESSION STATE
            # -----------------------------------------

            st.session_state[
                "latest_blockchain_payment"
            ] = payment


            # -----------------------------------------
            # AUDIT LOG
            # -----------------------------------------

            log_action(
                "Blockchain Payment Created",
                {
                    "product":
                        pending_order.get(
                            "product_name"
                        ),
                    "amount":
                        pending_order.get(
                            "total_amount"
                        ),
                    "wallet":
                        wallet_address.strip(),
                    "transaction_hash":
                        payment.get(
                            "transaction_hash"
                        )
                }
            )


            # -----------------------------------------
            # CLEAR PENDING ORDER
            # -----------------------------------------

            clear_pending_payment_order()


            st.success(
                "🎉 Blockchain Payment Created Successfully!"
            )

            st.balloons()

            st.rerun()


else:

    st.info(
        "Payment creation will unlock when an "
        "approved order is available."
    )


# -------------------------------------------------
# PAYMENT CONFIRMATION
# -------------------------------------------------

if (
    "latest_blockchain_payment"
    in st.session_state
):

    payment = st.session_state[
        "latest_blockchain_payment"
    ]

    st.divider()

    st.subheader(
        "✅ Payment Confirmation"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"""
**Product:** {payment.get('product_name', 'Unknown')}

**Amount:** ₹{payment.get('amount', 0):,}

**Status:** {payment.get('status', 'Unknown').upper()}

**Network:** {payment.get('network', 'Demo Network')}
"""
        )

    with col2:

        st.markdown(
            "### 🔗 Transaction Hash"
        )

        st.code(
            payment.get(
                "transaction_hash",
                "Not Available"
            ),
            language=None
        )
        st.success(
    "🎉 Your purchase is verified and you are now eligible "
    "to submit a verified product review."
)

st.info(
    "⭐ Next step: Go to the Verified Reviews page and use "
    "the same wallet address to review your purchased product."
)


# -------------------------------------------------
# VERIFY PAYMENT
# -------------------------------------------------

st.divider()

st.subheader(
    "🔍 Step 3: Verify Payment"
)


transaction_hash = st.text_input(
    "Enter Transaction Hash",
    placeholder="Paste transaction hash here"
)


if st.button(
    "Verify Transaction",
    use_container_width=True
):

    if not transaction_hash.strip():

        st.warning(
            "Please enter a transaction hash."
        )

    else:

        result = verify_payment(
            transaction_hash.strip()
        )

        if result.get("verified"):

            st.success(
                "✅ Payment Verified Successfully!"
            )

            st.json(
                result.get("payment")
            )

        else:

            st.error(
                "❌ Payment not found."
            )


# -------------------------------------------------
# WALLET PAYMENT HISTORY
# -------------------------------------------------

st.divider()

st.subheader(
    "📜 Step 4: Wallet Payment History"
)


if wallet_address.strip():

    payments = get_payments_by_wallet(
        wallet_address.strip()
    )

    if payments:

        st.success(
            f"Found {len(payments)} payment(s)."
        )

        for payment in reversed(payments):

            with st.expander(
                f"{payment.get('product_name', 'Product')} "
                f"— ₹{payment.get('amount', 0):,}"
            ):

                st.write(
                    f"**Status:** "
                    f"{payment.get('status', 'Unknown')}"
                )

                st.write(
                    f"**Network:** "
                    f"{payment.get('network', 'Demo Network')}"
                )

                st.write(
                    f"**Timestamp:** "
                    f"{payment.get('timestamp', 'Unknown')}"
                )

                st.code(
                    payment.get(
                        "transaction_hash",
                        "Not Available"
                    ),
                    language=None
                )

    else:

        st.info(
            "No payments found for this wallet."
        )


else:

    st.info(
        "Enter a wallet address above to view "
        "payment history."
    )


# -------------------------------------------------
# INFORMATION
# -------------------------------------------------

st.divider()

st.caption(
    "⚠️ Phase 1 Demo: This module simulates a "
    "blockchain-inspired payment workflow. No real "
    "cryptocurrency or blockchain transaction occurs."
)