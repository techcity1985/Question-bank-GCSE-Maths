from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import init_db, add_question, get_all_questions, get_question
from forms import QuestionForm
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
init_db()

@app.route('/')
def home():
    form = QuestionForm()
    rows = get_all_questions()
    return render_template('index.html', form=form, rows=rows)

@app.route('/add_question', methods=['POST'])
def add_question_route():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        image = form.image.data

        image_path = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

        add_question(question, answer, image_path)
        flash('Question added successfully', 'success')
        return redirect(url_for('home'))
    rows = get_all_questions()
    return render_template('index.html', form=form, rows=rows)

@app.route('/list_questions')
def list_questions():
    rows = get_all_questions()
    return render_template('list.html', rows=rows)

@app.route('/view_question/<int:question_id>')
def view_question_route(question_id):
    row = get_question(question_id)
    return render_template('view_question.html', row=row)

if __name__ == '__main__':
    app.run(debug=True)
