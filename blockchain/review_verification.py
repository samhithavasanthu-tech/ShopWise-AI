import json
import os
import uuid
from datetime import datetime

from blockchain.payment_service import has_verified_purchase


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

REVIEWS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "reviews.json"
)


def load_reviews():
    """Load all product reviews."""

    if not os.path.exists(REVIEWS_FILE):
        return []

    try:
        with open(
            REVIEWS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_reviews(reviews):
    """Save reviews to JSON."""

    os.makedirs(
        os.path.dirname(REVIEWS_FILE),
        exist_ok=True
    )

    with open(
        REVIEWS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            reviews,
            file,
            indent=4,
            ensure_ascii=False
        )


def submit_review(
    product_id,
    wallet_address,
    rating,
    review_text
):
    """
    Submit a review only if the wallet
    has a verified purchase.
    """

    verified_purchase = has_verified_purchase(
        product_id,
        wallet_address
    )

    if not verified_purchase:

        return {
            "success": False,
            "message": (
                "Review rejected. "
                "No verified purchase found for this wallet."
            ),
            "review": None
        }

    reviews = load_reviews()

    review = {
        "review_id": str(uuid.uuid4()),
        "product_id": product_id,
        "wallet_address": wallet_address,
        "rating": rating,
        "review": review_text,
        "verified_purchase": True,
        "verification_method": (
            "ShopWise Blockchain Payment Verification"
        ),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    reviews.append(review)

    save_reviews(reviews)

    return {
        "success": True,
        "message": (
            "Review submitted successfully "
            "as a Verified Purchase."
        ),
        "review": review
    }


def get_reviews_by_product(product_id):
    """Return all reviews for a product."""

    reviews = load_reviews()

    return [
        review
        for review in reviews
        if review["product_id"] == product_id
    ]


def get_all_reviews():
    """Return all reviews."""

    return load_reviews()


def calculate_average_rating(product_id):
    """Calculate average rating for a product."""

    reviews = get_reviews_by_product(
        product_id
    )

    if not reviews:
        return 0

    total_rating = sum(
        review["rating"]
        for review in reviews
    )

    return round(
        total_rating / len(reviews),
        1
    )