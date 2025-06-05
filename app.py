import streamlit as st
import requests
from readability import Document
from bs4 import BeautifulSoup

# Extract main readable content from a URL using readability-lxml
def extract_readable_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)

        # Parse with readability
        doc = Document(response.text)
        html_content = doc.summary()

        # Clean the HTML and extract visible text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove nav, header, footer just in case
        for tag in soup(['nav', 'header', 'footer']):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        word_count = len(text.split())

        return text, word_count

    except Exception as e:
        return f"Error extracting content from {url}: {e}", 0

# Streamlit UI
st.set_page_config(page_title="eCommerce Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor (Readability)")
st.markdown("This tool extracts the **main content** from eCommerce category pages using `readability-lxml` — just like browser reader mode.")

urls_input = st.text_area("Enter one or more category page URLs (one per line):", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]

    for url in urls:
        st.markdown(f"---\n### 🔗 {url}")
        with st.spinner("Extracting readable content..."):
            content, word_count = extract_readable_content(url)
            st.markdown(f"**Word Count:** `{word_count}`")
            st.text_area("Extracted Content", content, height=300)
