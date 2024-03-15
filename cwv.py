import streamlit as st
import requests
import json

# Define CrUX API endpoint (replace with your API key)
crux_api_url = "https://pageadspeedinsights.googleapis.com/v1/mobile?key={YOUR_API_KEY}&url="

def check_core_web_vitals(url):
  """
  Checks Core Web Vitals pass/fail based on CrUX data for the given URL.

  Args:
      url: The URL to check.

  Returns:
      A dictionary containing pass/fail status for each Core Web Vital metric.
  """
  response = requests.get(crux_api_url + url)
  data = json.loads(response.text)

  # Check for successful response
  if "originLists" not in data:
    return {"error": "Failed to retrieve CrUX data"}

  # Extract CrUX data for each metric
  lcp_data = data["originLists"][0]["audits"]["largest-contentful-paint"]["metrics"]
  fid_data = data["originLists"][0]["audits"]["first-input-delay"]["metrics"]
  cls_data = data["originLists"][0]["audits"]["cumulative-layout-shift"]["metrics"]

  # Define thresholds based on Google's recommendations (adjust as needed)
  lcp_threshold = 2.5
  fid_threshold = 100
  cls_threshold = 0.1

  # Analyze data and determine pass/fail
  results = {
      "Largest Contentful Paint (LCP)": "Pass" if lcp_data["percentile"] < lcp_threshold else "Fail",
      "First Input Delay (FID)": "Pass" if fid_data["percentile"] < fid_threshold else "Fail",
      "Cumulative Layout Shift (CLS)": "Pass" if cls_data["percentile"] < cls_threshold else "Fail",
  }

  return results

st.title("Core Web Vitals Bulk Checker")

# Input field for API key
api_key = st.text_input("Enter your CrUX API Key", type="password")

# Text area for URLs
urls_text = st.text_area("Enter a list of URLs (one per line)")

if st.button("Check Core Web Vitals"):
  # Split URLs by line break
  urls = urls_text.split("\n")

  # Check for empty API key or URL list
  if not api_key or not urls:
    st.error("Please enter a CrUX API key and a list of URLs.")
    return

  # Check each URL and display results
  for url in urls:
    st.header(f"URL: {url}")
    results = check_core_web_vitals(url)

    # Handle errors
    if "error" in results:
      st.error(results["error"])
    else:
      # Display results in a table
      table = st.table(results.items())
      st.success("Core Web Vitals assessment complete!")
