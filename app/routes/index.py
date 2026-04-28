from flask import Blueprint, render_template, request, redirect, url_for, flash
import random

# 定義 Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/recipes')
def index():
    """
    首頁 / 食譜列表
    - 輸入：URL 參數 ?q=關鍵字 或 ?tag=標籤名稱 (選擇性)
    - 處理邏輯：查詢資料庫獲取食譜列表，若有搜尋條件則過濾
    - 輸出：渲染 templates/index.html
    """
    pass

@routes.route('/random')
def random_recipe():
    """
    隨機推薦
    - 處理邏輯：隨機取得一個食譜 ID
    - 輸出：重導向至該食譜的詳情頁
    """
    pass

@routes.route('/recipes/new')
def new_recipe():
    """
    新增食譜頁面
    - 處理邏輯：取得所有可用標籤
    - 輸出：渲染 templates/edit.html (空白表單)
    """
    pass

@routes.route('/recipes/create', methods=['POST'])
def create_recipe():
    """
    建立食譜
    - 輸入：表單資料 (title, ingredients, instructions, image, source_url, tags)
    - 處理邏輯：驗證資料、儲存圖片、寫入資料庫並關聯標籤
    - 輸出：重導向至首頁
    """
    pass

@routes.route('/recipes/<int:id>')
def recipe_detail(id):
    """
    食譜詳情
    - 輸入：食譜 ID
    - 處理邏輯：根據 ID 查詢食譜詳細資訊與關聯標籤
    - 輸出：渲染 templates/recipe.html，若找不到則回傳 404
    """
    pass

@routes.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    """
    編輯食譜頁面
    - 輸入：食譜 ID
    - 處理邏輯：查詢該食譜既有資料與所有可用標籤
    - 輸出：渲染 templates/edit.html (帶入既有資料)
    """
    pass

@routes.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    更新食譜
    - 輸入：食譜 ID 與表單資料
    - 處理邏輯：更新資料庫紀錄、處理新圖片、更新標籤關聯
    - 輸出：重導向至食譜詳情頁
    """
    pass

@routes.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    - 輸入：食譜 ID
    - 處理邏輯：從資料庫刪除紀錄，並刪除對應的圖片實體檔案
    - 輸出：重導向至首頁
    """
    pass
