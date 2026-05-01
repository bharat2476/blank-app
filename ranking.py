import pandas as pd
import numpy as np
from datetime import datetime


APP_AFFINITIES = {
    "Run Club App": ["Running", "Trail"],
    "Training App": ["Training", "Yoga"],
    "Sneaker Drops App": ["Lifestyle", "Basketball", "Skateboarding"],
    "Shopping App": ["Running", "Training", "Lifestyle", "Soccer"],
}

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
    matched_apps = [
        app for app in app_signals
        if product["category"] in APP_AFFINITIES.get(app, [])
    ]
    return min(1.0, len(matched_apps) / 2)


def shoe_email_status(user):
    days = user.get("last_shoe_purchase_days_ago")
    if not user.get("email_opt_in", False) or not user.get("consent_marketing", False):
        return "Do not email: member is not opted in for marketing."
    if user.get("emails_sent_last_7_days", 0) >= user.get("email_frequency_cap_per_week", 3):
        return "Suppress email: weekly frequency cap reached."
    if days is None or pd.isna(days):
        return "Eligible: no prior shoe purchase."
    if days < 165:
        remaining = int(165 - days)
        return f"Suppress shoe emails for {remaining} more days."
    return "Eligible: 5.5 month running shoe replenishment window reached."


def privacy_safe_user(user, privacy_mode):
    safe_user = user.copy()
    if privacy_mode == "Full consent":
        return safe_user

    if privacy_mode == "Limited consent":
        safe_user["app_signals"] = []
        safe_user["estimated_monthly_miles"] = None
        return safe_user

    safe_user["app_signals"] = []
    safe_user["browser_signal"] = "Trending"
    safe_user["interests"] = [safe_user.get("segment", "Running").split()[0]]
    safe_user["estimated_monthly_miles"] = None
    safe_user["last_shoe_purchase_days_ago"] = None
    return safe_user


def lifecycle_strategy(user):
    stage = user.get("lifecycle_stage", "Active Member")
    strategies = {
        "New Visitor": "Use cold-start ranking: trending products, declared interest, and broad sport popularity.",
        "First Purchase Prospect": "Use first-purchase conversion offer with entry-level products and sale ribbons.",
        "Repeat Runner": "Prioritize replenishment, performance upgrades, and running accessories.",
        "Active Member": "Balance exploit recommendations with exploration across adjacent sport categories.",
        "Lapsed Runner": "Reactivate with replenishment timing, value messaging, and low-frequency email cadence.",
        "High-Value Member": "Prioritize premium launches, high-margin products, and early-access messaging.",
    }
    return strategies.get(stage, strategies["Active Member"])


def lifecycle_score(user, product):
    stage = user.get("lifecycle_stage", "Active Member")
    product_type = product["product_type"]
    category = product["category"]
    if stage == "New Visitor":
        return product["trend_norm"] * 0.10
    if stage == "First Purchase Prospect":
        return (0.08 if product["is_on_sale"] else 0.0) + product["popularity_norm"] * 0.04
    if stage == "Repeat Runner":
        return 0.12 if product_type == "Footwear" and category in ["Running", "Trail"] else 0.02
    if stage == "Lapsed Runner":
        return 0.10 if product_type == "Footwear" else 0.03
    if stage == "High-Value Member":
        return product["margin_score"] * 0.12
    return product["recency_norm"] * 0.04


def explain_recommendation(user, product):
    reasons = []
    if product["category"] in user.get("interests", []):
        reasons.append(f"matches {product['category']} interest")
    if product["browser_score"] > 0:
        reasons.append(f"matches browser intent: {user.get('browser_signal')}")
    if product["app_score"] > 0:
        matching_apps = [
            app for app in user.get("app_signals", [])
            if product["category"] in APP_AFFINITIES.get(app, [])
        ]
        if matching_apps:
            reasons.append(f"supported by {', '.join(matching_apps)} signal")
    if product["trend_score"] >= 75:
        reasons.append("trending in the marketplace")
    if product["is_on_sale"]:
        reasons.append(f"{int(product['discount_pct'])}% sale opportunity")
    if not reasons:
        reasons.append("selected for discovery and catalog diversity")
    return "Recommended because it " + "; ".join(reasons[:3]) + "."


def add_recommendation_explanations(ranked_df, user):
    df = ranked_df.copy()
    df["why_recommended"] = df.apply(lambda row: explain_recommendation(user, row), axis=1)
    return df


def martech_email_decision(user, top_product):
    status = shoe_email_status(user)
    can_email = status.startswith("Eligible")
    if not can_email:
        subject = "No campaign sent"
        action = "Suppress"
    else:
        product_name = top_product["name"] if top_product is not None else "recommended products"
        subject = f"{user['customer_name']}, your next run starts with {product_name}"
        action = "Send"

    return {
        "action": action,
        "channel": user.get("channel_preference", "Email"),
        "subject_line": subject,
        "decision_reason": status,
        "privacy_note": "Uses consented, synthetic lifecycle and shoe-usage signals only.",
    }


def simulate_experiment(ranked_df, user):
    top_20 = ranked_df.head(20)
    avg_score = top_20["final_score"].mean()
    relevance = top_20[["interest_score", "browser_score", "app_score"]].mean().mean()
    sale_share = top_20["is_on_sale"].mean()
    trend_strength = top_20["trend_norm"].mean()
    fatigue_penalty = min(user.get("emails_sent_last_7_days", 0), 5) * 0.006
    rows = [
        {
            "variant": "Control: popularity ranking",
            "ctr": round(0.045 + trend_strength * 0.025, 3),
            "conversion": round(0.018 + sale_share * 0.012, 3),
            "revenue_per_session": round(2.15 + avg_score * 1.2, 2),
            "unsubscribe_rate": round(0.010 + fatigue_penalty, 3),
        },
        {
            "variant": "Personalized: lifecycle + consent",
            "ctr": round(0.060 + relevance * 0.050, 3),
            "conversion": round(0.025 + relevance * 0.030 + sale_share * 0.010, 3),
            "revenue_per_session": round(2.70 + avg_score * 2.1, 2),
            "unsubscribe_rate": round(max(0.004, 0.012 + fatigue_penalty - 0.006), 3),
        },
    ]
    df = pd.DataFrame(rows)
    df["lift_vs_control"] = df["revenue_per_session"].pct_change().fillna(0).round(3)
    return df


def business_impact(experiment_df, users_count):
    control = experiment_df.iloc[0]
    treatment = experiment_df.iloc[1]
    session_volume = users_count * 25
    incremental_revenue = (treatment["revenue_per_session"] - control["revenue_per_session"]) * session_volume
    unsub_reduction = max(0, control["unsubscribe_rate"] - treatment["unsubscribe_rate"])
    return {
        "Incremental Revenue": f"${incremental_revenue:,.0f}",
        "Conversion Lift": f"{((treatment['conversion'] / control['conversion']) - 1) * 100:.1f}%",
        "Revenue / Session Lift": f"{treatment['lift_vs_control'] * 100:.1f}%",
        "Reduced Unsubscribes": f"{unsub_reduction * session_volume:,.0f}",
        "Privacy-Safe Coverage": "100% synthetic demo data",
    }


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
        df.apply(lambda row: lifecycle_score(user, row), axis=1) +
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
