# Personalization & Ad Targeting Simulator

This Streamlit portfolio app demonstrates a recommendation engine and marketing
technology platform for a digital marketplace. It simulates how behavioral signals,
browser intent, app signals, customer lifecycle, and merchandising goals can
work together to recommend products and decide when marketing emails should be
suppressed or reactivated.

Core UI logic lives in `streamlit_app.py`. MarTech signal processing, hybrid ranking,
and propensity-gated notifications are encapsulated in `martech_engine.py`.

## Demo scope

- 500 generated products across sport categories, audiences, and product
  types.
- 100 generated members split across repeat and new customers, men and
  women, demographics, browser signals, and app usage.
- Explore-vs-exploit ranking for repeat and new customers.
- Lifecycle orchestration for new visitors, first-purchase prospects, repeat
  runners, lapsed runners, active members, and high-value members.
- Privacy modes for full consent, limited consent, and no app usage data.
- Explainable recommendation labels for interview storytelling.
- Sale and trending product ribbons.
- Dropdown filtering for men, women, kids, footwear, apparel, and accessories.
- Shoe email suppression when a member recently purchased footwear.
- Running shoe email reactivation after the 5.5 month replenishment window.
- App usage signals, frequency caps, channel preferences, and
  consent-aware Martech email decisions.
- Simulated A/B experiment metrics and executive business impact estimates.
- Dedicated A/B Testing Lab with hypothesis, population, randomization unit,
  traffic allocation, sample assumptions, primary metric, guardrails, variants,
  result readout, and launch checklist.
- Sponsored product auction and portfolio metrics.
- Trust & Safety, privacy guardrails, reference architecture, and product pain
  points to discuss in interviews and roadmap conversations.
- Architecture Diagram tab to visualize end-to-end product workflow.
- **MarTech engine** (`martech_engine.py`): mock Bronze → Silver → Gold medallion layers for 0-party and session behavioral signals.
- **Hybrid recommendations**: sidebar A/B variant (behavioral-only vs. 0-party + behavioral blend) with instant re-ranking on View/Click.
- **Live product grid** with per-card “Why am I seeing this?” captions driven by current member state.
- **Propensity-scored push notifications**: queue only when score > 0.75; inspect decisions in **MarTech Backend: Propensity Logs** (sidebar).

## Project structure

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Streamlit UI, tabs, session state, sidebar experiment controls |
| `martech_engine.py` | Medallion layers, hybrid ranking, interaction tracking, propensity scoring |
| `ranking.py` | Base 0-party ranking, lifecycle email rules, A/B simulation helpers |
| `data_generator.py` | Synthetic members, products, sellers, and ad bids |
| `auction.py` | Sponsored product auction scoring |
| `metrics.py` | CTR, conversion, ROAS, and diversity metrics |

## Current app tabs

1. Member & Strategy
2. Recommendations
3. Marketing & Ads
4. Portfolio Metrics
5. A/B Testing Lab
6. Trust & Safety
7. Architecture Diagram

## Sidebar controls

- **Recommendation Variant** — Variant A (behavioral-only) or Variant B (hybrid: 70% base ranker + 30% session behavioral).
- **MarTech Backend: Propensity Logs** — expandable log of push propensity evaluations (score, threshold, queued vs. suppressed).

## Quick start (demo flow)

1. Open **Member & Strategy**, pick a member, set privacy and sliders, then click **Run Simulation**.
2. Open **Recommendations** — use **View** / **Click** on the live product grid; ranking updates on each interaction without resetting the app.
3. Toggle **Recommendation Variant** in the sidebar to compare behavioral-only vs. hybrid ranking.
4. Open **Marketing & Ads** — review email rules and propensity-gated push (interact in Recommendations first to raise propensity above 0.75).
5. Explore **Portfolio Metrics**, **A/B Testing Lab**, **Trust & Safety**, and **Architecture Diagram** as needed.

## Interview framing (FAANG-style)

### Architecture principles

- User trust first: consent and communication controls gate personalization.
- Business + user balance: ranking and auction optimize outcomes while protecting relevance.
- Explainability by default: recommendations include plain-language rationale.
- Experiment-driven iteration: A/B testing drives rollout decisions with guardrails.

### Key trade-offs

- Relevance vs. exploration (precision vs. discovery)
- Revenue vs. fairness (monetization vs. marketplace diversity)
- Personalization depth vs. privacy (signal richness vs. data minimization)
- Velocity vs. risk (shipping speed vs. guardrail quality)

## Member selection criteria

- Member segment
- Customer type
- Member gender
- Privacy preference (how much the user wants to share)

## MarTech engine (medallion + propensity)

### Signal layers (mock semantic pipeline)

1. **Bronze** — raw 0-party inputs: interests, browser signal, segment, consent flags, app signals.
2. **Silver** — session behavioral aggregates: product views/clicks and category engagement.
3. **Gold** — unified member profile passed into ranking and Martech decisions (visible under **Semantic profile** on the Recommendations tab).

### Recommendation variants

| Variant | Behavior |
|---------|----------|
| **Variant A: Behavioral-Only** | Ranks primarily from session views/clicks plus popularity, trend, and recency. |
| **Variant B: Hybrid Model** | Blends the existing 0-party `rank_products()` score with `behavioral_score` (70% / 30%). |

Session interactions update `behavioral_score` per product and category in real time via Streamlit reruns.

### Push propensity (Marketing & Ads)

`propensity_score` (0.0–1.0) combines consent, session engagement, top-product relevance, and lifecycle stage. Push notifications are **queued only when score > 0.75** and lifecycle/channel gates allow. Email rules in `ranking.py` still apply separately.

## Scoring logic

### Recommendations tab scoring

