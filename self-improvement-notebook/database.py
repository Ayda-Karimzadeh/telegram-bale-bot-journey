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
    CREATE TABLE IF NOT EXISTS progresses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        progress TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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

def add_progress(user_id, progress):
    conn , cursor = connect_to_db()
    cursor.execute("INSERT INTO progresses(user_id,progress) VALUES (?,?)",(user_id, progress))
    conn.commit()
    conn.close()

def get_list(user_id):
    conn, cursor  = connect_to_db()
    cursor.execute("SELECT progress, created_at FROM progresses WHERE user_id = ?",(user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def get_stats(user_id):
    conn,cursor = connect_to_db()
    cursor.execute("SELECT COUNT(*) FROM progresses WHERE user_id = ? ",(user_id,))
    count_all = cursor.fetchone()[0]
    conn.close()
    return count_all