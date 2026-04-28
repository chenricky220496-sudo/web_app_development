from .db import get_db_connection
import sqlite3

class Recipe:
    @staticmethod
    def create(title, ingredients='', instructions='', image_path='', source_url=''):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (title, ingredients, instructions, image_path, source_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, ingredients, instructions, image_path, source_url))
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return recipe_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def get_by_id(recipe_id):
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
        else:
            recipe_dict = None
            
        conn.close()
        return recipe_dict

    @staticmethod
    def update(recipe_id, title, ingredients='', instructions='', image_path='', source_url=''):
        conn = get_db_connection()
        conn.execute('''
            UPDATE recipes
            SET title = ?, ingredients = ?, instructions = ?, image_path = ?, source_url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, ingredients, instructions, image_path, source_url, recipe_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def add_tags(recipe_id, tag_ids):
        conn = get_db_connection()
        for tag_id in tag_ids:
            try:
                conn.execute('INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
            except sqlite3.IntegrityError:
                pass # 忽略重複
        conn.commit()
        conn.close()

    @staticmethod
    def clear_tags(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM recipe_tags WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()
