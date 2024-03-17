import streamlit as st
import requests


# Function to fetch CrUX History API data
def fetch_crux_history_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={api_key}"
    payload = {
        "origin": url,  # Assuming the input URL is the origin
        "metrics": [
            "largest_contentful_paint",
            "first_contentful_paint",
            "first_input_delay",
        ]
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()["record"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX History API data: {e}")
        return None


# Function to convert milliseconds to seconds with milliseconds
def ms_to_seconds_ms(milliseconds):
    seconds = int(milliseconds / 1000)
    remaining_ms = int(milliseconds % 1000)
    return f"{seconds} s {remaining_ms} ms"


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
                st.write("**Core Web Vitals:**")
                metrics = crux_history_data.get("metrics", {})

                for metric_name, metric_data in metrics.items():
                    if "percentiles" in metric_data:
                        percentiles = metric_data["percentiles"]
                        p75 = percentiles.get("p75", 0)
                        processed_value = ms_to_seconds_ms(p75)
                        st.write(f"- {metric_name.capitalize()}: {processed_value}")
                    else:
                        st.write(f"- {metric_name.capitalize()}: Data not available")
                st.write("")  # Add empty line for readability

            else:
                st.warning("No CrUX History API data found for the provided URL or an error occurred.")


if __name__ == "__main__":
    main()
