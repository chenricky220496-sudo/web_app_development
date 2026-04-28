from .db import get_db_connection
import sqlite3

class Tag:
    @staticmethod
    def create(name):
        """
        新增一筆標籤記錄
        :param name: 標籤名稱 (必填)
        :return: 新增的標籤 ID，若發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
                tag_id = cursor.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                # 標籤名稱已存在，直接取得 ID
                tag_id = conn.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()['id']
            return tag_id
        except sqlite3.Error as e:
            print(f"Error creating tag: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有標籤記錄
        :return: 包含標籤字典的列表，若發生錯誤則回傳空列表
        """
        try:
            conn = get_db_connection()
            tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
            return [dict(row) for row in tags]
        except sqlite3.Error as e:
            print(f"Error getting all tags: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(tag_id):
        """
        取得單筆標籤記錄
        :param tag_id: 標籤 ID
        :return: 標籤字典，若找不到或發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            tag = conn.execute('SELECT * FROM tags WHERE id = ?', (tag_id,)).fetchone()
            return dict(tag) if tag else None
        except sqlite3.Error as e:
            print(f"Error getting tag by id {tag_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(tag_id):
        """
        刪除一筆標籤記錄
        :param tag_id: 標籤 ID
        :return: 是否刪除成功 (True/False)
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting tag {tag_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
