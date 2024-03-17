import streamlit as st
import requests
from datetime import datetime, timedelta


# Function to fetch CrUX History API data
def fetch_crux_history_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key={api_key}"
    today = datetime.utcnow()
    past_28_days = today - timedelta(days=28)

    payload = {
        "origin": url,
        "metrics": [
            "largest_contentful_paint",
            "cumulative_layout_shift",
            "first_input_delay",
        ],
        "startDate": past_28_days.strftime("%Y-%m-%d"),
        "endDate": today.strftime("%Y-%m-%d"),
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()["record"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX History API data: {e}")
        return None


# Function to calculate score from density data
def calculate_score(densities):
    if not densities:
        return None

    # Define thresholds (can be adjusted based on specific requirements)
    lcp_good_threshold = 2500
    cls_good_threshold = 0.1
    fid_good_threshold = 100

    total_density = sum(densities)
    score = 0

    # Calculate weighted score based on density distribution relative to thresholds
    for i, density in enumerate(densities):
        start = i * 500  # Assuming histogram bin size is 500ms
        end = start + 500

        # LCP - good = higher density in lower end of bin
        if metric_name == "largest_contentful_paint":
            weight = 1 - (end / lcp_good_threshold)
        # CLS - good = lower density throughout
        elif metric_name == "cumulative_layout_shift":
            weight = 1 - density
        # FID - good = higher density in lower end of bin
        else:
            weight = 1 - (end / fid_good_threshold)

        score += density * weight

    return score * 100 / total_density


# Main function for Streamlit app
def main():
    st.title("CrUX History API - Core Web Vitals")

    # Input URL and API key
    url = st.text_input("Enter a URL or origin:")
    api_key = st.text_input("Enter your CrUX API key:")

    # Fetch CrUX History API data on button click
    if st.button("Fetch Core Web Vitals"):
        if not api_key:
            st.error("Please enter your CrUX API key.")
        elif not url:
            st.error("Please enter a URL or origin.")
        else:
            crux_history_data = fetch_crux_history_data(url, api_key)

            if crux_history_data:
                metrics = crux_history_data.get("metrics", {})

                for metric_name, metric_data in metrics.items():
                    if "histogramTimeseries" in metric_data:
                        # Get data for most recent period (assuming last entry)
                        latest_densities = metric_data["histogramTimeseries"][-1]["densities"]
                        score = calculate_score(latest_densities)
                        st.write(f"- {metric_name.capitalize()}:")
                        if score:
                            st.write(f"  - Score: {score:.1f}")
                        else:
                            st.write("  - Data not available for the past 28 days.")
                    else:
                        st.write(f"- {metric_name.capitalize()}: Data not available")
                st.write("")  # Add empty line for readability

            else:
                st.warning("No CrUX History API data found for the provided URL or an error occurred.")


if __name__ == "__main__":
    main()
