"""
Product registry and simulated 1st-party member database for the MarTech demo.
"""

from __future__ import annotations

import hashlib
import random
from datetime import datetime, timedelta

import pandas as pd

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ---------------------------------------------------------------------------
# Product registry (canonical catalog)
# ---------------------------------------------------------------------------

PRODUCT_REGISTRY: list[dict] = [
    {"sku": "RUN-PEG-40", "name": "Pegasus 40 Road Runner", "category": "Running", "product_type": "Footwear", "audience": "Men", "price": 129.99, "margin": 0.42, "behavioral_tags": ["running", "road", "cushioning", "daily trainer"]},
    {"sku": "RUN-VOM-17", "name": "Vomero 17 Premium Cushion", "category": "Running", "product_type": "Footwear", "audience": "Women", "price": 159.99, "margin": 0.38, "behavioral_tags": ["running", "max cushion", "recovery", "long run"]},
    {"sku": "RUN-ALP-06", "name": "Alphafly 3 Race Day", "category": "Running", "product_type": "Footwear", "audience": "Men", "price": 284.99, "margin": 0.31, "behavioral_tags": ["running", "racing", "carbon plate", "performance"]},
    {"sku": "TRL-KIG-07", "name": "Kiger 7 Trail Shoe", "category": "Trail", "product_type": "Footwear", "audience": "Women", "price": 139.99, "margin": 0.40, "behavioral_tags": ["trail", "hiking", "grip", "outdoor"]},
    {"sku": "TRL-WILD-02", "name": "Wildhorse 8 Trail", "category": "Trail", "product_type": "Footwear", "audience": "Men", "price": 124.99, "margin": 0.41, "behavioral_tags": ["trail", "mud", "outdoor", "ultra"]},
    {"sku": "HIK-BOOT-09", "name": "All-Weather Hiking Boot", "category": "Trail", "product_type": "Footwear", "audience": "Men", "price": 189.99, "margin": 0.45, "behavioral_tags": ["hiking", "outdoor", "waterproof", "ankle support"]},
    {"sku": "BB-DUNK-LOW", "name": "Dunk Low Retro", "category": "Basketball", "product_type": "Footwear", "audience": "Men", "price": 114.99, "margin": 0.35, "behavioral_tags": ["lifestyle", "sneaker culture", "streetwear", "basketball"]},
    {"sku": "BB-LEB-21", "name": "LeBron XXI Basketball", "category": "Basketball", "product_type": "Footwear", "audience": "Men", "price": 199.99, "margin": 0.33, "behavioral_tags": ["basketball", "indoor court", "support", "performance"]},
    {"sku": "BB-SAB-01", "name": "Sabrina 1 Court Shoe", "category": "Basketball", "product_type": "Footwear", "audience": "Women", "price": 129.99, "margin": 0.36, "behavioral_tags": ["basketball", "agility", "women", "court"]},
    {"sku": "TRN-MET-08", "name": "Metcon 8 Cross-Training", "category": "Training", "product_type": "Footwear", "audience": "Women", "price": 139.99, "margin": 0.39, "behavioral_tags": ["training", "gym", "crossfit", "stability"]},
    {"sku": "TRN-SUP-05", "name": "SuperRep Go 5", "category": "Training", "product_type": "Footwear", "audience": "Men", "price": 119.99, "margin": 0.37, "behavioral_tags": ["training", "hiit", "studio", "versatile"]},
    {"sku": "SOC-MRC-09", "name": "Mercurial Vapor 15", "category": "Soccer", "product_type": "Footwear", "audience": "Men", "price": 274.99, "margin": 0.30, "behavioral_tags": ["soccer", "speed", "firm ground", "competition"]},
    {"sku": "SOC-PHA-03", "name": "Phantom Luna II", "category": "Soccer", "product_type": "Footwear", "audience": "Women", "price": 249.99, "margin": 0.32, "behavioral_tags": ["soccer", "touch", "women", "elite"]},
    {"sku": "LIF-AIR-90", "name": "Air Max 90 Essential", "category": "Lifestyle", "product_type": "Footwear", "audience": "Men", "price": 129.99, "margin": 0.34, "behavioral_tags": ["lifestyle", "casual", "heritage", "everyday"]},
    {"sku": "LIF-AF1-07", "name": "Air Force 1 '07", "category": "Lifestyle", "product_type": "Footwear", "audience": "Women", "price": 114.99, "margin": 0.36, "behavioral_tags": ["lifestyle", "classic", "streetwear", "white sneaker"]},
    {"sku": "SKT-BRU-05", "name": "SB Bruin ISO", "category": "Skateboarding", "product_type": "Footwear", "audience": "Men", "price": 79.99, "margin": 0.43, "behavioral_tags": ["skateboarding", "board feel", "durability", "street"]},
    {"sku": "GOLF-VR2-04", "name": "Victory Tour 2 Golf", "category": "Golf", "product_type": "Footwear", "audience": "Men", "price": 179.99, "margin": 0.41, "behavioral_tags": ["golf", "spiked", "stability", "outdoor"]},
    {"sku": "KID-PEG-25", "name": "Kids Pegasus 25", "category": "Running", "product_type": "Footwear", "audience": "Kids", "price": 89.99, "margin": 0.44, "behavioral_tags": ["kids", "running", "school sport", "durable"]},
    {"sku": "APP-DRY-TEE", "name": "Dri-FIT ADV Run Tee", "category": "Running", "product_type": "Apparel", "audience": "Men", "price": 44.99, "margin": 0.55, "behavioral_tags": ["running", "moisture wicking", "breathable", "summer"]},
    {"sku": "APP-THER-HD", "name": "Therma-FIT Training Hoodie", "category": "Training", "product_type": "Apparel", "audience": "Women", "price": 74.99, "margin": 0.52, "behavioral_tags": ["training", "cold weather", "layering", "gym"]},
    {"sku": "APP-PRO-TGT", "name": "Pro Dri-FIT Tight", "category": "Training", "product_type": "Apparel", "audience": "Women", "price": 54.99, "margin": 0.53, "behavioral_tags": ["training", "compression", "studio", "yoga"]},
    {"sku": "APP-CLB-FLZ", "name": "Club Fleece Jogger", "category": "Lifestyle", "product_type": "Apparel", "audience": "Men", "price": 64.99, "margin": 0.50, "behavioral_tags": ["lifestyle", "casual", "lounge", "everyday"]},
    {"sku": "APP-AERO-SH", "name": "AeroSwift Race Short", "category": "Running", "product_type": "Apparel", "audience": "Men", "price": 59.99, "margin": 0.51, "behavioral_tags": ["running", "racing", "lightweight", "split shorts"]},
    {"sku": "APP-YOGA-BR", "name": "Zenvy Gentle-Support Bra", "category": "Yoga", "product_type": "Apparel", "audience": "Women", "price": 49.99, "margin": 0.54, "behavioral_tags": ["yoga", "studio", "low impact", "comfort"]},
    {"sku": "APP-RAIN-JK", "name": "Storm-FIT Run Jacket", "category": "Running", "product_type": "Apparel", "audience": "Women", "price": 119.99, "margin": 0.48, "behavioral_tags": ["running", "waterproof", "rain", "reflective"]},
    {"sku": "APP-TRAIL-VST", "name": "Trail Running Vest", "category": "Trail", "product_type": "Apparel", "audience": "Men", "price": 89.99, "margin": 0.49, "behavioral_tags": ["trail", "ultra", "hydration", "outdoor"]},
    {"sku": "ACC-ELT-SCK", "name": "Elite Cushion Crew Socks (3-pack)", "category": "Running", "product_type": "Accessories", "audience": "Men", "price": 24.99, "margin": 0.62, "behavioral_tags": ["running", "blister prevention", "cushion", "replenishment"]},
    {"sku": "ACC-HYD-21", "name": "21oz Insulated Hydration Flask", "category": "Trail", "product_type": "Accessories", "audience": "Women", "price": 34.99, "margin": 0.58, "behavioral_tags": ["trail", "hydration", "outdoor", "hiking"]},
    {"sku": "ACC-HRT-BAG", "name": "Heritage Gym Duffel", "category": "Lifestyle", "product_type": "Accessories", "audience": "Men", "price": 54.99, "margin": 0.56, "behavioral_tags": ["lifestyle", "travel", "gym", "carry"]},
    {"sku": "ACC-RUN-BLT", "name": "Expandable Running Belt", "category": "Running", "product_type": "Accessories", "audience": "Women", "price": 29.99, "margin": 0.60, "behavioral_tags": ["running", "race day", "phone pocket", "lightweight"]},
    {"sku": "ACC-CLB-CAP", "name": "Club Unstructured Cap", "category": "Lifestyle", "product_type": "Accessories", "audience": "Men", "price": 27.99, "margin": 0.61, "behavioral_tags": ["lifestyle", "sun protection", "casual", "everyday"]},
    {"sku": "ACC-TRN-MAT", "name": "Training Mat 4mm", "category": "Yoga", "product_type": "Accessories", "audience": "Women", "price": 39.99, "margin": 0.57, "behavioral_tags": ["yoga", "training", "home gym", "studio"]},
    {"sku": "ACC-SNK-LCE", "name": "Premium Sneaker Laces (2-pack)", "category": "Lifestyle", "product_type": "Accessories", "audience": "Men", "price": 12.99, "margin": 0.65, "behavioral_tags": ["sneaker culture", "customization", "lifestyle", "gift"]},
    {"sku": "TEN-VAP-11", "name": "Vapor Cage 4 Tennis", "category": "Tennis", "product_type": "Footwear", "audience": "Women", "price": 149.99, "margin": 0.37, "behavioral_tags": ["tennis", "lateral support", "hard court", "performance"]},
    {"sku": "RUN-INV-12", "name": "Invincible 3 Max Stack", "category": "Running", "product_type": "Footwear", "audience": "Women", "price": 179.99, "margin": 0.36, "behavioral_tags": ["running", "injury prevention", "max cushion", "recovery"]},
    {"sku": "OUT-PARKA", "name": "Storm-FIT Parka", "category": "Trail", "product_type": "Apparel", "audience": "Men", "price": 249.99, "margin": 0.46, "behavioral_tags": ["hiking", "outdoor", "waterproof", "winter"]},
    {"sku": "BB-SHORT-DR", "name": "Dri-FIT Basketball Short", "category": "Basketball", "product_type": "Apparel", "audience": "Men", "price": 39.99, "margin": 0.54, "behavioral_tags": ["basketball", "court", "moisture wicking", "training"]},
]

