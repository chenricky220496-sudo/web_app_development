from .db import get_db_connection
import sqlite3

class Tag:
    @staticmethod
    def create(name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
            tag_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            # 標籤名稱已存在，直接取得 ID
            tag_id = conn.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()['id']
        finally:
            conn.close()
        return tag_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
        conn.close()
        return [dict(row) for row in tags]

    @staticmethod
    def get_by_id(tag_id):
        conn = get_db_connection()
        tag = conn.execute('SELECT * FROM tags WHERE id = ?', (tag_id,)).fetchone()
        conn.close()
        return dict(tag) if tag else None

    @staticmethod
    def delete(tag_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
        conn.commit()
        conn.close()
