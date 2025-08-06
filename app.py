from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "쿠팡 파트너스 링크 확인 API입니다."

@app.route('/check', methods=['POST'])
def check_link():
    data = request.json
    short_url = data.get('url')

    if not short_url:
        return jsonify({'error': 'URL이 제공되지 않았습니다.'}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0 Safari/537.36'
    }

    try:
        # 1️⃣ 먼저 HEAD 요청 시도 (빠르게 리디렉션 확인)
        try:
            resp = requests.head(short_url, allow_redirects=True, headers=headers, timeout=8)
            final_url = resp.url
        except Exception:
            # 2️⃣ HEAD 실패 시 GET 요청 재시도
            resp = requests.get(short_url, allow_redirects=True, headers=headers, timeout=15)
            final_url = resp.url

        # 3️⃣ 원본 URL에서 lptag 파라미터 추출
        params = parse_qs(urlparse(final_url).query)
        lptag = params.get('lptag', [None])[0]

        return jsonify({
            'final_url': final_url,
            'is_partners': bool(lptag),
            'partners_id': lptag or '없음'
        })

    except requests.exceptions.Timeout:
        return jsonify({'error': '쿠팡 서버 응답이 너무 느립니다. 다시 시도해주세요.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
