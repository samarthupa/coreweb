import streamlit as st
import requests
from bs4 import BeautifulSoup
from lxml import html

def get_redirected_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        redirected_url = response.url
        return redirected_url
    except Exception as e:
        st.error(f"Error occurred while fetching the URL: {e}")
        return None

def get_span_text(url):
    try:
        response = requests.get(url)
        tree = html.fromstring(response.content)
        span_text = tree.xpath('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/span[1]/text()')
        if span_text:
            return span_text[0]
        else:
            return "Span element not found"
    except Exception as e:
        st.error(f"Error occurred while parsing the page: {e}")
        return None

def main():
    st.title("URL Analyzer")

    url_input = st.text_input("Enter URL(s) separated by commas:", "")

    if st.button("Analyze"):
        urls = [url.strip() for url in url_input.split(',')]
        for url in urls:
            concatenated_url = f"https://pagespeed.web.dev/analysis?url={url}"
            redirected_url = get_redirected_url(concatenated_url)
            if redirected_url:
                st.write(f"Redirected URL: {redirected_url}")
                span_text = get_span_text(redirected_url)
                if span_text:
                    st.write(f"Text of the span element: {span_text}")
                else:
                    st.warning("Failed to extract text from the span element.")
            else:
                st.warning("Failed to fetch redirected URL.")

if __name__ == "__main__":
    main()
