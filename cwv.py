import streamlit as st
import requests

# CrUX API endpoint (replace with your API key)
CRUX_API_URL = "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=AIzaSyANOzNJ4C4f2Ng5Ark4YzyWelNe-WBblug"

def fetch_crux_data(url, form_factor="DESKTOP"):
    """Fetches CrUX data for a given URL and form factor.

    Args:
        url (str): The URL to fetch data for.
        form_factor (str, optional): The device type ("DESKTOP" or "MOBILE"). Defaults to "DESKTOP".

    Returns:
        dict: A dictionary containing the CrUX data or None if an error occurs.
    """

    payload = {
        "url": url,
        "formFactor": form_factor,
    }

    try:
        response = requests.post(CRUX_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data = response.json()
        if "record" in data:
            return data["record"]
        else:
            st.warning("No CrUX data found for the provided URL.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CrUX data: {e}")
        return None

def main():
    """Main function for the Streamlit app."""

    st.title("CrUX Data Fetcher")

    url = st.text_input("Enter a URL:")
    form_factor = st.selectbox("Form Factor", ["DESKTOP", "MOBILE"])

    if st.button("Fetch CrUX Data"):
        crux_data = fetch_crux_data(url, form_factor)

        if crux_data:
            st.write("**CrUX Data:**")
            lcp = crux_data.get("metrics", {}).get("largest_contentful_paint", {}).get("percentile", None)
            cls = crux_data.get("metrics", {}).get("cumulative_layout_shift", {}).get("percentile", None)
            inp = crux_data.get("metrics", {}).get("first_input_delay", {}).get("percentile", None)

            # Handle potential None values before formatting
            lcp_str = f"- Largest Contentful Paint (LCP): {lcp:.2f} seconds (if available)" if lcp else "- Largest Contentful Paint (LCP): Not available"
            cls_str = f"- Cumulative Layout Shift (CLS): {cls:.2f} (if available)" if cls else "- Cumulative Layout Shift (CLS): Not available"
            inp_str = f"- First Input Delay (INP): {inp:.2f} milliseconds (if available)" if inp else "- First Input Delay (INP): Not available"

            st.write(lcp_str)
            st.write(cls_str)
            st.write(inp_str)
        else:
            st.warning("No CrUX data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
