from flask import Flask, render_template, request, redirect, url_for
from models import init_db, add_question, get_all_questions, get_question
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_question', methods=['POST'])
def add_question_route():
    question = request.form['question']
    answer = request.form['answer']
    image = request.files['image']

    image_path = None
    if image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

    add_question(question, answer, image_path)
    msg = "Question added successfully"
    return render_template('index.html', msg=msg)

@app.route('/list_questions')
def list_questions():
    rows = get_all_questions()
    return render_template('list.html', rows=rows)

@app.route('/view_question/<int:question_id>')
def view_question_route(question_id):
    row = get_question(question_id)
    return render_template('result.html', row=row)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
