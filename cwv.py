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
        return response.json()["record"]
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
            lcp = crux_data.get("largestContentfulPaint", {}).get("median", None)
            cls = crux_data.get("cumulativeLayoutShift", {}).get("median", None)
            inp = crux_data.get("firstInputDelay", {}).get("median", None)

            st.write(f"- Largest Contentful Paint (LCP): {lcp:.2f} seconds (if available)")
            st.write(f"- Cumulative Layout Shift (CLS): {cls:.2f} (if available)")
            st.write(f"- First Input Delay (INP): {inp:.2f} milliseconds (if available)")

            # Avoid unnecessary modifications (as per feedback)
            # st.success("Data fetched successfully!")
        else:
            st.warning("No CrUX data found for the provided URL or an error occurred.")

if __name__ == "__main__":
    main()
