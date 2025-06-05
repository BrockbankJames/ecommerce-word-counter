# Webpage Word Counter

A Streamlit application that allows you to scrape and count words from multiple web pages, focusing only on the main content (excluding headers, footers, and navigation).

## Features

- Extract main content from web pages using Trafilatura
- Process multiple URLs in parallel
- Count words in the extracted content
- Export results to CSV
- Clean and modern UI
- Error handling and validation
- Progress tracking

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

To run the app locally:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Deployment

### Deploying to Streamlit Cloud

1. Create a GitHub repository and push your code
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (`app.py`)
6. Click "Deploy"

### Deploying to Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port $PORT
   ```
2. Create a `runtime.txt`:
   ```
   python-3.9.18
   ```
3. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Usage

1. Enter one or more URLs in the text area (one per line)
2. Click "Process URLs"
3. View the results in the table
4. Download the results as CSV if needed

## Notes

- The app uses Trafilatura for content extraction, which is designed to extract main content while ignoring navigation, headers, and footers
- A maximum of 5 concurrent requests are processed to avoid overwhelming servers
- Some websites may block automated requests
- Processing time depends on the number of URLs and website response times

## License

MIT License 
