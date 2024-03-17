import streamlit as st
import requests

# Function to fetch CrUX History API data
def fetch_crux_history_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key={api_key}"
    payload = {
        "origin": url,  # Assuming the input URL is the origin
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
                st.write("**Metrics Averaged Over 28-Day Periods:**")
                metrics = crux_history_data.get("metrics", {})
                collection_periods = crux_history_data.get("collectionPeriods", [])

                for metric_name, metric_data in metrics.items():
                    st.write(f"**{metric_name.capitalize()}**:")
                    for period_index, period in enumerate(collection_periods):
                        start_date = period.get("firstDate", {})
                        end_date = period.get("lastDate", {})
                        start_str = f"{start_date.get('year', '')}-{start_date.get('month', '')}-{start_date.get('day', '')}"
                        end_str = f"{end_date.get('year', '')}-{end_date.get('month', '')}-{end_date.get('day', '')}"
                        st.write(f"Period {period_index + 1}: From {start_str} to {end_str}")
                        if "histogramTimeseries" in metric_data:
                            for bin_data in metric_data["histogramTimeseries"]:
                                densities = bin_data.get("densities", [])
                                st.write(f"  - Densities: {densities}")
                        elif "percentilesTimeseries" in metric_data:
                            percentiles = metric_data["percentilesTimeseries"].get("p75s", [])
                            st.write(f"  - Percentiles (p75): {percentiles}")
                        elif "fractionTimeseries" in metric_data:
                            fractions = metric_data["fractionTimeseries"]
                            for label, fraction_data in fractions.items():
                                fractions_values = fraction_data.get("fractions", [])
                                st.write(f"  - Fractions for {label}: {fractions_values}")
                        st.write("")  # Add empty line for readability
            else:
                st.warning("No CrUX History API data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
