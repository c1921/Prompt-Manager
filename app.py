from flask import Flask, render_template, request, jsonify
from services.translation_service import TranslationService, TranslationError
from config.config import config
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化翻译服务
    translator = TranslationService(config_name)
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            prompt = request.form.get('prompt', '')
            return render_template('index.html', prompt=prompt)
        return render_template('index.html')

    @app.route('/translate', methods=['POST'])
    def translate():
        try:
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