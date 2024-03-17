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

# Function to convert densities to metrics values
def convert_densities_to_metrics(densities):
    # Assuming the density represents the proportion of user experiences within that range
    # and the range values correspond to milliseconds
    total_samples = sum(densities)
    metric_value = sum(start * density for start, density in enumerate(densities)) / total_samples
    return metric_value

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
                st.write("**Most Recent Period Metrics:**")
                metrics = crux_history_data.get("metrics", {})

                for metric_name, metric_data in metrics.items():
                    st.write(f"**{metric_name.capitalize()}**:")
                    if "histogramTimeseries" in metric_data:
                        bin_data = metric_data["histogramTimeseries"][-1]  # Get data for most recent period
                        densities = bin_data.get("densities", [])
                        metric_value = convert_densities_to_metrics(densities)
                        st.write(f"  - Metric Value: {metric_value} milliseconds")
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
