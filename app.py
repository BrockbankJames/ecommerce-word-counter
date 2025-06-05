import streamlit as st
import requests
import trafilatura

def extract_main_content(url):
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        downloaded = trafilatura.extract(response.text)
        if downloaded:
            return downloaded
        else:
            return "No main content could be extracted."
    except Exception as e:
        return f"Error fetching {url}: {e}"

st.title("eCommerce Category Content Extractor (with trafilatura)")
st.write("Enter one or more eCommerce category URLs below. This tool will extract the main content using trafilatura.")

urls_input = st.text_area("Enter URLs (one per line)")
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
    for url in urls:
        st.markdown(f"### Content from {url}")
        with st.spinner(f"Extracting content from {url}..."):
            result = extract_main_content(url)
            st.text_area("Extracted Content", result, height=300)
