import sqlite3
import os

BOT_DB = os.environ.get('BOT_DB')

def init_db():
    conn = sqlite3.connect(BOT_DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        user_name TEXT            
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status BOLEAN DEFAULT FALSE,
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

def add_task(user_id, task):
    conn , cursor = connect_to_db()
    cursor.execute("INSERT INTO tasks(user_id,task) VALUES (?,?)",(user_id, task))
    conn.commit()
    conn.close()

def get_list(user_id):
    conn, cursor  = connect_to_db()
    cursor.execute("SELECT task, created_at FROM tasks WHERE user_id = ?",(user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def get_stats(user_id):
    conn,cursor = connect_to_db()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? ",(user_id,))
    count_all = cursor.fetchone()[0]
    conn.close()
    return count_all

def del_task(task_id):
    conn,cursor = connect_to_db()
    cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))