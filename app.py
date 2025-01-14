from flask import Flask, render_template, request, jsonify
from services.translation_service import TranslationService, TranslationError
from config.config import config
import os
import requests
import time

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化翻译服务
    translator = TranslationService(config_name)
    
    # 存储上次检测时间和状态
    network_status = {
        'last_check': 0,
        'is_available': False
    }
    
    def check_google_availability():
        """检查谷歌翻译服务是否可用"""
        current_time = time.time()
        # 如果距离上次检测时间不够长，直接返回缓存的状态
        if current_time - network_status['last_check'] < app.config['NETWORK_CHECK_INTERVAL']:
            return network_status['is_available']
            
        try:
            response = requests.get(app.config['GOOGLE_TEST_URL'], timeout=5)
            network_status['is_available'] = response.status_code == 200
        except:
            network_status['is_available'] = False
            
        network_status['last_check'] = current_time
        return network_status['is_available']

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            prompt = request.form.get('prompt', '')
            return render_template('index.html', prompt=prompt)
        return render_template('index.html')

    @app.route('/check-network', methods=['GET'])
    def check_network():
        """检查网络状态的接口"""
        is_available = check_google_availability()
        return jsonify({
            'status': 'available' if is_available else 'unavailable'
        })

    @app.route('/translate', methods=['POST'])
    def translate():
        try:
            # 先检查网络状态
            if not check_google_availability():
                return jsonify({'error': '无法访问谷歌翻译服务，请检查网络连接或使用代理'}), 503
                
            text = request.json.get('text', '')
            to_english = request.json.get('to_english', False)
            
            if not text:
                return jsonify({'error': '文本不能为空'}), 400
                
            translation = translator.translate_text(text, to_english)
            return jsonify({'translation': translation})
        except TranslationError as e:
            return jsonify({'error': str(e)}), 429
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(debug=app.config['DEBUG']) 