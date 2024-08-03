from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    image_path = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))

# Quiz model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    questions = db.relationship('Question', secondary='quiz_question', backref=db.backref('quizzes', lazy='dynamic'))

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_question'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)

# Form classes
class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    image_file = FileField('Image File Path')
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

@app.before_first_request
def create_tables():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/category/<int:category_id>')
@login_required
def category(category_id):
    category = Category.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, questions=questions)

@app.route('/add_category', methods=['GET', 'POST'])
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_category.html', form=form)

@app.route('/add', methods=['GET', 'POST'])
@admin_required
def add_question():
    form = QuestionForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        image_file = form.image_file.data
        if image_file:
            image_path = 'static/uploads/' + image_file.filename
            image_file.save(image_path)
        else:
            image_path = None

        question = Question(
            question=form.question.data,
            answer=form.answer.data,
            image_path=image_path,
            category_id=form.category.data
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_question.html', form=form)

@app.route('/create_quiz', methods=['GET', 'POST'])
@admin_required
def create_quiz():
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        question_ids = request.form.getlist('question_ids')
        
        quiz = Quiz(name=quiz_name)
        db.session.add(quiz)
        db.session.commit()
        
        for question_id in question_ids:
            quiz_question = QuizQuestion(quiz_id=quiz.id, question_id=question_id)
            db.session.add(quiz_question)
        
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('index'))

    questions = Question.query.all()
    return render_template('create_quiz.html', questions=questions)

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        correct_answers = 0
        for question in quiz.questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer == question.answer:
                correct_answers += 1
        score = (correct_answers / len(quiz.questions)) * 100
        return render_template('result.html', score=score)

    return render_template('quiz.html', quiz=quiz)

if __name__ == '__main__':
    app.run(debug=True)
