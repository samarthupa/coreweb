import streamlit as st
import requests

# Main function to fetch Core Web Vitals assessment
def get_core_web_vitals(url, api_key):
    endpoint = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}'
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        # Extract the Core Web Vitals assessment from the API response
        core_web_vitals = data.get('loadingExperience', {}).get('overall_category', 'Unknown')
        return core_web_vitals
    else:
        return 'API Error'

# Streamlit app
def main():
    st.title("Bulk Core Web Vitals Checker")

    # Input field for API key
    api_key = st.text_input("Enter your Google PageSpeed Insights API key:")

    # Text area for entering URLs
    st.subheader("Enter the URLs to check (one per line):")
    urls_text = st.text_area("URLs")

    # Convert the text area input to a list of URLs
    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

    if st.button("Check Core Web Vitals"):
        if not api_key:
            st.error("Please enter your Google PageSpeed Insights API key.")
        elif not urls:
            st.warning("Please enter at least one URL.")
        else:
            st.subheader("Core Web Vitals Assessment:")
            # Loop through each URL and get its Core Web Vitals assessment
            for url in urls:
                core_web_vitals = get_core_web_vitals(url, api_key)
                st.write(f'{url}: {core_web_vitals}')

if __name__ == "__main__":
    main()
