import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------------------
# HELPER: Interest Match Score
# -----------------------------------------

def interest_match_score(user_interests, product_category):
    return 1.0 if product_category in user_interests else 0.0


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

    # Compute base scores
    df["interest_score"] = df["category"].apply(
        lambda c: interest_match_score(user["interests"], c)
    )

    df["popularity_norm"] = df["popularity_score"] / df["popularity_score"].max()

    df["recency_norm"] = df["created_at"].apply(recency_score)

    # Weighting logic based on sliders
    explore_weight = config["explore_exploit"] / 100
    exploit_weight = 1 - explore_weight

    df["final_score"] = (
        df["interest_score"] * 0.5 * exploit_weight +
        df["popularity_norm"] * 0.3 * exploit_weight +
        df["recency_norm"] * 0.2 * exploit_weight +
        np.random.uniform(0, explore_weight, size=len(df))  # exploration randomness
    )

    df = df.sort_values("final_score", ascending=False)

    return df[[
        "product_id",
        "seller_id",
        "name",
        "category",
        "price",
        "interest_score",
        "popularity_norm",
        "recency_norm",
        "final_score"
    ]]
