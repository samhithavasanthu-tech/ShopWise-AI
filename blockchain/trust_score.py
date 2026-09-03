import json
import os


# -------------------------------------------------
# PROJECT ROOT
# -------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# -------------------------------------------------
# DATA FILES
# -------------------------------------------------

REVIEWS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "reviews.json"
)

PAYMENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "blockchain_payments.json"
)


# -------------------------------------------------
# LOAD JSON DATA
# -------------------------------------------------

def load_json(file_path):
    """Load JSON data safely."""

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
        FileNotFoundError,
        json.JSONDecodeError
    ):

        return []


# -------------------------------------------------
# GET PRODUCT REVIEWS
# -------------------------------------------------

def get_product_reviews(product_id):
    """Get verified reviews for a product."""

    reviews = load_json(
        REVIEWS_FILE
    )

    return [

        review

        for review in reviews

        if review.get("product_id") == product_id
        and review.get(
            "verified_purchase",
            False
        )

    ]


# -------------------------------------------------
# GET VERIFIED PURCHASES
# -------------------------------------------------

def get_verified_purchases(product_id):
    """Get confirmed blockchain purchases for a product."""

    payments = load_json(
        PAYMENTS_FILE
    )

    return [

        payment

        for payment in payments

        if payment.get("product_id") == product_id
        and payment.get("status") == "confirmed"

    ]


# -------------------------------------------------
# CALCULATE TRUST SCORE
# -------------------------------------------------

def calculate_trust_score(product_id):
    """
    Calculate Product Trust Score out of 100.

    Rating Score:
    Maximum 60 points

    Review Score:
    Maximum 20 points

    Purchase Verification Score:
    Maximum 20 points
    """

    reviews = get_product_reviews(
        product_id
    )

    purchases = get_verified_purchases(
        product_id
    )


    # ---------------------------------------------
    # RATING SCORE (MAX 60)
    # ---------------------------------------------

    if reviews:

        average_rating = sum(

            review.get(
                "rating",
                0
            )

            for review in reviews

        ) / len(reviews)


        rating_score = (
            average_rating / 5
        ) * 60

    else:

        average_rating = 0
        rating_score = 0


    # ---------------------------------------------
    # REVIEW SCORE (MAX 20)
    # ---------------------------------------------

    # 10 verified reviews = maximum score

    review_score = min(

        len(reviews) * 2,

        20

    )


    # ---------------------------------------------
    # PURCHASE SCORE (MAX 20)
    # ---------------------------------------------

    # 10 verified purchases = maximum score

    purchase_score = min(

        len(purchases) * 2,

        20

    )


    # ---------------------------------------------
    # FINAL SCORE
    # ---------------------------------------------

    trust_score = round(

        rating_score
        + review_score
        + purchase_score

    )


    return {

        "product_id": product_id,

        "trust_score": trust_score,

        "average_rating": round(
            average_rating,
            1
        ),

        "verified_reviews": len(
            reviews
        ),

        "verified_purchases": len(
            purchases
        ),

        "rating_score": round(
            rating_score,
            1
        ),

        "review_score": review_score,

        "purchase_score": purchase_score

    }