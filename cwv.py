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
            "first_input_delay"
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
                metrics = crux_history_data.get("metrics", {})
                cls_data = metrics.get("cumulative_layout_shift", [])
                inp_data = metrics.get("first_input_delay", [])
                lcp_data = metrics.get("largest_contentful_paint", [])
                
                # Filter data for the last 28 days
                cls_last_28_days = cls_data[-28:]
                inp_last_28_days = inp_data[-28:]
                lcp_last_28_days = lcp_data[-28:]
                
                # Calculate average values
                avg_cls = sum(cls_last_28_days) / len(cls_last_28_days)
                avg_inp = sum(inp_last_28_days) / len(inp_last_28_days)
                avg_lcp = sum(lcp_last_28_days) / len(lcp_last_28_days)
                
                # Display average values
                st.write("Core Web Vitals Assessment:")
                if avg_cls <= 0.1 and avg_inp <= 100 and avg_lcp <= 2500:
                    st.write("Passed")
                else:
                    st.write("Failed")

                st.write("Largest Contentful Paint (LCP)")
                st.write(f"{avg_lcp} ms")

                st.write("Interaction to Next Paint (INP)")
                st.write(f"{avg_inp} ms")

                st.write("Cumulative Layout Shift (CLS)")
                st.write(avg_cls)

                # Other notable metrics
                st.write("OTHER NOTABLE METRICS")
                st.write("First Contentful Paint (FCP)")
                st.write("First Input Delay (FID)")
                st.write("Time to First Byte (TTFB)")
            else:
                st.warning("No CrUX History API data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
