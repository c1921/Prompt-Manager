from flask import Flask, render_template, request, jsonify
from services.translation_service import TranslationService, TranslationError
from config.config import config
import webview
import os
import requests
import time
import threading
from werkzeug.serving import make_server
from src.version import VERSION_STR  # 添加这行导入

class FlaskThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 0, app)  # 使用随机端口
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def get_port(self):
        return self.server.server_port

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

    @app.route('/')
    def index():
        return render_template('index.html', 
                             prompt=app.config['DEFAULT_PROMPT'],
                             version=VERSION_STR)

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

def main():
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    
    # 根据环境变量决定是否使用 webview
    use_webview = os.getenv('USE_WEBVIEW', 'false').lower() == 'true'
    
    if use_webview:
        # 在后台线程中运行 Flask
        flask_thread = FlaskThread(app)
        flask_thread.daemon = True
        flask_thread.start()
        
        # 获取随机分配的端口
        port = flask_thread.get_port()
        
        # 创建窗口
        webview.create_window(
            'SD Prompt Manager',
            f'http://127.0.0.1:{port}',
            width=1000,
            height=800,
            resizable=True,
            min_size=(800, 600),
            background_color='#1a1a1a',  # 深色背景
            text_select=True,            # 允许文本选择
            frameless=False,             # 使用系统默认边框
            easy_drag=True               # 允许拖动
        )
        
        # 启动 webview
        webview.start()
    else:
        # 开发模式：直接运行 Flask
        app.run(debug=app.config['DEBUG'])

if __name__ == '__main__':
    main() 