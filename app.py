import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to extract visible category text from static HTML
def extract_category_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        candidates = []

        # Common visible tags
        tags_to_extract = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol']
        for tag in tags_to_extract:
            elements = soup.find_all(tag)
            for el in elements:
                text = el.get_text(separator=" ", strip=True)
                if text and len(text) > 30:  # Filter out very short bits
                    candidates.append(text)

        # Also target known class names used in eCommerce templates
        class_names = [
            'category-description',
            'collection-description',
            'page-description',
            'text-content',
            'main-copy',
            'seo-text',
            'content',
            'rte',
            'product-grid__description'
        ]
        for class_name in class_names:
            blocks = soup.find_all(class_=class_name)
            for block in blocks:
                text = block.get_text(separator=" ", strip=True)
                if text and text not in candidates:
                    candidates.append(text)

        combined_text = "\n\n".join(candidates)
        word_count = len(combined_text.split())

        return combined_text, word_count

    except Exception as e:
        return f"Error fetching {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="eCommerce Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor (Static HTML)")
st.markdown("Extracts visible content (including above/below product grid text) from eCommerce category pages using static HTML parsing. Compatible with **Streamlit Cloud**.")

urls_input = st.text_area("Enter one or more category page URLs (one per line):", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]

    for url in urls:
        st.markdown(f"---\n### 🔗 URL: {url}")
        with st.spinner("Fetching and extracting content..."):
            content, word_count = extract_category_text(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)

