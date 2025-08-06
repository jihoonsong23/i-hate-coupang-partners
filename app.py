from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS

# Flask 앱 생성
app = Flask(__name__)
CORS(app)  # CORS 허용 (프론트엔드에서 API 호출 가능하도록)

@app.route('/')
def home():
    return "쿠팡 파트너스 링크 확인 API입니다."

@app.route('/check', methods=['POST'])
def check_link():
    """쿠팡 단축링크 → 원본 링크 추출 → 파트너스 여부 판별"""
    data = request.json
    short_url = data.get('url')

    if not short_url:
        return jsonify({'error': 'URL이 제공되지 않았습니다.'}), 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(short_url, allow_redirects=True, headers=headers, timeout=5)
        final_url = resp.url

        # URL에서 쿼리 파라미터 분석
        params = parse_qs(urlparse(final_url).query)
        lptag = params.get('lptag', [None])[0]

        return jsonify({
            'final_url': final_url,
            'is_partners': bool(lptag),
            'partners_id': lptag or '없음'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 로컬 실행 시
    app.run(host='0.0.0.0', port=5000, debug=True)
