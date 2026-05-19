import sqlite3
import os

BOT_DB = os.environ.get('BOT_DB')

def init_db():
    conn = sqlite3.connect(BOT_DB)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        user_name TEXT,
        user_state TEXT DEFAULT "none"           
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)
    
    
    conn.commit()
    conn.close()

def connect_to_db():
    conn = sqlite3.connect(BOT_DB)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    return conn,cursor

def insert_user(user_id, user_name):
    conn ,cursor = connect_to_db()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)",(user_id, user_name))
    conn.commit()
    conn.close()

def get_user_state(user_id):
    conn,cursor = connect_to_db()
    cursor.execute("SELECT user_state FROM users WHERE user_id=?",(user_id,))
    state = cursor.fetchone()
    conn.close()

    if state:
        return state[0]
    return "none"

def update_user_state(user_id, user_state):
    conn, cursor = connect_to_db()
    cursor.execute(
        "UPDATE users SET user_state = ? WHERE user_id = ?",
        (user_state, user_id)
    )
    conn.commit()
    conn.close()

def add_task(user_id, task):
    conn , cursor = connect_to_db()
    cursor.execute("INSERT INTO tasks(user_id,task) VALUES (?,?)",(user_id, task))
    conn.commit()
    conn.close()

def get_list(user_id):
    conn, cursor  = connect_to_db()
    cursor.execute("SELECT task, id , status FROM tasks WHERE user_id = ?",(user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def get_stats(user_id):
    conn,cursor = connect_to_db()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? ",(user_id,))
    count_all = cursor.fetchone()[0]
    conn.close()
    return count_all

def update_task_status(task_id,user_id):
    conn,cursor = connect_to_db()
    cursor.execute("UPDATE tasks SET status = NOT status where id = ? AND user_id = ? ", (task_id,user_id))
    conn.commit()
    conn.close()
    
def del_task(task_id):
    conn,cursor = connect_to_db()
    cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    conn.commit()
    conn.close()