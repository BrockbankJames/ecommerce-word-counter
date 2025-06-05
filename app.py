import streamlit as st
import requests
import justext

def extract_main_content(url):
    try:
        response = requests.get(url, timeout=10)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        text = "\n".join([p.text for p in paragraphs if not p.is_boilerplate])
        return text
    except Exception as e:
        return f"Error fetching {url}: {e}"

st.title("eCommerce Category Content Extractor")
st.write("Enter one or more eCommerce category URLs to extract the main page content using jusText.")

urls_input = st.text_area("Enter URLs (one per line)")
extract_button = st.button("Extract Content")

if extract_button and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
    for url in urls:
        st.markdown(f"### Content from {url}")
        with st.spinner(f"Extracting content from {url}..."):
            result = extract_main_content(url)
            st.text_area("Extracted Content", result, height=300)
