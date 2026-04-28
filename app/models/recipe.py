from .db import get_db_connection
import sqlite3

class Recipe:
    @staticmethod
    def create(title, ingredients='', instructions='', image_path='', source_url=''):
        """
        新增一筆食譜記錄
        :param title: 食譜名稱 (必填)
        :param ingredients: 食材清單
        :param instructions: 製作步驟
        :param image_path: 圖片路徑
        :param source_url: 來源網址
        :return: 新增的食譜 ID，若發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, ingredients, instructions, image_path, source_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, ingredients, instructions, image_path, source_url))
            recipe_id = cursor.lastrowid
            conn.commit()
            return recipe_id
        except sqlite3.Error as e:
            print(f"Error creating recipe: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有食譜記錄
        :return: 包含食譜字典的列表，若發生錯誤則回傳空列表
        """
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in recipes]
        except sqlite3.Error as e:
            print(f"Error getting all recipes: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆食譜記錄
        :param recipe_id: 食譜 ID
        :return: 食譜字典 (包含 tags)，若找不到或發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            
            if recipe:
                recipe_dict = dict(recipe)
                # 取得關聯的標籤
                tags = conn.execute('''
                    SELECT t.id, t.name FROM tags t
                    JOIN recipe_tags rt ON t.id = rt.tag_id
                    WHERE rt.recipe_id = ?
                ''', (recipe_id,)).fetchall()
                recipe_dict['tags'] = [dict(t) for t in tags]
                return recipe_dict
            return None
        except sqlite3.Error as e:
            print(f"Error getting recipe by id {recipe_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(recipe_id, title, ingredients='', instructions='', image_path='', source_url=''):
        """
        更新一筆食譜記錄
        :param recipe_id: 食譜 ID
        :param title: 食譜名稱 (必填)
        :param ingredients: 食材清單
        :param instructions: 製作步驟
        :param image_path: 圖片路徑
        :param source_url: 來源網址
        :return: 是否更新成功 (True/False)
        """
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE recipes
                SET title = ?, ingredients = ?, instructions = ?, image_path = ?, source_url = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, ingredients, instructions, image_path, source_url, recipe_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating recipe {recipe_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除一筆食譜記錄
        :param recipe_id: 食譜 ID
        :return: 是否刪除成功 (True/False)
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting recipe {recipe_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def add_tags(recipe_id, tag_ids):
        """
        為食譜加入標籤關聯
        :param recipe_id: 食譜 ID
        :param tag_ids: 標籤 ID 列表
        :return: 是否加入成功 (True/False)
        """
        try:
            conn = get_db_connection()
            for tag_id in tag_ids:
                try:
                    conn.execute('INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
                except sqlite3.IntegrityError:
                    pass # 忽略重複
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding tags to recipe {recipe_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def clear_tags(recipe_id):
        """
        清除食譜的所有標籤關聯
        :param recipe_id: 食譜 ID
        :return: 是否清除成功 (True/False)
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipe_tags WHERE recipe_id = ?', (recipe_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing tags for recipe {recipe_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