SKU_TO_REGISTRY = {item["sku"]: item for item in PRODUCT_REGISTRY}


# ---------------------------------------------------------------------------
# User registry templates
# ---------------------------------------------------------------------------

SEGMENT_INTERESTS = {
    "Performance Runner": ["Running", "Training", "Trail"],
    "Sneaker Culture": ["Lifestyle", "Basketball", "Skateboarding"],
    "Team Sports Athlete": ["Soccer", "Basketball", "Training"],
    "Wellness & Studio": ["Yoga", "Training", "Running"],
    "Outdoor Explorer": ["Trail", "Golf", "Running"],
}

APPS = ["Run Club App", "Training App", "Sneaker Drops App", "Shopping App"]


def _rng_for_user(user_id: int) -> random.Random:
    digest = hashlib.sha256(f"member-{user_id}".encode()).hexdigest()
    return random.Random(int(digest[:8], 16))


def get_mock_1st_party_data(user_id: int) -> dict:
    """
    Historical 1st-party event log for propensity and hybrid ranking math.
    Deterministic per user_id for reproducible demos.
    """
    uid = int(user_id)
    rng = _rng_for_user(uid)
    catalog = PRODUCT_REGISTRY
    n_purchases = rng.randint(1, 5)
    purchase_indices = rng.sample(range(len(catalog)), k=min(n_purchases, len(catalog)))

    prior_purchases = []
    for idx in purchase_indices:
        item = catalog[idx]
        days_ago = rng.choice([7, 14, 21, 45, 90, 120, 168, 210])
        prior_purchases.append({
            "sku": item["sku"],
            "name": item["name"],
            "category": item["category"],
            "product_type": item["product_type"],
            "price": item["price"],
            "margin": item["margin"],
            "days_ago": days_ago,
            "behavioral_tags": list(item["behavioral_tags"]),
        })

    categories = list({p["category"] for p in prior_purchases})
    extra_categories = rng.sample(
        list({item["category"] for item in catalog}),
        k=min(3, len(catalog)),
    )
    dwell_pool = list(dict.fromkeys(categories + extra_categories))

    high_dwell_categories = []
    for cat in dwell_pool[: rng.randint(2, 4)]:
        high_dwell_categories.append({
            "category": cat,
            "dwell_seconds": rng.randint(90, 720),
            "page_views": rng.randint(3, 18),
            "pdp_views": rng.randint(1, 6),
        })

    affinity_tags = sorted(
        {
            tag
            for purchase in prior_purchases
            for tag in purchase["behavioral_tags"]
        }
        | {
            tag
            for item in catalog
            if item["category"] in {d["category"] for d in high_dwell_categories}
            for tag in item["behavioral_tags"][:2]
        }
    )

    return {
        "user_id": uid,
        "prior_purchases": prior_purchases,
        "high_dwell_categories": high_dwell_categories,
        "cart_abandons": [
            {
                "sku": catalog[rng.randint(0, len(catalog) - 1)]["sku"],
                "days_ago": rng.choice([1, 2, 3, 5]),
                "cart_value": round(rng.uniform(45, 220), 2),
            }
            for _ in range(rng.randint(0, 2))
        ],
        "email_engagement": {
            "opens_30d": rng.randint(0, 12),
            "clicks_30d": rng.randint(0, 5),
            "last_open_days_ago": rng.choice([1, 3, 7, 14, None]),
        },
        "affinity_tags": affinity_tags,
        "lifetime_value": round(sum(p["price"] for p in prior_purchases) * rng.uniform(1.1, 2.4), 2),
        "replenishment_due_skus": [
            p["sku"] for p in prior_purchases if p["days_ago"] >= 120 and p["product_type"] == "Footwear"
        ],
    }


