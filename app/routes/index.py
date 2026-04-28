from flask import Blueprint, render_template, request, redirect, url_for, flash
import random
import os
from werkzeug.utils import secure_filename
from app.models.recipe import Recipe
from app.models.tag import Tag

# 定義 Blueprint
routes = Blueprint('routes', __name__)

# 設定圖片上傳路徑
UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/')
@routes.route('/recipes')
def index():
    """首頁 / 食譜列表"""
    q = request.args.get('q', '').lower().strip()
    tag_name = request.args.get('tag', '').strip()
    
    # 取得所有標籤供篩選區塊使用
    all_tags = Tag.get_all()
    
    # 目前先取得全部食譜，再用 Python 過濾
    recipes = Recipe.get_all()
    
    # 為了顯示標籤，我們幫每個 recipe 取得 tags
    for r in recipes:
        detail = Recipe.get_by_id(r['id'])
        r['tags'] = detail['tags'] if detail else []
    
    if q:
        recipes = [r for r in recipes if q in (r['title'] or '').lower() or q in (r['ingredients'] or '').lower()]
        
    if tag_name:
        recipes = [r for r in recipes if any(t['name'] == tag_name for t in r['tags'])]
        
    return render_template('index.html', recipes=recipes, tags=all_tags, current_q=q, current_tag=tag_name)

@routes.route('/random')
def random_recipe():
    """隨機推薦"""
    recipes = Recipe.get_all()
    if not recipes:
        flash('目前還沒有任何食譜可以推薦，趕快新增一個吧！', 'warning')
        return redirect(url_for('routes.index'))
        
    selected_id = random.choice(recipes)['id']
    return redirect(url_for('routes.recipe_detail', id=selected_id))

@routes.route('/recipes/new')
def new_recipe():
    """新增食譜頁面"""
    tags = Tag.get_all()
    return render_template('edit.html', tags=tags, recipe=None, recipe_tag_ids=[])

@routes.route('/recipes/create', methods=['POST'])
def create_recipe():
    """建立食譜"""
    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    source_url = request.form.get('source_url', '').strip()
    
    # 處理標籤 (可以選多個)
    selected_tags = request.form.getlist('tags')
    
    # 處理新增標籤 (動態建立)
    new_tags_input = request.form.get('new_tags', '').strip()
    if new_tags_input:
        for tag_name in new_tags_input.split(','):
            tag_name = tag_name.strip()
            if tag_name:
                tag_id = Tag.create(tag_name)
                if tag_id:
                    selected_tags.append(str(tag_id))
    
    if not title:
        flash('食譜名稱為必填欄位！', 'danger')
        return redirect(url_for('routes.new_recipe'))
        
    image_path = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # 加入時間戳記避免檔名重複
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            image_path = unique_filename
            
    recipe_id = Recipe.create(title, ingredients, instructions, image_path, source_url)
    
    if recipe_id:
        if selected_tags:
            Recipe.add_tags(recipe_id, [int(t) for t in selected_tags if t.isdigit()])
        flash('食譜新增成功！', 'success')
        return redirect(url_for('routes.recipe_detail', id=recipe_id))
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        return redirect(url_for('routes.new_recipe'))

@routes.route('/recipes/<int:id>')
def recipe_detail(id):
    """食譜詳情"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('routes.index'))
    return render_template('recipe.html', recipe=recipe)

@routes.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    """編輯食譜頁面"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('routes.index'))
        
    tags = Tag.get_all()
    # 建立目前食譜擁有的 tag id 列表，方便前端渲染勾選狀態
    recipe_tag_ids = [t['id'] for t in recipe.get('tags', [])]
    return render_template('edit.html', recipe=recipe, tags=tags, recipe_tag_ids=recipe_tag_ids)

@routes.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """更新食譜"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('routes.index'))

    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    source_url = request.form.get('source_url', '').strip()
    
    if not title:
        flash('食譜名稱為必填欄位！', 'danger')
        return redirect(url_for('routes.edit_recipe', id=id))

    image_path = recipe.get('image_path', '')
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            image_path = unique_filename

    success = Recipe.update(id, title, ingredients, instructions, image_path, source_url)
    
    if success:
        # 處理標籤更新
        selected_tags = request.form.getlist('tags')
        new_tags_input = request.form.get('new_tags', '').strip()
        if new_tags_input:
            for tag_name in new_tags_input.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag_id = Tag.create(tag_name)
                    if tag_id:
                        selected_tags.append(str(tag_id))
                        
        Recipe.clear_tags(id)
        if selected_tags:
            Recipe.add_tags(id, [int(t) for t in selected_tags if t.isdigit()])
            
        flash('食譜更新成功！', 'success')
    else:
        flash('更新失敗，請稍後再試。', 'danger')

    return redirect(url_for('routes.recipe_detail', id=id))

@routes.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """刪除食譜"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('routes.index'))
        
    success = Recipe.delete(id)
    if success:
        # 刪除對應的圖片檔案
        if recipe.get('image_path'):
            img_path = os.path.join(UPLOAD_FOLDER, recipe['image_path'])
            if os.path.exists(img_path):
                os.remove(img_path)
        flash('食譜已刪除！', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('routes.index'))
