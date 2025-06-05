import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to extract visible content from static HTML
def extract_category_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove header, footer, nav elements
        for tag in soup(['nav', 'header', 'footer']):
            tag.decompose()

        # Extract visible content from these tags
        tags_to_extract = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'div']
        candidates = []

        for tag in tags_to_extract:
            for el in soup.find_all(tag):
                text = el.get_text(separator=" ", strip=True)
                if text and len(text.split()) >= 5:
                    candidates.append(text)

        combined_text = "\n\n".join(candidates)
        word_count = len(combined_text.split())

        return combined_text, word_count

    except Exception as e:
        return f"Error fetching {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="eCommerce Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor")
st.markdown("This tool extracts visible, meaningful content from eCommerce category pages using static HTML. It **ignores navigation, headers, and footers**, and is compatible with **Streamlit Cloud**.")

urls_input = st.text_area("Enter one or more category page URLs (one per line):", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]

    for url in urls:
        st.markdown(f"---\n### 🔗 {url}")
        with st.spinner("Fetching and extracting content..."):
            content, word_count = extract_category_text(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)

