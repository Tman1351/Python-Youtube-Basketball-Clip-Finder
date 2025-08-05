# Basketball Highlights Aggregator (GUI)

A simple desktop app built with **Tkinter** to search and display basketball highlight videos from **YouTube**.

## Features

- Search basketball highlights by keyword
- Fetch up to 5 YouTube videos related to basketball highlights
- Display video title, upload date, and URL
- Double-click a result to open the video in your web browser
- Sort results by upload date (newest first)
- Uses environment variables for YouTube API key security

## Prerequisites

- Python 3.7+
- A valid **YouTube Data API v3** key (create one via Google Cloud Console)

## Setup

1. Clone or download this repository.

2. (Recommended) Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .venv\Scripts\activate       # Windows
Install required packages:

bash
Copy
Edit
pip install -r requirements_gui.txt
Delete .env.template after looking at it
Create a .env file in the project root directory with your YouTube API key:

ini
Copy
Edit
YOUTUBE_API_KEY=your_youtube_api_key_here
Running the App
Run the main script:

bash
Copy
Edit
python highlight-app.py
Enter search terms in the input box.

Press Enter or click the Search button.

Results show video title, upload date, and URL.

Double-click a video to open it in your browser.

Notes
Make sure your YouTube Data API key is active and has YouTube Data API v3 enabled.

The app sorts results by newest uploads.

If the API key is missing or invalid, the app will log errors.

## Credits

- YouTube Data API provided by Google
- Tkinter GUI framework included with Python
- dotenv for environment variable management
- google-api-python-client library for YouTube API access
- Inspired by community examples and open-source projects
