# ⚡ Live Price Aggregator

**[🚀 Click here to try the Live Web App!](https://gaurav28r-live--app-hdhdog.streamlit.app/)**

An intelligent, real-time e-commerce price comparison engine built with Python and Streamlit. This tool bypasses traditional, fragile web scrapers by utilizing the Google Shopping API to fetch live market data from verified Indian retailers like Amazon, Flipkart, Croma, and Reliance Digital.

---

## 🧠 The Engineering Problem
Online shoppers suffer from price fragmentation, but building a robust price tracker is difficult because internet data is incredibly "dirty." API queries for high-value items (like a PlayStation 5) frequently return cheap accessories, empty boxes, or daily rental rates that ruin basic sorting algorithms. Furthermore, smaller merchants often have broken affiliate links.

## 🛠️ The Solution
This application implements a **Dual-Layer Outlier Rejection System** and a **Live Connectivity Gatekeeper** to ensure the user only sees genuine, actionable deals.

---

## ✨ Core Features & Architecture

* **The "Median Anchor" Algorithm:** Instead of relying on manual price floors, the engine calculates the median price of all fetched results in real-time. It automatically rejects any item priced below 40% of the median, instantly eliminating fake prices, cases, and daily rentals.
* **The Gatekeeper (Live Link Validation):** Before displaying a "winning" deal, the backend fires a lightning-fast HTTP `HEAD` request to the merchant's URL with a 2-second timeout. If the store's server is down or the link is broken, the deal is discarded.
* **NLP Keyword Exclusion:** A text-processing layer scans product titles and quietly drops items containing keywords like `'rent'`, `'empty box'`, or `'refurbished'`.
* **Trust-Weighted Ranking:** Verified "Tier 1" merchants are visually highlighted and prioritized, ensuring users don't fall for suspiciously cheap prices from unverified domains.
* **Dynamic Budget Filtering:** Users can optionally set a maximum budget ceiling to filter results.

---

## 💻 Tech Stack & Dependencies

**Language:** Python 3.x
**Frontend Framework:** Streamlit
**Core Libraries:**
* `requests` - For handling REST API calls and the Gatekeeper `HEAD` pings.
* `re` (Regex) - For cleaning chaotic price strings (e.g., converting '₹1,50,000.00' to `150000.00`).
* `statistics` - For the Median Anchor math logic.
**External API:** SerpApi (Google Shopping API)

---

## ⚙️ How to Run Locally

If you want to clone this repository and run the engine on your own machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Gaurav28r/Live_Aggregator.git](https://github.com/Gaurav28r/Live_Aggregator.git)
   cd Live_Aggregator
   
## 👨‍💻 Author

**Gaurav Verma**
*Computer Science & Engineering (AIML) Student*<br>
Built as a project focusing on API integration, algorithmic data cleaning, and secure cloud deployment.
