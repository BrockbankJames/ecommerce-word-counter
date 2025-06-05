# Webpage Word Counter

A Streamlit application that allows you to scrape and count words from multiple web pages, focusing only on the main content (excluding headers, footers, and navigation).

## Streamlit Cloud Deployment

This app is configured for deployment on Streamlit Cloud. To deploy:

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository
6. Set the main file path to `app.py`
7. Click "Deploy"

The app will be automatically deployed with all necessary dependencies.

## Local Development

If you want to run the app locally:

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features

- Extracts main content only (ignores headers, footers, and navigation)
- Uses jusText to remove boilerplate content
- Processes multiple URLs in parallel
- Provides word count statistics
- Handles errors gracefully
- Exports results to CSV

## Notes

- The app uses jusText for content extraction, which is designed to extract main content while ignoring navigation, headers, and footers
- A maximum of 5 concurrent requests are processed to avoid overwhelming servers
- Some websites may block automated requests
- Processing time depends on the number of URLs and website response times

## License

MIT License
