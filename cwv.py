import streamlit as st
import requests
from lxml import html

def get_redirected_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

def get_text_from_xpath(url, xpath):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    text = tree.xpath(xpath)
    if text:
        return text[0].text_content()
    else:
        return None

def main():
    st.title("URL Text Extractor")

    url_input = st.text_input("Enter URL(s) separated by space (or newline):")

    if st.button("Extract Text"):
        urls = url_input.split()
        for url in urls:
            redirected_url = get_redirected_url(url)
            st.write(f"Redirected URL: {redirected_url}")
            text = get_text_from_xpath(redirected_url, '//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/span[1]')
            if text:
                st.write(f"Text extracted from URL: {text}")
            else:
                st.write("Unable to extract text from the provided URL.")

if __name__ == "__main__":
    main()
