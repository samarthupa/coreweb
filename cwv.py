import streamlit as st
import requests

# Function to fetch CrUX History API data
def fetch_crux_history_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key={api_key}"
    payload = {
        "origin": url,
        "metrics": [
            "largest_contentful_paint",
            "cumulative_layout_shift",
            "first_input_delay",
            "first_contentful_paint",
            "experimental_time_to_first_byte"
        ]
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()["record"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX History API data: {e}")
        return None

# Main function for Streamlit app
def main():
    st.title("CrUX History API Data Fetcher")

    # Input URL and API key
    url = st.text_input("Enter a URL or origin:")
    api_key = st.text_input("Enter your CrUX API key:")

    # Fetch CrUX History API data on button click
    if st.button("Fetch CrUX History API Data"):
        if not api_key:
            st.error("Please enter your CrUX API key.")
        elif not url:
            st.error("Please enter a URL or origin.")
        else:
            crux_history_data = fetch_crux_history_data(url, api_key)
            if crux_history_data:
                st.write("**Core Web Vitals Assessment:**")
                cls_values = []
                inp_values = []
                lcp_values = []
                metrics = crux_history_data.get("metrics", {})
                collection_periods = crux_history_data.get("collectionPeriods", [])
                for metric_name, metric_data in metrics.items():
                    if metric_name == "cumulative_layout_shift":
                        for bin_data in metric_data["histogramTimeseries"]:
                            densities = bin_data.get("densities", [])
                            cls_values.extend(densities[-28:])  # Taking last 28 days
                    elif metric_name == "first_input_delay":
                        for bin_data in metric_data["histogramTimeseries"]:
                            densities = bin_data.get("densities", [])
                            inp_values.extend(densities[-28:])  # Taking last 28 days
                    elif metric_name == "largest_contentful_paint":
                        for bin_data in metric_data["histogramTimeseries"]:
                            densities = bin_data.get("densities", [])
                            lcp_values.extend(densities[-28:])  # Taking last 28 days
                
                # Calculate average values
                avg_cls = sum(cls_values) / len(cls_values) if cls_values else 0
                avg_inp = sum(inp_values) / len(inp_values) if inp_values else 0
                avg_lcp = sum(lcp_values) / len(lcp_values) if lcp_values else 0
                
                st.write("Failed" if avg_cls > 0.1 else "Passed")
                st.write("**Core Web Vitals Metrics:**")
                st.write(f"Largest Contentful Paint (LCP): {avg_lcp:.1f} s")
                st.write(f"Interaction to Next Paint (INP): {avg_inp:.0f} ms")
                st.write(f"Cumulative Layout Shift (CLS): {avg_cls:.2f}")
                
                st.write("**Other Notable Metrics:**")
                # You can add other metrics here and calculate their averages as well
                
            else:
                st.warning("No CrUX History API data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
