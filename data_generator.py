import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# -----------------------------
# USER GENERATION
# -----------------------------

def generate_users(n=100):
    segments = {
        "Performance Runner": ["Running", "Training", "Trail"],
        "Sneaker Culture": ["Lifestyle", "Basketball", "Skateboarding"],
        "Team Sports Athlete": ["Soccer", "Basketball", "Training"],
        "Wellness & Studio": ["Yoga", "Training", "Running"],
        "Outdoor Explorer": ["Trail", "Golf", "Running"],
    }
    apps = ["Nike Run Club", "Nike Training Club", "SNKRS", "Nike App"]
    genders = ["Men", "Women"]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    locations = ["NY", "CA", "TX", "WA", "FL", "IL", "GA", "OR"]

    users = []
    for i in range(n):
        segment = random.choice(list(segments.keys()))
        interests = random.sample(segments[segment], 2)
        customer_type = "Repeat" if i < int(n * 0.62) else "New"
        app_signals = random.sample(apps, random.randint(1, 3))
        run_frequency_per_week = random.choice([0, 1, 2, 3, 4, 5])
        estimated_monthly_miles = run_frequency_per_week * random.randint(8, 24)
        last_shoe_purchase_days_ago = (
            random.choice([7, 21, 45, 120, 168, 181, 230])
            if customer_type == "Repeat"
            else None
        )
        email_opt_in = random.choice([True, True, True, False])
        if customer_type == "New":
            lifecycle_stage = random.choice(["New Visitor", "First Purchase Prospect"])
        elif last_shoe_purchase_days_ago and last_shoe_purchase_days_ago >= 230:
            lifecycle_stage = "Lapsed Runner"
        elif random.random() < 0.22:
            lifecycle_stage = "High-Value Member"
        else:
            lifecycle_stage = random.choice(["Repeat Runner", "Active Member"])

        users.append({
            "user_id": i,
            "customer_name": f"Nike Member {i:03d}",
            "gender": random.choice(genders),
            "age_group": random.choice(age_groups),
            "location": random.choice(locations),
            "customer_type": customer_type,
            "lifecycle_stage": lifecycle_stage,
            "segment": segment,
            "interests": interests,
            "browser_signal": random.choice(interests + ["Sale", "Trending"]),
            "app_signals": app_signals,
            "run_frequency_per_week": run_frequency_per_week,
            "estimated_monthly_miles": estimated_monthly_miles,
            "last_purchase_category": random.choice(["Footwear", "Apparel", "Accessories"]),
            "last_shoe_purchase_days_ago": last_shoe_purchase_days_ago,
            "avg_order_value": random.randint(65, 240),
            "email_opt_in": email_opt_in,
            "consent_app_usage": random.choice([True, True, True, False]),
            "consent_marketing": email_opt_in and random.choice([True, True, True, False]),
            "channel_preference": random.choice(["Email", "Push", "In-app", "Email + Push"]),
            "emails_sent_last_7_days": random.randint(0, 5),
            "email_frequency_cap_per_week": random.choice([2, 3, 4]),
        })

    return pd.DataFrame(users)


# -----------------------------
# SELLER GENERATION
# -----------------------------

def generate_sellers(n=12):
    categories = ["Running", "Basketball", "Training", "Soccer", "Lifestyle", "Trail"]

    sellers = []
    for i in range(n):
        sellers.append({
            "seller_id": i,
            "name": f"Nike Channel {i}",
            "category_focus": random.choice(categories),
            "rating": round(random.uniform(3.0, 5.0), 2),
            "historical_revenue": random.randint(5000, 500000),
            "is_small_seller": random.choice([True, False])
        })

    return pd.DataFrame(sellers)


# -----------------------------
# PRODUCT GENERATION
# -----------------------------

def generate_products(sellers_df, n=500):
    sport_categories = [
        "Running", "Basketball", "Training", "Soccer", "Tennis",
        "Yoga", "Skateboarding", "Lifestyle", "Golf", "Trail"
    ]
    audiences = ["Men", "Women", "Kids"]
    product_types = ["Footwear", "Apparel", "Accessories"]
    product_names = {
        "Footwear": ["Pegasus", "Vomero", "Metcon", "Mercurial", "Dunk", "Air Max"],
        "Apparel": ["Dri-FIT Tee", "Therma Hoodie", "Pro Tight", "Club Fleece", "AeroSwift Short"],
        "Accessories": ["Elite Socks", "Heritage Bag", "Club Cap", "Hydration Belt"],
    }

    products = []
    for i in range(n):
        seller = sellers_df.sample(1).iloc[0]
        product_type = random.choice(product_types)
        is_on_sale = random.random() < 0.28

        products.append({
            "product_id": i,
            "seller_id": seller["seller_id"],
            "name": f"Nike {random.choice(product_names[product_type])} {i:03d}",
            "category": random.choice(sport_categories),
            "audience": random.choice(audiences),
            "product_type": product_type,
            "price": round(random.uniform(20, 300), 2),
            "popularity_score": random.randint(1, 100),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365)),
            "is_on_sale": is_on_sale,
            "discount_pct": random.choice([10, 15, 20, 25, 30]) if is_on_sale else 0,
            "inventory_level": random.choice(["Low", "Medium", "High"]),
            "margin_score": round(random.uniform(0.25, 0.75), 2),
            "trend_score": random.randint(1, 100),
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
            "target_audience": product["audience"],
            "target_product_type": product["product_type"],
        })

    return pd.DataFrame(bids)
