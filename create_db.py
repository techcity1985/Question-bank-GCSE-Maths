import sqlite3

def create_db():
    conn = sqlite3.connect('gcse_maths_question_bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                 id INTEGER PRIMARY KEY,
                 question TEXT,
                 answer TEXT,
                 topic TEXT,
                 difficulty TEXT,
                 question_type TEXT)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
