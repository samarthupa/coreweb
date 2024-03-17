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
            "experimental_first_input_delay"
        ]
    }
    response = requests.post(endpoint, params=params, json=data)
    return response.json()

# Function to calculate Core Web Vitals scores
def calculate_core_web_vitals_scores(metrics_data):
    lcp_scores = metrics_data["record"]["metrics"]["largest_contentful_paint"]["histogramTimeseries"][-1]["densities"]
    cls_scores = metrics_data["record"]["metrics"]["cumulative_layout_shift"]["histogramTimeseries"][-1]["densities"]
    fid_scores = metrics_data["record"]["metrics"]["experimental_first_input_delay"]["histogramTimeseries"][-1]["densities"]
    
    lcp_score = sum(lcp_scores)
    cls_score = sum(cls_scores)
    fid_score = sum(fid_scores)
    
    return lcp_score, cls_score, fid_score

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
        lcp_score, cls_score, fid_score = calculate_core_web_vitals_scores(metrics_data)
        st.write("Largest Contentful Paint (LCP) Score:", lcp_score)
        st.write("Cumulative Layout Shift (CLS) Score:", cls_score)
        st.write("First Input Delay (FID) Score:", fid_score)
    else:
        st.warning("Please enter the URL and API Key.")
