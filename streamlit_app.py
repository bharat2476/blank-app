import streamlit as st
import pandas as pd

from data_generator import generate_users, generate_sellers, generate_products, generate_bids
from ranking import rank_products
from auction import run_auction
from metrics import (
    compute_ctr,
    compute_conversion,
    compute_roas,
    compute_seller_diversity,
    compute_small_seller_share
)

st.set_page_config(page_title="Marketplace Personalization Simulator", layout="wide")

st.title("Marketplace Personalization & Ad Targeting Simulator")

# ---------------------------------------------------------
# INITIALIZE DATA ON FIRST LOAD
# ---------------------------------------------------------

if "users" not in st.session_state:
    st.session_state["users"] = generate_users()
    st.session_state["sellers"] = generate_sellers()
    st.session_state["products"] = generate_products(st.session_state["sellers"])
    st.session_state["bids"] = generate_bids(
        st.session_state["products"],
        st.session_state["sellers"]
    )

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Simulation Config",
    "Personalized Results",
    "Ads & Auction",
    "Metrics Dashboard"
])

# ---------------------------------------------------------
# TAB 1 — SIMULATION CONFIG
# ---------------------------------------------------------

with tab1:
    st.header("Simulation Configuration")

    user_segment = st.selectbox(
        "Select User Segment",
        ["Runner", "Sneakerhead", "Tech Buyer", "Outdoor Enthusiast"]
    )

    roas_fairness = st.slider(
        "ROAS vs Fairness Optimization",
        0, 100, 50
    )

    explore_exploit = st.slider(
        "Exploration vs Exploitation",
        0, 100, 50
    )

    enforce_diversity = st.checkbox("Enforce Seller Diversity Guardrail")

    if st.button("Run Simulation"):
        # Pick a random user from the chosen segment
        users_df = st.session_state["users"]
        user = users_df[users_df["segment"] == user_segment].sample(1).iloc[0].to_dict()

        st.session_state["user"] = user
        st.session_state["config"] = {
            "user_segment": user_segment,
            "roas_fairness": roas_fairness,
            "explore_exploit": explore_exploit,
            "enforce_diversity": enforce_diversity
        }

        st.success("Simulation configuration saved. Switch tabs to continue.")

# ---------------------------------------------------------
# TAB 2 — PERSONALIZED RESULTS
# ---------------------------------------------------------

with tab2:
    st.header("Personalized Ranking Results")

    if "config" not in st.session_state:
        st.info("Configure the simulation first in Tab 1.")
    else:
        user = st.session_state["user"]
        config = st.session_state["config"]

        ranked_df = rank_products(
            user,
            st.session_state["products"],
            config
        )

        st.subheader(f"User Segment: {user['segment']}")
        st.write(f"Interests: {user['interests']}")

        st.dataframe(ranked_df.head(20))

        st.session_state["ranked_df"] = ranked_df

# ---------------------------------------------------------
# TAB 3 — ADS & AUCTION
# ---------------------------------------------------------

with tab3:
    st.header("Ads & Auction Results")

    if "config" not in st.session_state:
        st.info("Configure the simulation first in Tab 1.")
    else:
        user = st.session_state["user"]
        config = st.session_state["config"]

        auction_df = run_auction(
            user,
            st.session_state["bids"],
            st.session_state["products"],
            st.session_state["sellers"],
            config
        )

        st.dataframe(auction_df.head(15))

        st.session_state["auction_df"] = auction_df

# ---------------------------------------------------------
# TAB 4 — METRICS DASHBOARD
# ---------------------------------------------------------

with tab4:
    st.header("Marketplace Metrics")

    if "auction_df" not in st.session_state:
        st.info("Run the simulation first.")
    else:
        auction_df = st.session_state["auction_df"]
        sellers_df = st.session_state["sellers"]

        # Fake impressions for now (each auction result = 1 impression)
        impressions_df = auction_df[["seller_id", "product_id"]].copy()

        # Fake events (no real clicks yet)
        events_df = pd.DataFrame(columns=["event_type", "product_id"])

        ctr = compute_ctr(events_df)
        conversion = compute_conversion(events_df)
        roas = compute_roas(auction_df, events_df)
        diversity = compute_seller_diversity(impressions_df)
        small_seller_share = compute_small_seller_share(impressions_df, sellers_df)

        st.metric("CTR", ctr)
        st.metric("Conversion Rate", conversion)
        st.metric("ROAS", roas)
        st.metric("Seller Diversity Index", diversity)
        st.metric("Small Seller Share", small_seller_share)

        st.write("Impressions by Seller")
        st.bar_chart(impressions_df["seller_id"].value_counts())
