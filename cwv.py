import streamlit as st
import requests

# Function to fetch CrUX data
def fetch_crux_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={api_key}"
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
                st.write("**Core Web Vitals Assessment:**")
                lcp = crux_data.get("metrics", {}).get("largest_contentful_paint", {}).get("percentiles", {}).get("p75")
                cls = crux_data.get("metrics", {}).get("cumulative_layout_shift", {}).get("percentiles", {}).get("p75")
                fid = crux_data.get("metrics", {}).get("first_input_delay", {}).get("percentiles", {}).get("p75")
                fcp = crux_data.get("metrics", {}).get("first_contentful_paint", {}).get("percentiles", {}).get("p75")
                ttfb = crux_data.get("metrics", {}).get("experimental_time_to_first_byte", {}).get("percentiles", {}).get("p75")
                inp = crux_data.get("metrics", {}).get("interaction_to_next_paint", {}).get("percentiles", {}).get("p75")
                
                st.write("Expand view")
                st.write(f"Largest Contentful Paint (LCP): {lcp} ms")
                st.write(f"Cumulative Layout Shift (CLS): {cls}")
                st.write(f"First Input Delay (FID): {fid} ms")
                st.write(f"First Contentful Paint (FCP): {fcp} ms")
                st.write(f"Time to First Byte (TTFB): {ttfb} ms")
                st.write(f"Interaction to Next Paint (INP): {inp} ms")
            else:
                st.warning("No CrUX data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
