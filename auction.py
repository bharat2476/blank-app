import pandas as pd
import numpy as np

# -----------------------------------------
# HELPER: Relevance Score (same logic as ranking)
# -----------------------------------------

def relevance_score(user_interests, product_category):
    return 1.0 if product_category in user_interests else 0.2


# -----------------------------------------
# FAIRNESS BOOST
# -----------------------------------------

def fairness_boost(is_small_seller, enforce_diversity):
    if enforce_diversity and is_small_seller:
        return 1.25   # boost small sellers
    return 1.0


# -----------------------------------------
# MAIN AUCTION FUNCTION
# -----------------------------------------

def run_auction(user, bids_df, products_df, sellers_df, config):
    """
    user: dict with interests
    bids_df: DataFrame of bids
    products_df: DataFrame of products
    sellers_df: DataFrame of sellers
    config: dict with sliders (roas_fairness, enforce_diversity)
    """

    df = bids_df.merge(products_df, on="product_id", how="left")
    df = df.merge(sellers_df, on="seller_id", how="left")

    # Compute relevance
    df["relevance"] = df["category"].apply(
        lambda c: relevance_score(user["interests"], c)
    )

    # Fairness boost
    df["fairness_factor"] = df.apply(
        lambda row: fairness_boost(row["is_small_seller"], config["enforce_diversity"]),
        axis=1
    )

    # ROAS vs fairness weighting
    roas_weight = config["roas_fairness"] / 100
    fairness_weight = 1 - roas_weight

    # Final auction score
    df["final_score"] = (
        df["bid_amount"] * roas_weight +
        df["relevance"] * 0.5 +
        df["fairness_factor"] * fairness_weight
    )

    df = df.sort_values("final_score", ascending=False)

    return df[[
        "bid_id",
        "seller_id",
        "product_id",
        "name",
        "category",
        "bid_amount",
        "relevance",
        "fairness_factor",
        "final_score"
    ]]
