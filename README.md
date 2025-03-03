# Terabox Downloader (Koyeb)

A Flask app to extract Terabox download links, deployed on Koyeb.

## Setup Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Add `cookies.txt` with valid Terabox cookies.
3. Run: `python app.py`

## Deploy on Koyeb
1. Push to GitHub.
2. Connect repo to Koyeb.
3. Set build command: `pip install -r requirements.txt`.
4. Set run command: `gunicorn app:app`.
5. Add `cookies.txt` via Koyeb dashboard.
