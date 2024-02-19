from flask import Flask, render_template, request
from gptQuestioner import main   # Import your existing script


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    if request.method == 'POST':
        question = request.form['question']
        
        answer = main(question)
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
