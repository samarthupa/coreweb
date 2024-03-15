import streamlit as st
import requests

# Function to fetch Core Web Vitals assessment for mobile
def get_core_web_vitals_mobile(url, api_key):
    endpoint = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}&strategy=mobile'
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        # Extract the Core Web Vitals metrics
        lcp = data.get('loadingExperience', {}).get('metrics', {}).get('LARGEST_CONTENTFUL_PAINT_MS', -1)
        fid = data.get('loadingExperience', {}).get('metrics', {}).get('FIRST_INPUT_DELAY_MS', -1)
        cls = data.get('loadingExperience', {}).get('metrics', {}).get('CUMULATIVE_LAYOUT_SHIFT_SCORE', -1)
        # Check if metrics meet the thresholds for passing Core Web Vitals
        if lcp <= 2500 and fid <= 100 and cls <= 0.1:
            return 'Passed'
        else:
            return 'Failed'
    else:
        return 'API Error'

# Streamlit app
def main():
    st.title("Bulk Core Web Vitals Checker (Mobile)")

    # Input field for API key
    api_key = st.text_input("Enter your Google PageSpeed Insights API key:")

    # Text area for entering URLs
    st.subheader("Enter the URLs to check (one per line):")
    urls_text = st.text_area("URLs")

    # Convert the text area input to a list of URLs
    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

    if st.button("Check Core Web Vitals (Mobile)"):
        if not api_key:
            st.error("Please enter your Google PageSpeed Insights API key.")
        elif not urls:
            st.warning("Please enter at least one URL.")
        else:
            st.subheader("Core Web Vitals Assessment (Mobile):")
            # Loop through each URL and get its Core Web Vitals assessment for mobile
            for url in urls:
                core_web_vitals = get_core_web_vitals_mobile(url, api_key)
                st.write(f'{url}: {core_web_vitals}')

if __name__ == "__main__":
    main()