def get_user_registry(n: int = 100) -> pd.DataFrame:
    """Simulated member dimension table keyed by user_id."""
    segments = list(SEGMENT_INTERESTS.keys())
    genders = ["Men", "Women"]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    locations = ["NY", "CA", "TX", "WA", "FL", "IL", "GA", "OR"]
    rows = []

    for user_id in range(n):
        rng = _rng_for_user(user_id)
        segment = segments[user_id % len(segments)]
        interests = SEGMENT_INTERESTS[segment][:2]
        customer_type = "Repeat" if user_id < int(n * 0.62) else "New"
        first_party = get_mock_1st_party_data(user_id)
        last_shoe = next(
            (p for p in first_party["prior_purchases"] if p["product_type"] == "Footwear"),
            None,
        )
        last_shoe_purchase_days_ago = last_shoe["days_ago"] if last_shoe else None
        email_opt_in = rng.choice([True, True, True, False])

        if customer_type == "New":
            lifecycle_stage = rng.choice(["New Visitor", "First Purchase Prospect"])
        elif last_shoe_purchase_days_ago and last_shoe_purchase_days_ago >= 230:
            lifecycle_stage = "Lapsed Runner"
        elif rng.random() < 0.22:
            lifecycle_stage = "High-Value Member"
        else:
            lifecycle_stage = rng.choice(["Repeat Runner", "Active Member"])

        rows.append({
            "user_id": user_id,
            "customer_name": f"Member {user_id:03d}",
            "gender": rng.choice(genders),
            "age_group": rng.choice(age_groups),
            "location": rng.choice(locations),
            "customer_type": customer_type,
            "lifecycle_stage": lifecycle_stage,
            "segment": segment,
            "interests": interests,
            "browser_signal": rng.choice(interests + ["Sale", "Trending"]),
            "app_signals": rng.sample(APPS, rng.randint(1, 3)),
            "run_frequency_per_week": rng.choice([0, 1, 2, 3, 4, 5]),
            "estimated_monthly_miles": rng.randint(0, 120),
            "last_purchase_category": (
                first_party["prior_purchases"][0]["product_type"]
                if first_party["prior_purchases"]
                else rng.choice(["Footwear", "Apparel", "Accessories"])
            ),
            "last_shoe_purchase_days_ago": last_shoe_purchase_days_ago,
            "avg_order_value": round(first_party["lifetime_value"] / max(len(first_party["prior_purchases"]), 1), 2),
            "email_opt_in": email_opt_in,
            "consent_app_usage": rng.choice([True, True, True, False]),
            "consent_marketing": email_opt_in and rng.choice([True, True, True, False]),
            "channel_preference": rng.choice(["Email", "Push", "In-app", "Email + Push"]),
            "emails_sent_last_7_days": rng.randint(0, 5),
            "email_frequency_cap_per_week": rng.choice([2, 3, 4]),
            "affinity_tags": first_party["affinity_tags"],
        })

    return pd.DataFrame(rows)