- `interest_score`: `1.0` when product category matches member interests, else `0.0`.
- `browser_score`: `1.0` when browser intent matches category, or when intent is `Sale` and product is on sale, or `Trending` with trend >= 70; else `0.0`.
- `trend_score`: base trend signal from product catalog; used as normalized `trend_norm = trend_score / max(trend_score)`.
- `final_score`: weighted combination of personalization, business, lifecycle, and exploration components:

  `final_score =`
  `interest_score * 0.30 * exploit_weight`
  `+ audience_score * 0.18 * exploit_weight`
  `+ browser_score * 0.15 * exploit_weight`
  `+ app_score * 0.14 * exploit_weight`
  `+ popularity_norm * 0.12 * exploit_weight`
  `+ trend_norm * 0.06 * exploit_weight`
  `+ recency_norm * 0.05 * exploit_weight`
  `+ margin_score * lifecycle_boost`
  `+ trend_norm * discovery_boost`
  `+ lifecycle_score`
  `+ random_exploration(0..explore_weight)`

  Where:
  - `explore_weight = explore_exploit / 100`
  - `exploit_weight = 1 - explore_weight`
  - `lifecycle_boost = 0.12` for repeat members, else `0.0`
  - `discovery_boost = 0.12` for new members, else `0.0`

**Hybrid variant (Variant B)** additionally applies:

`final_score = base_final_score * 0.70 + behavioral_score * 0.30`

where `behavioral_score` is derived from per-product and per-category session views and clicks.

### Marketing & Ads tab scoring

- `relevance`: `1.0` when ad product category matches member interests, else `0.2`.
- `fairness_factor`: `1.25` for small sellers when diversity guardrail is enabled, else `1.0`.
- `final_score`:

  `roas_weight = roas_fairness / 100`  
  `fairness_weight = 1 - roas_weight`  
  `final_score = (bid_amount * roas_weight) + (relevance * 0.5) + (fairness_factor * fairness_weight)`

## Signals captured for scoring

- Member interests and lifecycle stage
- Browser intent signal
- App affinity signals
- Audience fit (Men/Women/Kids)
- Product trend, popularity, recency, and margin
- Seller type (`is_small_seller`)
- Bid amount
- Privacy preference and consent mode
- ROAS vs fairness and explore vs exploit controls

## Suggested additional signals

- Inventory and size availability by location
- Price affinity and discount sensitivity
- Return risk and fit confidence
- Session context (device, channel, time of day)
- Weather and seasonality
- Fulfillment promise (delivery speed)
- Campaign pacing, budget constraints, and ad quality
- Predicted CTR/CVR and post-click quality outcomes

## Example calculations

### Recommendations example

Assume:
- `explore_exploit = 30` => `explore_weight = 0.30`, `exploit_weight = 0.70`
- Repeat member => `lifecycle_boost = 0.12`, `discovery_boost = 0.0`
- `interest_score = 1.0`
- `audience_score = 1.0`
- `browser_score = 1.0`
- `app_score = 0.5`
- `popularity_norm = 0.8`
- `trend_norm = 0.7`
- `recency_norm = 0.9`
- `margin_score = 0.6`
- `lifecycle_score = 0.08`
- `random_exploration = 0.12`

Calculation:

`final_score =`
`(1.0*0.30*0.70) + (1.0*0.18*0.70) + (1.0*0.15*0.70) + (0.5*0.14*0.70) +`
`(0.8*0.12*0.70) + (0.7*0.06*0.70) + (0.9*0.05*0.70) + (0.6*0.12) +`
`(0.7*0.0) + 0.08 + 0.12`

`final_score = 0.8885` (approx.)

What changes this score most:
- Strongest positive levers are `interest_score`, `audience_score`, and `browser_score` because of their higher weights.
- For repeat members, `margin_score * lifecycle_boost` can materially move rank order.
- Increasing `explore_exploit` raises exploration noise and can reshuffle close-ranked products.

### Marketing & Ads example

Assume:
- `roas_fairness = 60` => `roas_weight = 0.60`, `fairness_weight = 0.40`
- `bid_amount = 1.80`
- `relevance = 1.0` (interest-category match)
- `fairness_factor = 1.25` (small seller + diversity on)

Calculation:

`final_score = (1.80*0.60) + (1.0*0.5) + (1.25*0.40)`

`final_score = 1.08 + 0.5 + 0.5 = 2.08`

What changes this score most:
- Higher `bid_amount` dominates when `roas_fairness` is set high.
- `relevance` strongly affects rank quality and keeps ads aligned with member intent.
- `fairness_factor` has larger impact when `roas_fairness` is lower (more fairness weight).

## View the live prototype

Anyone can open and view the deployed prototype using this public URL:

- https://blank-app-zwp52hqbzm2sxhgqckmv6w.streamlit.app/

No local setup is required for viewing. Open the link in any browser.

After pushing changes to GitHub, Streamlit Community Cloud redeploys from `main` (usually within a few minutes). If the live app looks stale:

1. Confirm the latest commit is on `origin/main` (includes `martech_engine.py`).
2. Open [share.streamlit.io](https://share.streamlit.io) → your app → verify **Repository** `bharat2476/blank-app`, **Branch** `main`, **Main file** `streamlit_app.py`.
3. Check deploy logs for errors, then **Reboot app** and hard-refresh the URL (Ctrl+F5).

**Signs the new build is live:** left sidebar shows **Experiment Controls** and **Recommendation Variant**; Recommendations tab includes **Live Product Grid**; Marketing & Ads includes **Push Notification (Propensity-Gated)**.

## How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
   ```

   The app serves on port **8501** by default.

3. Verify imports (optional)

   ```
   $ python -c "import streamlit_app"
   ```
