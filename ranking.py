import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------------------
# HELPER: Interest Match Score
# -----------------------------------------

def interest_match_score(user_interests, product_category):
    return 1.0 if product_category in user_interests else 0.0


def audience_match_score(user, audience):
    if audience == "Kids":
        return 0.65
    return 1.0 if audience == user["gender"] else 0.25


def browser_signal_score(browser_signal, product):
    if browser_signal == product["category"]:
        return 1.0
    if browser_signal == "Sale" and product["is_on_sale"]:
        return 1.0
    if browser_signal == "Trending" and product["trend_score"] >= 70:
        return 1.0
    return 0.0


def app_signal_score(app_signals, product):
    app_affinities = {
        "Nike Run Club": ["Running", "Trail"],
        "Nike Training Club": ["Training", "Yoga"],
        "SNKRS": ["Lifestyle", "Basketball", "Skateboarding"],
        "Nike App": ["Running", "Training", "Lifestyle", "Soccer"],
    }
    matched_apps = [
        app for app in app_signals
        if product["category"] in app_affinities.get(app, [])
    ]
    return min(1.0, len(matched_apps) / 2)


def shoe_email_status(user):
    days = user.get("last_shoe_purchase_days_ago")
    if not user.get("email_opt_in", False):
        return "Do not email: user is not opted in."
    if days is None or pd.isna(days):
        return "Eligible: no prior shoe purchase."
    if days < 165:
        remaining = int(165 - days)
        return f"Suppress shoe emails for {remaining} more days."
    return "Eligible: 5.5 month running shoe replenishment window reached."


# -----------------------------------------
# HELPER: Recency Score
# -----------------------------------------

def recency_score(created_at):
    days_old = (datetime.now() - created_at).days
    return max(0.1, 1 - (days_old / 365))  # newer products score higher


# -----------------------------------------
# MAIN RANKING FUNCTION
# -----------------------------------------

def rank_products(user, products_df, config):
    """
    user: dict with interests, segment, etc.
    products_df: DataFrame of products
    config: dict with sliders (roas_fairness, explore_exploit)
    """

    df = products_df.copy()

    df["interest_score"] = df["category"].apply(
        lambda c: interest_match_score(user["interests"], c)
    )
    df["audience_score"] = df["audience"].apply(lambda audience: audience_match_score(user, audience))
    df["browser_score"] = df.apply(lambda row: browser_signal_score(user["browser_signal"], row), axis=1)
    df["app_score"] = df.apply(lambda row: app_signal_score(user["app_signals"], row), axis=1)
    df["popularity_norm"] = df["popularity_score"] / df["popularity_score"].max()
    df["trend_norm"] = df["trend_score"] / df["trend_score"].max()
    df["recency_norm"] = df["created_at"].apply(recency_score)

    explore_weight = config["explore_exploit"] / 100
    exploit_weight = 1 - explore_weight
    lifecycle_boost = 0.12 if user["customer_type"] == "Repeat" else 0.0
    discovery_boost = 0.12 if user["customer_type"] == "New" else 0.0

    df["final_score"] = (
        df["interest_score"] * 0.30 * exploit_weight +
        df["audience_score"] * 0.18 * exploit_weight +
        df["browser_score"] * 0.15 * exploit_weight +
        df["app_score"] * 0.14 * exploit_weight +
        df["popularity_norm"] * 0.12 * exploit_weight +
        df["trend_norm"] * 0.06 * exploit_weight +
        df["recency_norm"] * 0.05 * exploit_weight +
        df["margin_score"] * lifecycle_boost +
        df["trend_norm"] * discovery_boost +
        np.random.default_rng(config.get("seed", 42)).uniform(0, explore_weight, size=len(df))
    )

    df = df.sort_values("final_score", ascending=False)

    return df[[
        "product_id",
        "seller_id",
        "name",
        "category",
        "audience",
        "product_type",
        "price",
        "is_on_sale",
        "discount_pct",
        "trend_score",
        "interest_score",
        "audience_score",
        "browser_score",
        "app_score",
        "popularity_norm",
        "trend_norm",
        "recency_norm",
        "final_score"
    ]]


def ribbon_products(products_df, ribbon_type, audience=None, product_type=None):
    df = products_df.copy()
    if audience and audience != "All":
        df = df[df["audience"] == audience]
    if product_type and product_type != "All":
        df = df[df["product_type"] == product_type]

    if ribbon_type == "Sale":
        return df[df["is_on_sale"]].sort_values(["discount_pct", "popularity_score"], ascending=False)
    if ribbon_type == "Trending":
        return df.sort_values(["trend_score", "popularity_score"], ascending=False)
    return df
