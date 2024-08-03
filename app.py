from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT,
        image TEXT
    )''')
    print("Table created successfully")
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    conn.close()
    return render_template('index.html', questions=questions)

@app.route('/add-question/', methods=['POST'])
def add_question():
    if request.method == 'POST':
        try:
            question = request.form['question']
            answer = request.form['answer']
            image = request.form['image']  # Path to the image file

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO questions (question, answer, image) VALUES (?, ?, ?)", (question, answer, image))
                conn.commit()
                msg = "Record successfully added"
        except Exception as e:
            conn.rollback()
            msg = "Error in insert operation: " + str(e)
        finally:
            return render_template('result.html', msg=msg)
            conn.close()

if __name__ == "__main__":
    init_sqlite_db()
    app.run(debug=True)
