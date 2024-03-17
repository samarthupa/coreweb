import streamlit as st
import requests

# CrUX API endpoint (replace with your desired data source if needed)
CRUX_API_URL = "https://chromeuxreport.googleapis.com/v1/browsingData"

# Function to fetch CrUX data for a URL and date range
def fetch_crux_data(url, start_date, end_date):
    params = {
        "url": url,
        "keys": "largestContentfulPaint,cumulativeLayoutShift,firstInputDelay",
        "filter": f"date >= '{start_date}' AND date <= '{end_date}'",
    }
    headers = {"Authorization": "Bearer AIzaSyANOzNJ4C4f2Ng5Ark4YzyWelNe-WBblug"}  # Replace with your CrUX API key

    try:
        response = requests.get(CRUX_API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX data: {e}")
        return None

# Streamlit app layout
st.title("CrUX Data Fetcher")

url = st.text_input("Enter URL:")
if not url:
    st.warning("Please enter a valid URL.")

if url:
    # Calculate date range for the last 28 days
    today = datetime.datetime.now()
    start_date = (today - datetime.timedelta(days=28)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    # Fetch CrUX data
    crux_data = fetch_crux_data(url, start_date, end_date)

    # Display results (handle potential missing data gracefully)
    if crux_data:
        if "aggregations" in crux_data:
            for metric, data in crux_data["aggregations"].items():
                if data:
                    st.write(f"{metric.upper()}: {data['percentiles']['75']}")  # Display 75th percentile
                else:
                    st.warning(f"No data available for {metric.upper()}")
        else:
            st.warning("No CrUX data found for the specified URL and date range.")
    else:
        st.warning("An error occurred while fetching CrUX data.")
