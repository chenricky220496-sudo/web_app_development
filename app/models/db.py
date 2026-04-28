import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'database.db')

def get_db_connection():
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 開啟 Foreign Key 支援
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    conn = get_db_connection()
    schema_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
