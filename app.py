from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        # 这里后续可以添加处理提示词的逻辑
        return render_template('index.html', prompt=prompt)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 