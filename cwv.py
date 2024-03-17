import requests
import streamlit as st

# Function to query CrUX History API and fetch Core Web Vitals metrics
def fetch_core_web_vitals_metrics(url, api_key):
    endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord"
    params = {"key": api_key}
    data = {
        "url": url,
        "metrics": [
            "largest_contentful_paint",
            "cumulative_layout_shift",
            "experimental_time_to_first_byte"
        ]
    }
    response = requests.post(endpoint, params=params, json=data)
    return response.json()

# Function to calculate Core Web Vitals scores
def calculate_core_web_vitals_scores(metrics_data):
    metrics = metrics_data.get("record", {}).get("metrics", {})
    lcp_scores = metrics.get("largest_contentful_paint", {}).get("histogramTimeseries", [])[-1].get("densities", [])
    cls_scores = metrics.get("cumulative_layout_shift", {}).get("histogramTimeseries", [])[-1].get("densities", [])
    fid_scores = metrics.get("experimental_time_to_first_byte", {}).get("histogramTimeseries", [])[-1].get("densities", [])
    
    # Convert LCP score to seconds
    lcp_score_sec = sum(lcp_scores) / 1000 if lcp_scores else 0
    
    # FID scores are already in milliseconds
    fid_score_ms = sum(fid_scores) if fid_scores else 0
    
    # Convert CLS score to PSI format (multiply by 100 to get a percentage)
    cls_score_psi = sum(cls_scores) * 100 if cls_scores else 0
    
    return lcp_score_sec, cls_score_psi, fid_score_ms

# Streamlit app
st.title("Core Web Vitals Metrics")

# Input fields
url = st.text_input("Enter URL:", "https://example.com")
api_key = st.text_input("Enter API Key:")

# Fetch and display Core Web Vitals metrics
if st.button("Fetch Metrics"):
    if url and api_key:
        st.write("Fetching Core Web Vitals metrics...")
        metrics_data = fetch_core_web_vitals_metrics(url, api_key)
        lcp_score_sec, cls_score_psi, fid_score_ms = calculate_core_web_vitals_scores(metrics_data)
        st.write("Largest Contentful Paint (LCP) Score:", lcp_score_sec, "seconds")
        st.write("Cumulative Layout Shift (CLS) Score:", cls_score_psi, "%")
        st.write("First Input Delay (FID) Score:", fid_score_ms, "milliseconds")
    else:
        st.warning("Please enter the URL and API Key.")
