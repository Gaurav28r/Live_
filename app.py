import streamlit as st
import requests
import re
import statistics

# MUST BE THE FIRST COMMAND!
st.set_page_config(page_title="Live Price Aggregator", page_icon="⚡")

# ==========================================
# 1. THE ENGINE (Backend Logic)
# ==========================================
def fetch_live_prices(product_name):
    # PASTE YOUR SERPAPI KEY HERE
    API_KEY = st.secrets["SERPAPI_KEY"] 
    
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "gl": "in",      # Country: India
        "hl": "en",      # Language: English
        "api_key": API_KEY
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("shopping_results", [])
    return []

def clean_price_string(price_str):
    """
    Converts messy strings like '₹1,50,000.00' into a clean float '150000.00' 
    so the computer can do math on it.
    """
    try:
        # Removes everything except numbers and decimals
        clean_num = re.sub(r'[^\d.]', '', str(price_str))
        return float(clean_num)
    except:
        return float('inf') # If there's an error, make it artificially high so it doesn't win

# ==========================================
# --- SIDEBAR: OPTIONAL BUDGET ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("### 🎯 Filtering Options")
    
    # Optional Max Budget: If left at 0, we treat it as "No Limit"
    max_input = st.number_input("Maximum Budget (₹) [Set 0 for No Limit]", min_value=0, value=0, step=1000)
    max_budget = max_input if max_input > 0 else float('inf')
    
    st.divider()
    st.info("Active Gatekeeper: This app now pings every store link to ensure it is live before showing it to you.")

# --- MAIN DASHBOARD ---
st.title("⚡ Live Price Aggregator")
st.markdown("Search across verified Indian stores in real-time.")

user_query = st.text_input("What do you want to buy? (e.g., 'Oats', 'PS5')")

if st.button("Find Lowest Price", type="primary") and user_query:
    with st.spinner(f"Validating live links for {user_query}..."):
        results = fetch_live_prices(user_query)
        
        if not results:
            st.error("No results found. Try being more specific.")
        else:
            # 1. PRE-FILTERING: Calculate Median for Outlier Detection
            all_prices = [clean_price_string(i.get("price")) for i in results]
            all_prices = [p for p in all_prices if p < float('inf')]
            dynamic_floor = statistics.median(all_prices) * 0.4 if all_prices else 0

            # 2. THE GATEKEEPER: Connectivity & Genuine Check
            valid_items = []
            TRUSTED_STORES = ['amazon', 'flipkart', 'croma', 'reliance', 'jiomart', 'tata', 'samsung', 'apple']
            exclude_words = ['rent', 'rental', 'case', 'cover', 'skin', 'cable', 'used', 'refurbished', 'empty box']

            # We only check the Top 10 results to keep the app fast
            for item in results[:10]: 
                num_price = clean_price_string(item.get("price"))
                title_lower = item.get('title', '').lower()
                link = item.get('link', item.get('product_link'))

                # Layer 1: Price & Keyword Check
                if dynamic_floor <= num_price <= max_budget:
                    if not any(bw in title_lower for bw in exclude_words):
                        
                        # Layer 2: LIVE LINK VALIDATION (The Gatekeeper)
                        try:
                            # We send a tiny 'ping' with a 2-second timeout
                            check = requests.head(link, timeout=2, allow_redirects=True)
                            if check.status_code < 400: # 200 or 300 range means the link works!
                                item['numeric_price'] = num_price
                                item['is_trusted'] = any(t in item.get('source','').lower() for t in TRUSTED_STORES)
                                valid_items.append(item)
                        except:
                            continue # If the link times out or fails, skip it silently!

            # 3. DISPLAY RESULTS
            valid_items.sort(key=lambda x: x['numeric_price'])

            if valid_items:
                st.success(f"🎯 Found {len(valid_items)} verified live deals!")
                
                cols = st.columns(min(len(valid_items), 3))
                for i, item in enumerate(valid_items[:3]):
                    with cols[i]:
                        st.subheader(f"Option #{i+1}")
                        st.metric(label=item.get('source'), value=f"₹{item['numeric_price']:,.2f}")
                        
                        # Added fallback just in case link is missing
                        final_link = item.get('link', item.get('product_link', 'https://google.com/shopping'))
                        st.link_button(f"🛒 Buy Now", final_link)
                
                st.divider()
                st.write("### All Verified Offers:")
                comparison_data = []
                for item in valid_items:
                    comparison_data.append({
                        "Store": item.get('source'),
                        "Price": f"₹{item['numeric_price']:,.2f}",
                        "Status": "✅ Live & Working",
                        "Product": item.get('title')
                    })
                st.dataframe(comparison_data, use_container_width=True)
            else:
                st.warning("All found links were either broken, rentals/accessories, or didn't match your budget.")