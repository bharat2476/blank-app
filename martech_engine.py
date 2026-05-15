"""
MarTech engine: medallion signal processing, hybrid ranking, and propensity-gated notifications.
"""

from datetime import datetime

import pandas as pd

from ranking import (
    add_recommendation_explanations,
    app_signal_score,
    audience_match_score,
    browser_signal_score,
    explain_recommendation,
    interest_match_score,
    lifecycle_score,
    martech_email_decision,
    rank_products,
    recency_score,
)

PROPENSITY_THRESHOLD = 0.75
REC_VARIANT_BEHAVIORAL = "Variant A: Behavioral-Only"
REC_VARIANT_HYBRID = "Variant B: Hybrid Model"


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def empty_interactions():
    return {
        "views": {},
        "clicks": {},
        "category_views": {},
        "category_clicks": {},
    }


def init_martech_session(session_state):
    if "interactions" not in session_state:
        session_state["interactions"] = empty_interactions()
    if "propensity_logs" not in session_state:
        session_state["propensity_logs"] = []
    if "notification_queue" not in session_state:
        session_state["notification_queue"] = []


def reset_martech_session(session_state):
    session_state["interactions"] = empty_interactions()
    session_state["propensity_logs"] = []
    session_state["notification_queue"] = []


def record_interaction(session_state, product_id, category, event_type):
    interactions = session_state.setdefault("interactions", empty_interactions())
    pid = int(product_id)
    cat = str(category)

    if event_type == "view":
        interactions["views"][pid] = interactions["views"].get(pid, 0) + 1
        interactions["category_views"][cat] = interactions["category_views"].get(cat, 0) + 1
    elif event_type == "click":
        interactions["clicks"][pid] = interactions["clicks"].get(pid, 0) + 1
        interactions["category_clicks"][cat] = interactions["category_clicks"].get(cat, 0) + 1


def log_propensity_evaluation(session_state, evaluation):
    logs = session_state.setdefault("propensity_logs", [])
    entry = evaluation["log_entry"]
    fingerprint = (
        entry["propensity_score"],
        entry["session_clicks"],
        entry["session_views"],
        entry["rule_gate"],
        entry["queued"],
    )
    if logs:
        last = logs[-1]
        last_fp = (
            last["propensity_score"],
            last["session_clicks"],
            last["session_views"],
            last["rule_gate"],
            last["queued"],
        )
        if last_fp == fingerprint:
            return

    logs.append(entry)
    if evaluation["queued"]:
        queue = session_state.setdefault("notification_queue", [])
        if not any(item["title"] == evaluation["notification"]["title"] for item in queue):
            queue.append(evaluation["notification"])


# ---------------------------------------------------------------------------
# Mock semantic / medallion layers
# ---------------------------------------------------------------------------

def bronze_layer_zero_party(user):
    """Bronze: raw declared (0-party) and consent signals."""
    return {
        "member_id": user.get("user_id"),
        "interests": list(user.get("interests", [])),
        "browser_signal": user.get("browser_signal"),
        "segment": user.get("segment"),
        "gender": user.get("gender"),
        "lifecycle_stage": user.get("lifecycle_stage"),
        "consent_marketing": bool(user.get("consent_marketing", False)),
        "consent_app_usage": bool(user.get("consent_app_usage", False)),
        "app_signals": list(user.get("app_signals", [])),
        "channel_preference": user.get("channel_preference", "Email"),
    }


def silver_layer_behavioral(user, interactions):
    """Silver: session behavioral aggregates."""
    views = interactions.get("views", {})
    clicks = interactions.get("clicks", {})
    return {
        "session_product_views": int(sum(views.values())),
        "session_product_clicks": int(sum(clicks.values())),
        "engaged_categories": sorted(
            set(interactions.get("category_clicks", {}).keys())
            | set(interactions.get("category_views", {}).keys())
        ),
        "run_frequency_per_week": user.get("run_frequency_per_week", 0),
        "estimated_monthly_miles": user.get("estimated_monthly_miles"),
    }


def gold_layer_member_profile(bronze, silver):
    """Gold: unified semantic profile for ranking and Martech."""
    return {
        **bronze,
        **silver,
        "profile_version": "gold_v1",
        "processed_at": datetime.now().isoformat(timespec="seconds"),
    }


def process_member_signals(user, interactions, privacy_mode, privacy_fn):
    """Run bronze → silver → gold before UI ranking."""
    safe_user = privacy_fn(user, privacy_mode)
    bronze = bronze_layer_zero_party(safe_user)
    silver = silver_layer_behavioral(safe_user, interactions)
    gold = gold_layer_member_profile(bronze, silver)
    return gold, safe_user


# ---------------------------------------------------------------------------
# Hybrid recommendation
# ---------------------------------------------------------------------------

def behavioral_affinity_score(product_row, interactions):
    pid = int(product_row["product_id"])
    category = product_row["category"]
    views = interactions.get("views", {}).get(pid, 0)
    clicks = interactions.get("clicks", {}).get(pid, 0)
    cat_views = interactions.get("category_views", {}).get(category, 0)
    cat_clicks = interactions.get("category_clicks", {}).get(category, 0)
    return min(
        1.0,
        views * 0.15 + clicks * 0.35 + cat_views * 0.08 + cat_clicks * 0.20,
    )


def _attach_behavioral_scores(df, interactions):
    out = df.copy()
    out["behavioral_score"] = out.apply(
        lambda row: behavioral_affinity_score(row, interactions),
        axis=1,
    )
    return out


