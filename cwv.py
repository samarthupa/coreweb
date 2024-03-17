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
    
    lcp_score = sum(lcp_scores) if lcp_scores else 0
    cls_score = sum(cls_scores) if cls_scores else 0
    fid_score = sum(fid_scores) if fid_scores else 0
    
    return lcp_score, cls_score, fid_score

# Function to categorize scores
def categorize_score(score, metric):
    if metric == "largest_contentful_paint":
        if score <= 2500:
            return "Good"
        elif 2500 < score <= 4000:
            return "Needs Improvement"
        else:
            return "Poor"
    elif metric == "cumulative_layout_shift":
        if score <= 0.1:
            return "Good"
        elif 0.1 < score <= 0.25:
            return "Needs Improvement"
        else:
            return "Poor"
    elif metric == "experimental_time_to_first_byte":
        if score <= 100:
            return "Good"
        elif 100 < score <= 300:
            return "Needs Improvement"
        else:
            return "Poor"

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
        
        st.subheader("Largest Contentful Paint (LCP)")
        st.write("Score:", lcp_score)
        st.write("Category:", categorize_score(lcp_score, "largest_contentful_paint"))
        
        st.subheader("Cumulative Layout Shift (CLS)")
        st.write("Score:", cls_score)
        st.write("Category:", categorize_score(cls_score, "cumulative_layout_shift"))
        
        st.subheader("Experimental Time to First Byte (FID)")
        st.write("Score:", fid_score)
        st.write("Category:", categorize_score(fid_score, "experimental_time_to_first_byte"))
    else:
        st.warning("Please enter the URL and API Key.")
