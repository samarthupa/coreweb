import streamlit as st
import requests

# Streamlit App Header
st.title('Core Web Vitals Checker')

# Function to Fetch CWV Data from CrUX API
def fetch_cwv_data(url):
    # Construct the API URL
    api_url = f'https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=AIzaSyANOzNJ4C4f2Ng5Ark4YzyWelNe-WBblug'
    # Construct the request payload
    payload = {
        "url": url,
        "metrics": [
            {"metric": "cumulative_layout_shift"},
            {"metric": "largest_contentful_paint"},
            {"metric": "first_input_delay"}
        ],
        "dateRange": {"startDate": "2023-02-01", "endDate": "2023-02-28"},
        "formFactor": "PHONE",
        "effectiveConnectionType": "4G"
    }
    # Make a POST request to the CrUX API
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data. Please try again later.")
        return None

# Streamlit App Interface
url = st.text_input('Enter URL:')
if st.button('Fetch CWV Data'):
    if url:
        cwv_data = fetch_cwv_data(url)
        if cwv_data:
            # Display CWV Data
            st.write(cwv_data)
    else:
        st.warning('Please enter a URL.')
