from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('questions.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question TEXT NOT NULL,
                            answer TEXT NOT NULL
                          )''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('questions.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT question, answer FROM questions')
        questions = cursor.fetchall()
    return render_template('index.html', questions=questions)

@app.route('/add', methods=['POST'])
def add_question():
    question = request.form['question']
    answer = request.form['answer']
    with sqlite3.connect('questions.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO questions (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
