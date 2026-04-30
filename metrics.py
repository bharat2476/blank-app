import pandas as pd
import numpy as np

# ---------------------------------------------------
# CTR (Click-Through Rate)
# ---------------------------------------------------

def compute_ctr(events_df):
    if len(events_df) == 0:
        return 0.0
    views = len(events_df[events_df["event_type"] == "view"])
    clicks = len(events_df[events_df["event_type"] == "click"])
    return round(clicks / views, 3) if views > 0 else 0.0


# ---------------------------------------------------
# Conversion Rate
# ---------------------------------------------------

def compute_conversion(events_df):
    if len(events_df) == 0:
        return 0.0
    clicks = len(events_df[events_df["event_type"] == "click"])
    purchases = len(events_df[events_df["event_type"] == "purchase"])
    return round(purchases / clicks, 3) if clicks > 0 else 0.0


# ---------------------------------------------------
# ROAS (Return on Ad Spend)
# ---------------------------------------------------

def compute_roas(auction_df, events_df):
    if len(auction_df) == 0:
        return 0.0

    # Total ad spend = sum of winning bids
    total_spend = auction_df["bid_amount"].sum()

    if "price" not in auction_df.columns:
        return 0.0

    # Revenue = sum of product prices for purchased items
    purchased_ids = events_df[events_df["event_type"] == "purchase"]["product_id"]
    revenue = auction_df[auction_df["product_id"].isin(purchased_ids)]["price"].sum()

    return round(revenue / total_spend, 3) if total_spend > 0 else 0.0


# ---------------------------------------------------
# Seller Diversity Index
# ---------------------------------------------------

def compute_seller_diversity(impressions_df):
    if len(impressions_df) == 0:
        return 0.0

    seller_counts = impressions_df["seller_id"].value_counts(normalize=True)
    diversity = 1 - np.sum(seller_counts ** 2)  # Gini-Simpson index

    return round(diversity, 3)


# ---------------------------------------------------
# Small Seller Share
# ---------------------------------------------------

def compute_small_seller_share(impressions_df, sellers_df):
    if len(impressions_df) == 0:
        return 0.0

    merged = impressions_df.merge(sellers_df, on="seller_id", how="left")
    small_seller_impressions = merged[merged["is_small_seller"] == True]

    return round(len(small_seller_impressions) / len(merged), 3)
