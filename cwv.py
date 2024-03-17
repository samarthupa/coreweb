import streamlit as st
import requests

# Function to fetch CrUX data
def fetch_crux_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key={api_key}"
    payload = {
        "url": url
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()["record"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX data: {e}")
        return None

# Main function for Streamlit app
def main():
    st.title("CrUX Data Fetcher")
    
    # Input URL and API key
    url = st.text_input("Enter a URL:")
    api_key = st.text_input("Enter your CrUX API key:")
    
    # Fetch CrUX data on button click
    if st.button("Fetch CrUX Data"):
        if not api_key:
            st.error("Please enter your CrUX API key.")
        else:
            crux_data = fetch_crux_data(url, api_key)
            if crux_data:
                st.write("**CrUX Data:**")
                metrics = crux_data.get("metrics", {})
                for metric_name, metric_data in metrics.items():
                    st.write(f"- {metric_name}:")
                    percentiles = metric_data.get("percentiles", {})
                    if percentiles:
                        for percentile, value in percentiles.items():
                            st.write(f" - Percentile {percentile}: {value}")
                        average_value = sum(percentiles.values()) / len(percentiles)
                        st.write(f" - Average: {average_value}")
                    else:
                        st.write(" - No percentile data available.")
            else:
                st.warning("No CrUX data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
