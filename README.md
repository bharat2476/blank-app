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
- Sale and trending product ribbons.
- Dropdown filtering for men, women, kids, footwear, apparel, and accessories.
- Shoe email suppression when a member recently purchased footwear.
- Running shoe email reactivation after the 5.5 month replenishment window.
- Sponsored product auction and portfolio metrics.
- Product pain points to discuss in interviews and roadmap conversations.

## How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
   ```
