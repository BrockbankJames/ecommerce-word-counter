import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to extract visible category text
def extract_category_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for <p> and content blocks that typically hold category copy
        candidates = []

        # All <p> tags
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                candidates.append(text)

        # Known category content block classes
        for classname in ['category-description', 'intro-text', 'page-description', 'collection-description']:
            for block in soup.find_all(class_=classname):
                text = block.get_text(strip=True)
                if text and text not in candidates:
                    candidates.append(text)

        combined_text = "\n".join(candidates)
        word_count = len(combined_text.split())

        return combined_text, word_count

    except Exception as e:
        return f"Error fetching {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="eCommerce Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor (Static HTML)")
st.markdown("Extracts visible HTML content from eCommerce category pages using BeautifulSoup. For use on **Streamlit Cloud** (no JavaScript rendering).")

urls_input = st.text_area("Enter one or more URLs (one per line)", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]

    for url in urls:
        st.markdown(f"---\n### 🔗 {url}")
        with st.spinner("Fetching and parsing content..."):
            content, word_count = extract_category_text(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)
