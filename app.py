from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('questions.db')
    print("Opened database successfully")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            image BLOB
        )
    ''')
    print("Table created successfully")
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_question', methods=['POST'])
def add_question():
    question = request.form['question']
    answer = request.form['answer']
    image = request.files['image'].read() if 'image' in request.files else None

    with sqlite3.connect('questions.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO questions (question, answer, image) VALUES (?, ?, ?)", (question, answer, image))
        con.commit()
        msg = "Question added successfully"
    return render_template('index.html', msg=msg)

@app.route('/list_questions')
def list_questions():
    con = sqlite3.connect('questions.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM questions")

    rows = cur.fetchall()
    return render_template('list.html', rows=rows)

@app.route('/view_question/<int:question_id>')
def view_question(question_id):
    con = sqlite3.connect('questions.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    row = cur.fetchone()

    return render_template('result.html', row=row)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
