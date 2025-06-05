import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to extract clean content from category pages
def extract_clean_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 1: Remove unwanted elements
        for tag in soup(['nav', 'header', 'footer', 'script', 'style', 'noscript']):
            tag.decompose()

        # Remove common product containers by class/id (expand as needed)
        product_classes = ['product-tile', 'product-grid', 'product-list', 'grid-item']
        product_ids = ['product-grid', 'product-list']

        for cls in product_classes:
            for tag in soup.find_all(class_=cls):
                tag.decompose()
        for pid in product_ids:
            tag = soup.find(id=pid)
            if tag:
                tag.decompose()

        # Step 2: Extract visible content
        tags_to_extract = ['h1', 'h2', 'h3', 'h4', 'p', 'div']
        candidates = []

        for tag in tags_to_extract:
            for el in soup.find_all(tag):
                # Skip hidden or empty elements
                if el.get("aria-hidden") == "true":
                    continue
                text = el.get_text(separator=" ", strip=True)
                if text and len(text.split()) >= 5:
                    candidates.append(text)

        # Step 3: Combine and clean
        combined_text = "\n\n".join(candidates)
        word_count = len(combined_text.split())

        return combined_text, word_count

    except Exception as e:
        return f"Error extracting content from {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="Clean Category Content Extractor", layout="wide")
st.title("🛍️ Clean eCommerce Category Content Extractor")
st.markdown("This tool extracts **clean, non-product content** from eCommerce category pages. It removes navigation, footer, product grids, and other noise.")

urls_input = st.text_area("Enter one or more category page URLs (one per line):", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]

    for url in urls:
        st.markdown(f"---\n### 🔗 {url}")
        with st.spinner("Extracting clean content..."):
            content, word_count = extract_clean_content(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)

