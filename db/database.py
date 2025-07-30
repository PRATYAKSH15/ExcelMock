import sqlite3

def init_db():
    conn = sqlite3.connect("interview_results.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            question TEXT,
            answer TEXT,
            score INTEGER,
            feedback TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_response(question_obj, answer, score, feedback):
    conn = sqlite3.connect("interview_results.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO results (question, answer, score, feedback)
        VALUES (?, ?, ?, ?)
    """, (question_obj["question"], answer, score, feedback))
    conn.commit()
    conn.close()
