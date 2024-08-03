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

def add_question(question, answer, topic, difficulty, question_type):
    conn = sqlite3.connect('gcse_maths_question_bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO questions (question, answer, topic, difficulty, question_type) VALUES (?, ?, ?, ?, ?)", 
              (question, answer, topic, difficulty, question_type))
    conn.commit()
    conn.close()

def get_questions_by_topic(topic):
    conn = sqlite3.connect('gcse_maths_question_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE topic=?", (topic,))
    questions = c.fetchall()
    conn.close()
    return questions

def get_questions_by_difficulty(difficulty):
    conn = sqlite3.connect('gcse_maths_question_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE difficulty=?", (difficulty,))
    questions = c.fetchall()
    conn.close()
    return questions

def get_all_questions():
    conn = sqlite3.connect('gcse_maths_question_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    questions = c.fetchall()
    conn.close()
    return questions

def main():
    create_db()
    while True:
        print("1. Add a question")
        print("2. Retrieve questions by topic")
        print("3. Retrieve questions by difficulty")
        print("4. Retrieve all questions")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            question = input("Enter the question: ")
            answer = input("Enter the answer: ")
            topic = input("Enter the topic: ")
            difficulty = input("Enter the difficulty (Easy/Medium/Hard): ")
            question_type = input("Enter the question type (Multiple Choice/Short Answer/Long Answer): ")
            add_question(question, answer, topic, difficulty, question_type)
            print("Question added successfully!")
        elif choice == '2':
            topic = input("Enter the topic: ")
            questions = get_questions_by_topic(topic)
            for q in questions:
                print(q)
        elif choice == '3':
            difficulty = input("Enter the difficulty (Easy/Medium/Hard): ")
            questions = get_questions_by_difficulty(difficulty)
            for q in questions:
                print(q)
        elif choice == '4':
            questions = get_all_questions()
            for q in questions:
                print(q)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
