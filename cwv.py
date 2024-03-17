import streamlit as st
import requests

def fetch_crux_data(url):
    api_url = f'https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=AIzaSyANOzNJ4C4f2Ng5Ark4YzyWelNe-WBblug'
    body = {
        "url": url,
        "metrics": [
            {"name": "first_contentful_paint"},
            {"name": "cumulative_layout_shift"},
            {"name": "largest_contentful_paint"},
            {"name": "first_input_delay"}
        ],
        "formFactor": "PHONE",
        "device": "all",
        "endDate": "2024-03-17", # Change to today's date
        "startDate": "2024-02-17", # Change to 28 days before today's date
    }
    response = requests.post(api_url, json=body)
    return response.json()

def calculate_score(metrics_data):
    lcp_density = metrics_data['first_contentful_paint']['histogram'][0]['density']
    cls_density = metrics_data['cumulative_layout_shift']['histogram'][0]['density']
    inp_density = metrics_data['first_input_delay']['histogram'][0]['density']
    
    lcp_score = lcp_density * 1000
    cls_score = cls_density * 1000
    inp_score = inp_density * 1000
    
    return lcp_score, cls_score, inp_score

def main():
    st.title("Core Web Vitals Metrics Calculator")
    url = st.text_input("Enter URL:")
    if st.button("Calculate"):
        if not url:
            st.error("Please enter a valid URL.")
            return
        try:
            crux_data = fetch_crux_data(url)
            lcp_score, cls_score, inp_score = calculate_score(crux_data)
            st.success(f"Largest Contentful Paint (LCP) Score: {lcp_score}")
            st.success(f"Cumulative Layout Shift (CLS) Score: {cls_score}")
            st.success(f"Input Delay (FID) Score: {inp_score}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
