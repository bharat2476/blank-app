import random

import numpy as np
import pandas as pd

from seed_data import build_product_catalog, get_user_registry

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_users(n=100):
    return get_user_registry(n)


def generate_sellers(n=12):
    categories = ["Running", "Basketball", "Training", "Soccer", "Lifestyle", "Trail"]

    sellers = []
    for i in range(n):
        sellers.append({
            "seller_id": i,
            "name": f"Marketplace Channel {i}",
            "category_focus": random.choice(categories),
            "rating": round(random.uniform(3.0, 5.0), 2),
            "historical_revenue": random.randint(5000, 500000),
            "is_small_seller": random.choice([True, False]),
        })

    return pd.DataFrame(sellers)


def generate_products(sellers_df, n=500):
    return build_product_catalog(sellers_df, target_n=n)


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
            "target_audience": product["audience"],
            "target_product_type": product["product_type"],
        })

    return pd.DataFrame(bids)


def initialize_marketplace(user_count=100, product_count=500, bid_count=200):
    """Load sellers, registry-backed catalog, members, and bids for the simulator."""
    sellers = generate_sellers()
    products = generate_products(sellers, n=product_count)
    users = generate_users(user_count)
    bids = generate_bids(products, sellers, n=bid_count)
    return {
        "users": users,
        "sellers": sellers,
        "products": products,
        "bids": bids,
    }
