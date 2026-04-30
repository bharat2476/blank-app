import streamlit as st
import pandas as pd

from data_generator import generate_users, generate_sellers, generate_products, generate_bids
from ranking import rank_products, ribbon_products, shoe_email_status
from auction import run_auction
from metrics import (
    compute_ctr,
    compute_conversion,
    compute_roas,
    compute_seller_diversity,
    compute_small_seller_share
)

st.set_page_config(page_title="Nike Personalization Engine Simulator", layout="wide")

st.title("Nike Hyper Personalization & Marketing Technology Simulator")
st.caption(
    "Portfolio demo for product recommendations, sale/trending merchandising, "
    "explore-vs-exploit ranking, and lifecycle email suppression."
)

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
    "Member & Strategy",
    "Recommendations",
    "Marketing & Ads",
    "Portfolio Metrics"
])

# ---------------------------------------------------------
# TAB 1 — SIMULATION CONFIG
# ---------------------------------------------------------

with tab1:
    st.header("Member & Strategy Configuration")
    users_df = st.session_state["users"]
    products_df = st.session_state["products"]

    metric_cols = st.columns(4)
    metric_cols[0].metric("Demo Products", f"{len(products_df):,}")
    metric_cols[1].metric("Demo Members", f"{len(users_df):,}")
    metric_cols[2].metric("Repeat Customers", int((users_df["customer_type"] == "Repeat").sum()))
    metric_cols[3].metric("New Customers", int((users_df["customer_type"] == "New").sum()))

    st.write(
        "This simulator combines behavioral signals, browser intent, Nike app signals, "
        "customer lifecycle, and merchandising goals into one recommendation platform."
    )

    user_segment = st.selectbox("Select Member Segment", sorted(users_df["segment"].unique()))
    customer_type = st.selectbox("Customer Type", ["All", "Repeat", "New"])
    gender = st.selectbox("Member Gender", ["All", "Men", "Women"])
    candidate_users = users_df[users_df["segment"] == user_segment]
    if customer_type != "All":
        candidate_users = candidate_users[candidate_users["customer_type"] == customer_type]
    if gender != "All":
        candidate_users = candidate_users[candidate_users["gender"] == gender]
    if candidate_users.empty:
        st.warning("No member matches this combination. Broaden the filters.")
        st.stop()

    selected_user_id = st.selectbox(
        "Demo Member",
        candidate_users["user_id"].tolist(),
        format_func=lambda user_id: (
            f"{candidate_users[candidate_users['user_id'] == user_id].iloc[0]['customer_name']} "
            f"({candidate_users[candidate_users['user_id'] == user_id].iloc[0]['customer_type']}, "
            f"{candidate_users[candidate_users['user_id'] == user_id].iloc[0]['gender']})"
        )
    )
    selected_user = users_df[users_df["user_id"] == selected_user_id].iloc[0].to_dict()

    roas_fairness = st.slider(
        "ROAS vs Diversity Optimization",
        0, 100, 50
    )

    explore_exploit = st.slider(
        "Explore vs Exploit",
        0, 100, 50
    )

    audience_filter = st.selectbox("Merchandising Audience Dropdown", ["All", "Men", "Women", "Kids"])
    product_type_filter = st.selectbox("Product Dropdown", ["All", "Footwear", "Apparel", "Accessories"])
    enforce_diversity = st.checkbox("Enforce Channel Diversity Guardrail", value=True)

    st.subheader("Signals Available")
    st.json({
        "behavioral_interests": selected_user["interests"],
        "browser_signal": selected_user["browser_signal"],
        "nike_app_signals": selected_user["app_signals"],
        "last_shoe_purchase_days_ago": selected_user["last_shoe_purchase_days_ago"],
        "email_opt_in": selected_user["email_opt_in"],
    })

    if st.button("Run Simulation"):
        st.session_state["user"] = selected_user
        st.session_state["config"] = {
            "user_segment": user_segment,
            "roas_fairness": roas_fairness,
            "explore_exploit": explore_exploit,
            "audience_filter": audience_filter,
            "product_type_filter": product_type_filter,
            "enforce_diversity": enforce_diversity,
            "seed": selected_user_id + explore_exploit
        }

        st.success("Simulation saved. Open Recommendations and Marketing & Ads.")

