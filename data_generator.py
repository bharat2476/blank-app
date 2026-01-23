import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# USER GENERATION
# -----------------------------

def generate_users(n=200):
    segments = {
        "Runner": ["running", "fitness", "outdoor"],
        "Sneakerhead": ["sneakers", "streetwear", "fashion"],
        "Tech Buyer": ["electronics", "gadgets", "computers"],
        "Outdoor Enthusiast": ["camping", "hiking", "outdoor"]
    }

    users = []
    for i in range(n):
        segment = random.choice(list(segments.keys()))
        interests = random.sample(segments[segment], 2)

        users.append({
            "user_id": i,
            "segment": segment,
            "interests": interests,
            "age": random.randint(18, 60),
            "location": random.choice(["NY", "CA", "TX", "WA", "FL"])
        })

    return pd.DataFrame(users)


# -----------------------------
# SELLER GENERATION
# -----------------------------

def generate_sellers(n=40):
    categories = ["running", "fitness", "outdoor", "sneakers", "fashion", "electronics"]

    sellers = []
    for i in range(n):
        sellers.append({
            "seller_id": i,
            "name": f"Seller {i}",
            "category_focus": random.choice(categories),
            "rating": round(random.uniform(3.0, 5.0), 2),
            "historical_revenue": random.randint(5000, 500000),
            "is_small_seller": random.choice([True, False])
        })

    return pd.DataFrame(sellers)


# -----------------------------
# PRODUCT GENERATION
# -----------------------------

def generate_products(sellers_df, n=300):
    categories = ["running", "fitness", "outdoor", "sneakers", "fashion", "electronics"]

    products = []
    for i in range(n):
        seller = sellers_df.sample(1).iloc[0]

        products.append({
            "product_id": i,
            "seller_id": seller["seller_id"],
            "name": f"Product {i}",
            "category": seller["category_focus"],
            "price": round(random.uniform(20, 300), 2),
            "popularity_score": random.randint(1, 100),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        })

    return pd.DataFrame(products)


# -----------------------------
# BID GENERATION (ADS)
# -----------------------------

def generate_bids(products_df, sellers_df, n=200):
    bids = []
    for i in range(n):
        product = products_df.sample(1).iloc[0]
        seller = sellers_df[sellers_df["seller_id"] == product["seller_id"]].iloc[0]

        bids.append({
            "bid_id": i,
            "seller_id": seller["seller_id"],
            "product_id": product["product_id"],
            "bid_amount": round(random.uniform(0.5, 5.0), 2),
            "target_category": product["category"],
            "target_interest": product["category"]
        })

    return pd.DataFrame(bids)
