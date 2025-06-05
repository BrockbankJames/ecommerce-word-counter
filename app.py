import streamlit as st
import requests
import trafilatura

# Function to extract main content and word count
def extract_main_content(url):
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        downloaded = trafilatura.extract(response.text)
        if downloaded:
            word_count = len(downloaded.split())
            return downloaded, word_count
        else:
            return "No main content could be extracted.", 0
    except Exception as e:
        return f"Error fetching {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="Category Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor")
st.markdown("Extract the main content and word count from one or more eCommerce category URLs using **trafilatura**.")

# Input box
urls_input = st.text_area("Enter URLs (one per line)", height=200)
extract_button = st.button("Extract Content")

# Process URLs on button click
if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
    
    for url in urls:
        st.markdown(f"---\n### 🔗 URL: {url}")
        with st.spinner(f"Extracting content from {url}..."):
            content, word_count = extract_main_content(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)
