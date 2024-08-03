from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)')
    print("Table created successfully")
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-question/', methods=['POST'])
def add_question():
    if request.method == 'POST':
        try:
            question = request.form['question']
            answer = request.form['answer']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (question, answer))
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
