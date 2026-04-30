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

## How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
   ```