def rank_products_variant(user, products_df, config, interactions, variant):
    """
    Variant A: session behavioral signals dominate.
    Variant B: hybrid blend of existing 0-party ranker + behavioral loop.
    """
    zero_party_df = rank_products(user, products_df, config)

    if variant == REC_VARIANT_BEHAVIORAL:
        df = products_df.copy()
        df["interest_score"] = df["category"].apply(
            lambda c: interest_match_score(user["interests"], c)
        )
        df["audience_score"] = df["audience"].apply(
            lambda audience: audience_match_score(user, audience)
        )
        df["browser_score"] = df.apply(
            lambda row: browser_signal_score(user["browser_signal"], row),
            axis=1,
        )
        df["app_score"] = df.apply(
            lambda row: app_signal_score(user["app_signals"], row),
            axis=1,
        )
        df["popularity_norm"] = df["popularity_score"] / df["popularity_score"].max()
        df["trend_norm"] = df["trend_score"] / df["trend_score"].max()
        df["recency_norm"] = df["created_at"].apply(recency_score)
        df["behavioral_score"] = df.apply(
            lambda row: behavioral_affinity_score(row, interactions),
            axis=1,
        )
        df["final_score"] = (
            df["behavioral_score"] * 0.72
            + df["popularity_norm"] * 0.14
            + df["trend_norm"] * 0.10
            + df["recency_norm"] * 0.04
        )
        df = df.sort_values("final_score", ascending=False)
        return df[zero_party_df.columns.tolist() + ["behavioral_score"]]

    hybrid = _attach_behavioral_scores(zero_party_df, interactions)
    hybrid["final_score"] = hybrid["final_score"] * 0.70 + hybrid["behavioral_score"] * 0.30
    hybrid = hybrid.sort_values("final_score", ascending=False)
    return hybrid


def build_dynamic_reason(user, product_row, variant, interactions):
    reasons = []
    behavioral = behavioral_affinity_score(product_row, interactions)
    if behavioral >= 0.2:
        reasons.append("boosted by your recent views/clicks in this session")
    if product_row.get("interest_score", 0) > 0:
        reasons.append("matches declared sport interests (0-party)")
    if product_row.get("browser_score", 0) > 0:
        reasons.append(f"aligned with browser intent: {user.get('browser_signal')}")
    if product_row.get("app_score", 0) > 0:
        reasons.append("supported by consented app affinity signals")
    if variant == REC_VARIANT_HYBRID and product_row.get("behavioral_score", 0) > 0:
        reasons.append("hybrid model blending 0-party + behavioral scores")
    if not reasons:
        reasons.append(explain_recommendation(user, product_row).replace("Recommended because it ", ""))
    label = "Behavioral-only ranking" if variant == REC_VARIANT_BEHAVIORAL else "Hybrid ranking"
    return f"Why am I seeing this? [{label}] {'; '.join(reasons[:3])}."


# ---------------------------------------------------------------------------
# Propensity-gated notifications
# ---------------------------------------------------------------------------

def compute_propensity_score(user, interactions, top_product):
    score = 0.32
    if user.get("consent_marketing"):
        score += 0.12
    if user.get("email_opt_in"):
        score += 0.08

    total_clicks = sum(interactions.get("clicks", {}).values())
    total_views = sum(interactions.get("views", {}).values())
    score += min(0.28, total_clicks * 0.09)
    score += min(0.12, total_views * 0.03)

    if top_product is not None:
        if interest_match_score(user.get("interests", []), top_product["category"]) > 0:
            score += 0.18
        if top_product.get("is_on_sale"):
            score += 0.05

    lifecycle = user.get("lifecycle_stage", "")
    if lifecycle in ("Repeat Runner", "High-Value Member", "Active Member"):
        score += 0.08
    if lifecycle == "Lapsed Runner":
        score -= 0.05

    return round(min(1.0, max(0.0, score)), 3)


def evaluate_push_notification(user, interactions, top_product, threshold=PROPENSITY_THRESHOLD):
    """Propensity gate for push; lifecycle rules still apply via email decision helper."""
    base_decision = martech_email_decision(user, top_product)
    score = compute_propensity_score(user, interactions, top_product)
    channel = user.get("channel_preference", "Email")
    push_capable = "Push" in channel or channel == "In-app"
    rule_gate_open = base_decision["action"] == "Send"
    queued = score > threshold and rule_gate_open and push_capable

    product_name = (
        top_product["name"] if top_product is not None else "recommended gear"
    )
    notification = {
        "channel": "Push",
        "title": f"Hey {user.get('customer_name', 'Member')}, ready for your next run?",
        "body": f"Check out {product_name} — picked for your {user.get('lifecycle_stage', 'profile')}.",
        "propensity_score": score,
        "queued_at": datetime.now().isoformat(timespec="seconds"),
    }

    log_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "channel": "Push",
        "propensity_score": score,
        "threshold": threshold,
        "queued": queued,
        "rule_gate": base_decision["action"],
        "lifecycle": user.get("lifecycle_stage"),
        "session_views": int(sum(interactions.get("views", {}).values())),
        "session_clicks": int(sum(interactions.get("clicks", {}).values())),
        "decision": "QUEUED" if queued else "SUPPRESSED",
        "note": base_decision["decision_reason"],
    }

    return {
        "score": score,
        "threshold": threshold,
        "queued": queued,
        "log_entry": log_entry,
        "notification": notification,
        "base_decision": base_decision,
    }
