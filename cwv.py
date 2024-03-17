import streamlit as st
import requests

# Function to fetch CrUX History API data
def fetch_crux_history_data(url, api_key):
    endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={api_key}"
    payload = {
        "url": url
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()["record"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX History API data: {e}")
        return None

# Calculate metric value based on density
def calculate_metric_value(densities):
    total = 0
    for i, density in enumerate(densities):
        total += (i + 1) * density
    return total

# Main function for Streamlit app
def main():
    st.title("CrUX History API Data Fetcher")

    # Input URL and API key
    url = st.text_input("Enter a URL:")
    api_key = st.text_input("Enter your CrUX API key:")

    # Fetch CrUX History API data on button click
    if st.button("Fetch CrUX History API Data"):
        if not api_key:
            st.error("Please enter your CrUX API key.")
        elif not url:
            st.error("Please enter a URL.")
        else:
            crux_history_data = fetch_crux_history_data(url, api_key)

            if crux_history_data:
                metrics = crux_history_data.get("metrics", {})
                core_web_vitals = {
                    "largest_contentful_paint": "Largest Contentful Paint (LCP)",
                    "first_input_delay": "Interaction to Next Paint (INP)",
                    "cumulative_layout_shift": "Cumulative Layout Shift (CLS)"
                }

                st.header("Core Web Vitals Assessment:")
                all_passed = True
                for metric_name, metric_label in core_web_vitals.items():
                    metric_data = metrics.get(metric_name, {})
                    if "histogram" in metric_data:
                        densities = metric_data["histogram"][-1]["density"]
                        metric_value = calculate_metric_value(densities)
                        st.write(f"{metric_label}: {metric_value:.1f} ms")
                        if metric_name == "cumulative_layout_shift" and metric_value > 0.1:
                            all_passed = False
                        elif metric_value > 2500:  # LCP threshold is 2.5 seconds
                            all_passed = False
                    else:
                        st.write(f"No data available for {metric_label}")

                if all_passed:
                    st.write("Core Web Vitals Assessment: Passed")
                else:
                    st.write("Core Web Vitals Assessment: Failed")

                st.header("Other Notable Metrics:")
                other_metrics = {
                    "first_contentful_paint": "First Contentful Paint (FCP)",
                    "first_input_delay": "First Input Delay (FID)",
                    "experimental_time_to_first_byte": "Time to First Byte (TTFB)"
                }

                for metric_name, metric_label in other_metrics.items():
                    metric_data = metrics.get(metric_name, {})
                    if "histogram" in metric_data:
                        densities = metric_data["histogram"][-1]["density"]
                        metric_value = calculate_metric_value(densities)
                        st.write(f"{metric_label}: {metric_value:.1f} ms")
                    else:
                        st.write(f"No data available for {metric_label}")

if __name__ == "__main__":
    main()