# ---------------------------------------------------------
# TAB 2 — PERSONALIZED RESULTS
# ---------------------------------------------------------

with tab2:
    st.header("Personalized Recommendations")

    if "config" not in st.session_state:
        st.info("Configure the member strategy first in Tab 1.")
    else:
        user = st.session_state["user"]
        config = st.session_state["config"]
        products_df = st.session_state["products"]

        ranked_df = rank_products(
            user,
            products_df,
            config
        )
        filtered_ranked_df = ranked_df.copy()
        if config["audience_filter"] != "All":
            filtered_ranked_df = filtered_ranked_df[filtered_ranked_df["audience"] == config["audience_filter"]]
        if config["product_type_filter"] != "All":
            filtered_ranked_df = filtered_ranked_df[filtered_ranked_df["product_type"] == config["product_type_filter"]]

        st.subheader(f"{user['customer_name']} | {user['segment']} | {user['customer_type']}")
        st.write(f"Interests: {user['interests']} | Browser: {user['browser_signal']} | Apps: {user['app_signals']}")

        ribbon_cols = st.columns(2)
        with ribbon_cols[0]:
            st.subheader("Ribbon: Products on Sale")
            st.dataframe(
                ribbon_products(products_df, "Sale", config["audience_filter"], config["product_type_filter"])
                .head(8)[["name", "category", "audience", "product_type", "price", "discount_pct"]],
                use_container_width=True
            )
        with ribbon_cols[1]:
            st.subheader("Ribbon: Trending Products")
            st.dataframe(
                ribbon_products(products_df, "Trending", config["audience_filter"], config["product_type_filter"])
                .head(8)[["name", "category", "audience", "product_type", "price", "trend_score"]],
                use_container_width=True
            )

        st.subheader("Recommended Products")
        st.dataframe(
            filtered_ranked_df.head(20)[[
                "name", "category", "audience", "product_type", "price",
                "is_on_sale", "discount_pct", "trend_score", "interest_score",
                "browser_score", "app_score", "final_score"
            ]],
            use_container_width=True
        )

        st.session_state["ranked_df"] = filtered_ranked_df

# ---------------------------------------------------------
# TAB 3 — ADS & AUCTION
# ---------------------------------------------------------

with tab3:
    st.header("Marketing & Ads")

    if "config" not in st.session_state:
        st.info("Configure the member strategy first in Tab 1.")
    else:
        user = st.session_state["user"]
        config = st.session_state["config"]

        st.subheader("Lifecycle Email Decision")
        st.info(shoe_email_status(user))
        st.write(
            "Rule: if the member just bought footwear, suppress shoe emails. "
            "Running shoe emails resume when the member reaches 5.5 months since last shoe purchase."
        )

        auction_df = run_auction(
            user,
            st.session_state["bids"],
            st.session_state["products"],
            st.session_state["sellers"],
            config
        )

        st.subheader("Sponsored Product Auction")
        st.dataframe(auction_df.head(15), use_container_width=True)

        st.session_state["auction_df"] = auction_df

# ---------------------------------------------------------
# TAB 4 — METRICS DASHBOARD
# ---------------------------------------------------------

with tab4:
    st.header("Portfolio Metrics & Open Pain Points")

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
        st.metric("Channel Diversity Share", small_seller_share)

        st.write("Impressions by Nike Channel")
        st.bar_chart(impressions_df["seller_id"].value_counts())

    st.subheader("Additional Pain Points to Address")
    st.markdown(
        """
        - Cold-start ranking for anonymous visitors with sparse behavioral history.
        - Identity stitching across web, retail, Nike App, SNKRS, and Nike Run Club.
        - Size availability, inventory constraints, and local fulfillment promises.
        - Frequency capping so marketing and onsite recommendations do not over-message.
        - Privacy, consent, and regional data retention controls.
        - Explainability for why a product was recommended.
        - Fairness checks across gender, age groups, and sport communities.
        - Incrementality measurement to prove recommendations caused lift.
        """
    )
