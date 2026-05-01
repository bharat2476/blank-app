# Nike Hyper Personalization & Marketing Technology Simulator

This Streamlit portfolio app demonstrates a recommendation engine and marketing
technology platform for Nike products. It simulates how behavioral signals,
browser intent, Nike app signals, customer lifecycle, and merchandising goals can
work together to recommend products and decide when marketing emails should be
suppressed or reactivated.

## Demo scope

- 500 generated Nike products across sport categories, audiences, and product
  types.
- 100 generated Nike members split across repeat and new customers, men and
  women, demographics, browser signals, and Nike app usage.
- Explore-vs-exploit ranking for repeat and new customers.
- Lifecycle orchestration for new visitors, first-purchase prospects, repeat
  runners, lapsed runners, active members, and high-value members.
- Privacy modes for full consent, limited consent, and no app usage data.
- Explainable recommendation labels for interview storytelling.
- Sale and trending product ribbons.
- Dropdown filtering for men, women, kids, footwear, apparel, and accessories.
- Shoe email suppression when a member recently purchased footwear.
- Running shoe email reactivation after the 5.5 month replenishment window.
- Nike Run-style shoe usage signals, frequency caps, channel preferences, and
  consent-aware Martech email decisions.
- Simulated A/B experiment metrics and executive business impact estimates.
- Dedicated A/B Testing Lab with hypothesis, population, randomization unit,
  traffic allocation, sample assumptions, primary metric, guardrails, variants,
  result readout, and launch checklist.
- Sponsored product auction and portfolio metrics.
- Responsible AI, privacy guardrails, reference architecture, and product pain
  points to discuss in interviews and roadmap conversations.
- Architecture Diagram tab to visualize end-to-end product workflow.

## Current app tabs

1. Member & Strategy
2. Recommendations
3. Marketing & Ads
4. Portfolio Metrics
5. A/B Testing Lab
6. Responsible AI
7. Architecture Diagram

## Member selection criteria

- Member segment
- Customer type
- Member gender
- Privacy preference (how much the user wants to share)

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
- Nike app affinity signals
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

## How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
   ```
