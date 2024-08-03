from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from forms import QuestionForm, RegistrationForm, LoginForm, CategoryForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

from models import User, Question, Category, Quiz

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        image_file = None
        if form.image_file.data:
            image_file = form.image_file.data.filename
            form.image_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file))
        new_question = Question(question=form.question.data, answer=form.answer.data, image_path=image_file, category_id=form.category.data)
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully.', 'success')
        return redirect(url_for('index'))
    questions = Question.query.all()
    return render_template('add_question.html', form=form, questions=questions)

@app.route('/category/<int:category_id>')
@login_required
def category(category_id):
    category = Category.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('category.html', category=category, questions=questions)

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_category.html', form=form)

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if session.get('role') != 'admin':
        flash('You do not have permission to create quizzes.', 'danger')
        return redirect(url_for('index'))
    form = QuizForm()
    if form.validate_on_submit():
        questions = [Question.query.get(q_id) for q_id in form.questions.data]
        new_quiz = Quiz(name=form.name.data, questions=questions)
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz created successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('create_quiz.html', form=form)

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer and user_answer.strip().lower() == question.answer.strip().lower():
                score += 1
        score_percentage = (score / len(quiz.questions)) * 100
        return render_template('result.html', score=score_percentage)
    return render_template('quiz.html', quiz=quiz)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
