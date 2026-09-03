import streamlit as st


# -------------------------------------------------
# SAVE ORDER FOR BLOCKCHAIN PAYMENT
# -------------------------------------------------

def save_order_for_payment(
    selected_product,
    total_amount,
    recommendations=None
):
    """
    Save the approved order in Streamlit session state.

    The Blockchain Payments page can later read this
    information and automatically prepare the payment.
    """

    if recommendations is None:
        recommendations = []


    payment_order = {

        # Main product
        "product_id": selected_product.get(
            "id"
        ),

        "product_name": selected_product.get(
            "name"
        ),

        "product_price": selected_product.get(
            "price",
            0
        ),


        # Order information
        "total_amount": total_amount,


        # Recommended add-ons
        "recommendations": recommendations,


        # Payment status
        "payment_status": "pending"

    }


    # Save order in session state

    st.session_state[
        "pending_payment_order"
    ] = payment_order


# -------------------------------------------------
# GET PENDING PAYMENT ORDER
# -------------------------------------------------

def get_pending_payment_order():
    """
    Get the order waiting for blockchain payment.
    """

    return st.session_state.get(
        "pending_payment_order",
        None
    )


# -------------------------------------------------
# CLEAR PAYMENT ORDER
# -------------------------------------------------

def clear_pending_payment_order():
    """
    Remove the pending order after payment.
    """

    if (
        "pending_payment_order"
        in st.session_state
    ):

        del st.session_state[
            "pending_payment_order"
        ]