import streamlit as st
import trafilatura
import pandas as pd
from urllib.parse import urlparse
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Set page config
st.set_page_config(
    page_title="Webpage Word Counter",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-text {
        color: #28a745;
    }
    .error-text {
        color: #dc3545;
    }
    </style>
    """, unsafe_allow_html=True)

def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def scrape_url(url):
    """Scrape content from a URL using trafilatura."""
    try:
        # Add timeout and headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        downloaded = trafilatura.fetch_url(url, headers=headers, timeout=10)
        
        if downloaded:
            # Extract main content
            content = trafilatura.extract(downloaded, include_comments=False, 
                                        include_tables=True, 
                                        no_fallback=False)
            
            if content:
                # Clean and count words
                words = content.split()
                word_count = len(words)
                return {
                    'url': url,
                    'word_count': word_count,
                    'status': 'Success',
                    'error': None
                }
            else:
                return {
                    'url': url,
                    'word_count': 0,
                    'status': 'Error',
                    'error': 'No content could be extracted'
                }
        else:
            return {
                'url': url,
                'word_count': 0,
                'status': 'Error',
                'error': 'Could not download the page'
            }
    except Exception as e:
        return {
            'url': url,
            'word_count': 0,
            'status': 'Error',
            'error': str(e)
        }

def process_urls(urls):
    """Process multiple URLs in parallel."""
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(scrape_url, url): url for url in urls}
        for future in future_to_url:
            results.append(future.result())
    return results

# App header
st.markdown('<h1 class="main-header">Webpage Word Counter</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enter URLs to scrape and count words from their main content</p>', unsafe_allow_html=True)

# URL input
urls_input = st.text_area(
    "Enter URLs (one per line):",
    height=150,
    help="Enter multiple URLs, each on a new line"
)

# Process button
if st.button("Process URLs", type="primary"):
    if urls_input:
        # Split URLs and clean them
        urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
        
        # Validate URLs
        valid_urls = [url for url in urls if is_valid_url(url)]
        invalid_urls = [url for url in urls if not is_valid_url(url)]
        
        if invalid_urls:
            st.warning(f"Invalid URLs found: {', '.join(invalid_urls)}")
        
        if valid_urls:
            with st.spinner('Processing URLs...'):
                # Process URLs
                results = process_urls(valid_urls)
                
                # Create DataFrame
                df = pd.DataFrame(results)
                
                # Display results
                st.markdown("### Results")
                
                # Summary statistics
                total_words = df['word_count'].sum()
                avg_words = df['word_count'].mean()
                success_count = len(df[df['status'] == 'Success'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Words", f"{total_words:,}")
                with col2:
                    st.metric("Average Words per Page", f"{avg_words:,.0f}")
                with col3:
                    st.metric("Successfully Processed", f"{success_count}/{len(valid_urls)}")
                
                # Display detailed results
                st.dataframe(
                    df.style.format({'word_count': '{:,}'}),
                    use_container_width=True
                )
                
                # Download button for results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="webpage_word_counts.csv",
                    mime="text/csv"
                )
    else:
        st.error("Please enter at least one URL")

# Instructions
with st.expander("How to use this tool"):
    st.markdown("""
    ### Instructions
    1. Enter one or more URLs in the text area above (one URL per line)
    2. Click the "Process URLs" button
    3. View the results in the table below
    4. Download the results as a CSV file if needed
    
    ### Features
    - Extracts main content only (ignores headers, footers, and navigation)
    - Processes multiple URLs in parallel
    - Provides word count statistics
    - Handles errors gracefully
    - Exports results to CSV
    
    ### Notes
    - Some websites may block automated requests
    - Processing time depends on the number of URLs and website response times
    - Maximum of 5 concurrent requests to avoid overwhelming servers
    """) 
