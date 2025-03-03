from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import requests
import os

app = Flask(__name__)

def extract_domain_and_surl(url):
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid URL provided")
    return parsed.netloc, parsed.path[3:] if len(parsed.path) > 3 else ""

def parseCookieFile(cookiefile):
    cookies = {}
    if not os.path.exists(cookiefile):
        return None
    with open(cookiefile, 'r') as fp:
        for line in fp:
            if not line.startswith('#'):
                line_fields = line.strip().split('\t')
                if len(line_fields) >= 7:
                    cookie_name = line_fields[5]
                    cookie_value = line_fields[6]
                    cookies[cookie_name] = cookie_value
    return cookies

def get_download_link(url: str) -> dict:
    axios = requests.Session()
    cookies = parseCookieFile('cookies.txt')
    if cookies:
        axios.cookies.update(cookies)
    else:
        return {"success": False, "link": None, "error": "Cookies file not found"}

    try:
        response = axios.get(url)
        response.raise_for_status()
        domain, key = extract_domain_and_surl(response.url)

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': f'https://{domain}/sharing/link?surl={key}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = axios.get(
            f'https://www.terabox.com/share/list?app_id=250528&shorturl={key}&root=1', headers=headers)
        response.raise_for_status()

        data = response.json()
        if 'list' in data and data['list']:
            return {"success": True, "link": data['list'][0]['dlink'], "error": None}
        else:
            return {"success": False, "link": None, "error": "No download link found"}
    except requests.RequestException as e:
        return {"success": False, "link": None, "error": f"HTTP Error: {str(e)}"}
    except ValueError as e:
        return {"success": False, "link": None, "error": f"Error: {str(e)}"}
    except requests.JSONDecodeError:
        return {"success": False, "link": None, "error": "Failed to parse JSON response"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({"success": False, "link": None, "error": "No URL provided"}), 400
    
    result = get_download_link(url)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
