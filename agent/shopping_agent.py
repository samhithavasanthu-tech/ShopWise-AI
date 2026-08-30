# -----------------------------------
# AI INTENT ANALYSIS
# -----------------------------------

def analyze_intent(user_query, budget):

    query = user_query.lower().strip()

    detected_categories = []

    # Laptop intent
    if any(word in query for word in [
        "laptop",
        "coding",
        "programming",
        "developer",
        "computer",
        "software"
    ]):
        detected_categories.append("Laptop")

    # Mouse intent
    if "mouse" in query:
        detected_categories.append("Mouse")

    # Keyboard intent
    if any(word in query for word in [
        "keyboard",
        "typing",
        "mechanical"
    ]):
        detected_categories.append("Keyboard")

    # Bag intent
    if any(word in query for word in [
        "bag",
        "backpack",
        "carry"
    ]):
        detected_categories.append("Bag")

    # Detect use case
    use_case = "General Shopping"

    if any(word in query for word in [
        "coding",
        "programming",
        "developer",
        "software"
    ]):
        use_case = "Programming / Coding"

    elif any(word in query for word in [
        "student",
        "study",
        "college"
    ]):
        use_case = "Student / Education"

    elif any(word in query for word in [
        "typing",
        "writing",
        "write"
    ]):
        use_case = "Typing / Productivity"

    return {
        "categories": detected_categories,
        "use_case": use_case,
        "budget": budget
    }


# -----------------------------------
# PRODUCT SEARCH + MATCH SCORE
# -----------------------------------

def find_products(products, user_query, budget):

    query = user_query.lower().strip()

    intent = analyze_intent(user_query, budget)

    detected_categories = [
        category.lower()
        for category in intent["categories"]
    ]

    matching_products = []


    for product in products:

        name = product["name"].lower()
        category = product["category"].lower()
        description = product["description"].lower()
        price = product["price"]


        # Budget filter
        if price > budget:
            continue


        score = 0


        # -----------------------------------
        # PRODUCT INTENT MATCH
        # -----------------------------------

        if "laptop" in detected_categories and category == "laptop":
            score += 70

        if "mouse" in detected_categories and "mouse" in name:
            score += 70

        if "keyboard" in detected_categories and "keyboard" in name:
            score += 70

        if "bag" in detected_categories and (
            "bag" in name or "backpack" in name
        ):
            score += 70


        # -----------------------------------
        # QUERY KEYWORD MATCH
        # -----------------------------------

        important_words = [
            "laptop",
            "coding",
            "programming",
            "student",
            "developer",
            "mouse",
            "keyboard",
            "typing",
            "bag",
            "backpack"
        ]

        for word in important_words:

            if word in query:

                if word in name:
                    score += 10

                if word in description:
                    score += 5


        # -----------------------------------
        # BUDGET MATCH
        # -----------------------------------

        if price <= budget * 0.90:
            score += 10
        else:
            score += 5


        # Keep score maximum at 100
        match_score = min(score, 100)


        # Only include relevant products
        if match_score >= 50:

            product_copy = product.copy()

            product_copy["match_score"] = match_score

            matching_products.append(product_copy)


    # -----------------------------------
    # FALLBACK
    # -----------------------------------

    if not matching_products:

        for product in products:

            if product["price"] <= budget:

                product_copy = product.copy()

                product_copy["match_score"] = 50

                matching_products.append(product_copy)


    # Best score first
    matching_products.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matching_products