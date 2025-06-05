import streamlit as st
import requests
import trafilatura

# Function to extract main content using trafilatura
def extract_trafilatura_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)

        # Run trafilatura on the HTML (with fallback if it fails)
        downloaded = trafilatura.extract(response.text, include_comments=False, include_tables=False, no_fallback=False)

        if downloaded:
            word_count = len(downloaded.split())
            return downloaded, word_count
        else:
            return "No content extracted by trafilatura.", 0

    except Exception as e:
        return f"Error extracting content from {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="eCommerce Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor (trafilatura)")
st.markdown("This tool extracts readable content from eCommerce category pages using **trafilatura**. Fully compatible with **Streamlit Cloud**.")

urls_input = st.text_area("Enter one or more category page URLs (one per line):", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]

    for url in urls:
        st.markdown(f"---\n### 🔗 {url}")
        with st.spinner("Extracting content with trafilatura..."):
            content, word_count = extract_trafilatura_content(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)

