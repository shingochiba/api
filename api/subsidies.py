from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            category = data.get('category', 'all')
            limit = int(data.get('limit', 10))
            industry = data.get('industry', 'all')
            
            # モックデータ
            mock_subsidies = [
                {
                    "name": "IT導入補助金2025",
                    "category": "経済産業省 中小企業庁",
                    "saitakuritsu": "約58%",
                    "Upper limit": "上限額：450万円",
                    "Application deadline": "応募締切：2025年7月31日",
                    "industry": "IT"
                },
                {
                    "name": "ものづくり補助金",
                    "category": "経済産業省 中小企業庁", 
                    "saitakuritsu": "約45%",
                    "Upper limit": "上限額：1,000万円",
                    "Application deadline": "応募締切：2025年8月15日",
                    "industry": "製造業"
                }
            ]
            
            # フィルタリング
            filtered = mock_subsidies
            if category != "all":
                filtered = [s for s in filtered if category in s.get('category', '')]
            if industry != "all":
                filtered = [s for s in filtered if s.get('industry') == industry or s.get('industry') == 'all']
            
            result = {
                "success": True,
                "subsidies": filtered[:limit],
                "total_count": len(filtered[:limit]),
                "message": f"{len(filtered[:limit])}件の補助金データを取得しました"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers()
            error_response = {"success": False, "error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))