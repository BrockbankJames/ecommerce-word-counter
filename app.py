import streamlit as st
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

# Function to render page and return full HTML
def get_rendered_html(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            time.sleep(2)  # Wait for JavaScript-rendered content
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        return None  # Return None to indicate failure

# Function to extract visible text blocks from rendered HTML
def extract_text_blocks(html):
    if html is None:
        return "Page could not be rendered.", 0

    soup = BeautifulSoup(html, 'html.parser')

    paragraphs = soup.find_all('p')
    text_blocks = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]

    combined_text = "\n".join(text_blocks)
    word_count = len(combined_text.split())

    return combined_text, word_count

# Streamlit UI
st.set_page_config(page_title="eCommerce Content Extractor", layout="wide")
st.title("🛍️ eCommerce Category Content Extractor")
st.markdown("This tool uses **Playwright + BeautifulSoup** to extract visible content from eCommerce category pages (above & below the product grid).")

urls_input = st.text_area("Enter URLs (one per line)", height=200)
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
    
    for url in urls:
        st.markdown(f"---\n### 🔗 URL: {url}")
        with st.spinner("Rendering and extracting content..."):
            html = get_rendered_html(url)
            if html:
                try:
                    text, word_count = extract_text_blocks(html)
                    st.markdown(f"**Word Count:** `{word_count}`")
                    st.text_area("Extracted Content", text, height=300)
                except Exception as parse_err:
                    st.error(f"Parsing error: {parse_err}")
            else:
                st.error("❌ Page could not be rendered or loaded.")
