def get_recommendations(selected_product, products):
    
    recommendations = []

    # Recommend accessories when a laptop is selected
    if selected_product["category"] == "Laptop":

        for product in products:

            if (
                product["category"] == "Accessory"
                and product["stock"] == True
            ):
                recommendations.append(product)

    return recommendations