def get_product_registry_df() -> pd.DataFrame:
    return pd.DataFrame(PRODUCT_REGISTRY)


def build_product_catalog(sellers_df: pd.DataFrame, target_n: int = 500) -> pd.DataFrame:
    """
    Expand the canonical registry into a marketplace catalog with relational keys.
    Variants inherit SKU lineage and behavioral_tags from parent registry rows.
    """
    rng = random.Random(RANDOM_SEED)
    rows = []
    registry = PRODUCT_REGISTRY
    product_id = 0

    while product_id < target_n:
        template = registry[product_id % len(registry)]
        seller = sellers_df.sample(1, random_state=product_id).iloc[0]
        variant_n = product_id // len(registry)
        price_jitter = round(rng.uniform(-12, 18), 2) if variant_n else 0.0
        is_on_sale = rng.random() < 0.28

        rows.append({
            "product_id": product_id,
            "sku": template["sku"] if variant_n == 0 else f"{template['sku']}-V{variant_n}",
            "parent_sku": template["sku"],
            "seller_id": seller["seller_id"],
            "name": template["name"] if variant_n == 0 else f"{template['name']} ({variant_n})",
            "category": template["category"],
            "audience": template["audience"],
            "product_type": template["product_type"],
            "price": round(max(12.0, template["price"] + price_jitter), 2),
            "margin": template["margin"],
            "margin_score": template["margin"],
            "behavioral_tags": list(template["behavioral_tags"]),
            "popularity_score": rng.randint(20, 100),
            "created_at": datetime.now() - timedelta(days=rng.randint(1, 365)),
            "is_on_sale": is_on_sale,
            "discount_pct": rng.choice([10, 15, 20, 25, 30]) if is_on_sale else 0,
            "inventory_level": rng.choice(["Low", "Medium", "High"]),
            "trend_score": rng.randint(30, 100),
        })
        product_id += 1

    return pd.DataFrame(rows)


def lookup_registry_item(sku: str) -> dict | None:
    base = sku.split("-V")[0] if "-V" in sku else sku
    return SKU_TO_REGISTRY.get(base)
