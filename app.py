from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 프론트와 연결 시 CORS 이슈 처리

@app.route('/check', methods=['POST'])
def check_link():
    data = request.json
    short_url = data.get('url')

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(short_url, allow_redirects=True, headers=headers, timeout=5)
        final_url = resp.url
        params = parse_qs(urlparse(final_url).query)
        lptag = params.get('lptag', [None])[0]

        return jsonify({
            'final_url': final_url,
            'is_partners': bool(lptag),
            'partners_id': lptag or '없음'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
