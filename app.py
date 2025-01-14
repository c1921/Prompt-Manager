from flask import Flask, render_template, request, jsonify
from translation_service import TranslationService

app = Flask(__name__)
translator = TranslationService()

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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 