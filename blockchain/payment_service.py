import json
import os
import hashlib
from datetime import datetime
import uuid


PAYMENTS_FILE = "data/blockchain_payments.json"


def load_payments():
    """
    Load all blockchain payment records.
    """

    if not os.path.exists(PAYMENTS_FILE):
        return []

    try:
        with open(PAYMENTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_payments(payments):
    """
    Save blockchain payment records.
    """

    os.makedirs("data", exist_ok=True)

    with open(PAYMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(payments, file, indent=4)


def generate_transaction_hash(
    product_id,
    wallet_address,
    amount
):
    """
    Generate a simulated blockchain transaction hash.

    This is used for Phase 1 demonstration.
    It does NOT represent a real blockchain transaction.
    """

    unique_data = (
        f"{product_id}"
        f"{wallet_address}"
        f"{amount}"
        f"{datetime.now().isoformat()}"
        f"{uuid.uuid4()}"
    )

    transaction_hash = hashlib.sha256(
        unique_data.encode()
    ).hexdigest()

    return "0x" + transaction_hash


def create_payment(
    product,
    wallet_address
):
    """
    Create a simulated blockchain payment.
    """

    payments = load_payments()

    transaction_hash = generate_transaction_hash(
        product_id=product["id"],
        wallet_address=wallet_address,
        amount=product["price"]
    )

    payment = {
        "payment_id": str(uuid.uuid4()),
        "product_id": product["id"],
        "product_name": product["name"],
        "amount": product["price"],
        "wallet_address": wallet_address,
        "transaction_hash": transaction_hash,
        "network": "ShopWise Test Blockchain",
        "status": "confirmed",
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    payments.append(payment)

    save_payments(payments)

    return payment


def verify_payment(
    transaction_hash
):
    """
    Verify whether a payment exists and is confirmed.
    """

    payments = load_payments()

    for payment in payments:

        if (
            payment["transaction_hash"]
            == transaction_hash
        ):

            return {
                "verified": True,
                "payment": payment
            }

    return {
        "verified": False,
        "payment": None
    }


def get_payments():
    """
    Return all payment records.
    """

    return load_payments()


def get_payments_by_wallet(
    wallet_address
):
    """
    Return all payments made by a wallet.
    """

    payments = load_payments()

    wallet_address = wallet_address.lower()

    user_payments = []

    for payment in payments:

        if (
            payment["wallet_address"].lower()
            == wallet_address
        ):

            user_payments.append(payment)

    return user_payments


def has_verified_purchase(
    product_id,
    wallet_address
):
    """
    Check whether a wallet has a verified purchase
    for a specific product.

    This function will later be used for
    verifiable product reviews.
    """

    payments = get_payments_by_wallet(
        wallet_address
    )

    for payment in payments:

        if (
            payment["product_id"] == product_id
            and payment["status"] == "confirmed"
        ):

            return True

    return False
