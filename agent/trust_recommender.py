from blockchain.trust_score import (
    calculate_trust_score
)


def calculate_final_score(
    ai_match_score,
    trust_score
):
    """
    Combine AI relevance and Product Trust.

    AI Match Score = 70% weight
    Trust Score = 30% weight
    """

    final_score = (
        ai_match_score * 0.7
        + trust_score * 0.3
    )

    return round(
        final_score,
        2
    )


def rank_products_by_trust(products):
    """
    Add trust information and final recommendation
    score to each product, then rank products.
    """

    ranked_products = []


    for product in products:

        # -----------------------------------------
        # AI MATCH SCORE
        # -----------------------------------------

        ai_match_score = product.get(
            "match_score",
            0
        )


        # -----------------------------------------
        # PRODUCT TRUST SCORE
        # -----------------------------------------

        trust_data = calculate_trust_score(
            product["id"]
        )

        trust_score = trust_data[
            "trust_score"
        ]


        # -----------------------------------------
        # FINAL RECOMMENDATION SCORE
        # -----------------------------------------

        final_score = calculate_final_score(
            ai_match_score,
            trust_score
        )


        # -----------------------------------------
        # CREATE UPDATED PRODUCT
        # -----------------------------------------

        ranked_product = product.copy()

        ranked_product[
            "trust_score"
        ] = trust_score

        ranked_product[
            "final_score"
        ] = final_score

        ranked_product[
            "trust_data"
        ] = trust_data


        ranked_products.append(
            ranked_product
        )


    # ---------------------------------------------
    # SORT PRODUCTS
    # ---------------------------------------------

    ranked_products.sort(
        key=lambda product:
            product["final_score"],
        reverse=True
    )


    return ranked_products