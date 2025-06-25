from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

def handler(request):
    """Vercel用ハンドラー"""
    
    if request.method == 'OPTIONS':
        # CORS対応
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            category = data.get('category', 'all')
            limit = int(data.get('limit', 10))
            industry = data.get('industry', 'all')
            
            # モック補助金データ
            mock_subsidies = [
                {
                    "name": "IT導入補助金2025",
                    "category": "経済産業省 中小企業庁",
                    "saitakuritsu": "約58%",
                    "Upper limit": "上限額：450万円",
                    "Application deadline": "応募締切：2025年7月31日",
                    "description": "中小企業・小規模事業者等のITツール導入を支援",
                    "industry": "IT"
                },
                {
                    "name": "ものづくり補助金",
                    "category": "経済産業省 中小企業庁",
                    "saitakuritsu": "約45%",
                    "Upper limit": "上限額：1,000万円",
                    "Application deadline": "応募締切：2025年8月15日",
                    "description": "中小企業等の生産性向上に向けた革新的サービス開発を支援",
                    "industry": "製造業"
                },
                {
                    "name": "事業再構築補助金",
                    "category": "経済産業省",
                    "saitakuritsu": "約40%",
                    "Upper limit": "上限額：8,000万円",
                    "Application deadline": "応募締切：2025年9月30日",
                    "description": "新分野展開、事業転換、業種転換等を支援",
                    "industry": "all"
                },
                {
                    "name": "小規模事業者持続化補助金",
                    "category": "経済産業省 中小企業庁",
                    "saitakuritsu": "約65%",
                    "Upper limit": "上限額：200万円",
                    "Application deadline": "応募締切：2025年8月31日",
                    "description": "小規模事業者の販路開拓等を支援",
                    "industry": "サービス業"
                },
                {
                    "name": "創業支援補助金",
                    "category": "経済産業省",
                    "saitakuritsu": "約35%",
                    "Upper limit": "上限額：300万円",
                    "Application deadline": "応募締切：2025年10月15日",
                    "description": "新たに創業する者に対する支援",
                    "industry": "all"
                },
                {
                    "name": "キャリアアップ助成金",
                    "category": "厚生労働省",
                    "saitakuritsu": "約72%",
                    "Upper limit": "上限額：500万円",
                    "Application deadline": "応募締切：2025年12月28日",
                    "description": "非正規雇用労働者の企業内でのキャリアアップを支援",
                    "industry": "all"
                }
            ]
            
            # フィルタリング
            filtered_subsidies = mock_subsidies
            
            if category != "all":
                filtered_subsidies = [s for s in filtered_subsidies if category in s.get('category', '')]
            
            if industry != "all":
                filtered_subsidies = [s for s in filtered_subsidies if s.get('industry') == industry or s.get('industry') == 'all']
            
            # 件数制限
            final_subsidies = filtered_subsidies[:limit]
            
            result = {
                "success": True,
                "subsidies": final_subsidies,
                "total_count": len(final_subsidies),
                "message": f"{len(final_subsidies)}件の補助金データを取得しました",
                "last_updated": datetime.now().isoformat(),
                "input_params": {
                    "category": category,
                    "limit": limit,
                    "industry": industry
                }
            }
            
            return jsonify(result), 200, {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            }
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
                "subsidies": [],
                "total_count": 0,
                "message": f"エラーが発生しました: {str(e)}"
            }), 500, {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            }
    
    return jsonify({"message": "Method not allowed"}), 405