import sqlite3

def init_db():
    with sqlite3.connect('questions.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                image TEXT
            )
        ''')

def add_question(question, answer, image):
    with sqlite3.connect('questions.db') as conn:
        conn.execute("INSERT INTO questions (question, answer, image) VALUES (?, ?, ?)", (question, answer, image))

def get_all_questions():
    with sqlite3.connect('questions.db') as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM questions").fetchall()

def get_question(question_id):
    with sqlite3.connect('questions.db') as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
