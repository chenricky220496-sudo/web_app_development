# 路由設計 (Routes Design) - 食譜收藏夾

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 食譜列表 | GET | `/` 或 `/recipes` | `templates/index.html` | 顯示所有食譜，支援關鍵字與標籤過濾 |
| 隨機推薦 | GET | `/random` | — | 隨機挑選食譜並重導向至詳情頁 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/edit.html` | 顯示新增表單（與編輯共用模板） |
| 建立食譜 | POST | `/recipes/create` | — | 接收表單，存入 DB，重導向至首頁或詳情頁 |
| 食譜詳情 | GET | `/recipes/<int:id>` | `templates/recipe.html` | 顯示單筆食譜完整資訊 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `templates/edit.html` | 顯示編輯表單，預載入既有資料 |
| 更新食譜 | POST | `/recipes/<int:id>/update` | — | 接收表單，更新 DB，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete` | — | 刪除資料庫紀錄，重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 / 食譜列表
- **URL**: `GET /` 或 `GET /recipes`
- **輸入**: URL 參數 `?q=關鍵字` 或 `?tag=標籤名稱` (選擇性)。
- **處理邏輯**: 呼叫 `Recipe.get_all()`。如果有搜尋關鍵字或標籤，則進行過濾。
- **輸出**: 渲染 `index.html`。
- **錯誤處理**: 若無任何食譜，顯示「尚無食譜」提示。

### 隨機推薦
- **URL**: `GET /random`
- **輸入**: 無。
- **處理邏輯**: 取得所有食譜 ID，使用 `random.choice()` 挑選一個 ID。
- **輸出**: 呼叫 `redirect(url_for('routes.recipe_detail', id=selected_id))` 重導向至該食譜詳情頁。
- **錯誤處理**: 若資料庫全空，導回首頁並顯示提示。

### 新增食譜頁面
- **URL**: `GET /recipes/new`
- **輸入**: 無。
- **處理邏輯**: 取得所有可用標籤 `Tag.get_all()` 供表單選擇。
- **輸出**: 渲染 `edit.html`。

### 建立食譜
- **URL**: `POST /recipes/create`
- **輸入**: 表單資料 `title`, `ingredients`, `instructions`, `image`, `source_url`, `tags[]`。
- **處理邏輯**: 
  - 驗證 `title` 是否存在。
  - 將圖片儲存至 `static/images/`，並取得路徑。
  - 呼叫 `Recipe.create()` 寫入。
  - 呼叫 `Recipe.add_tags()` 處理標籤關聯。
- **輸出**: `redirect(url_for('routes.index'))`。
- **錯誤處理**: 若必填欄位遺失，導回新增頁面並顯示錯誤訊息。

### 食譜詳情
- **URL**: `GET /recipes/<int:id>`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)`。
- **輸出**: 渲染 `recipe.html`。
- **錯誤處理**: 若找不到對應的 `id`，回傳 404 頁面或導回首頁。

### 編輯食譜頁面
- **URL**: `GET /recipes/<int:id>/edit`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 取得現有資料，並呼叫 `Tag.get_all()`。
- **輸出**: 渲染 `edit.html` (預填資料)。
- **錯誤處理**: 若找不到對應的 `id`，回傳 404 頁面。

### 更新食譜
- **URL**: `POST /recipes/<int:id>/update`
- **輸入**: 表單資料與 URL 變數 `id`。
- **處理邏輯**: 
  - 更新資料庫紀錄 `Recipe.update()`。
  - 若有新圖片則覆蓋。
  - 呼叫 `Recipe.clear_tags()` 後重新 `Recipe.add_tags()`。
- **輸出**: `redirect(url_for('routes.recipe_detail', id=id))`。

### 刪除食譜
- **URL**: `POST /recipes/<int:id>/delete`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.delete(id)`，若有圖片一併刪除實體檔案。
- **輸出**: `redirect(url_for('routes.index'))`。

## 3. Jinja2 模板清單

- `templates/base.html`
  - **說明**: 共用的網頁骨架結構（包含 `<head>`、導覽列、頁尾等）。
- `templates/index.html`
  - **繼承**: `base.html`
  - **說明**: 首頁，顯示食譜卡片列表、搜尋列、隨機推薦按鈕。
- `templates/recipe.html`
  - **繼承**: `base.html`
  - **說明**: 顯示單一食譜的詳細圖文、食材與步驟。包含編輯與刪除按鈕。
- `templates/edit.html`
  - **繼承**: `base.html`
  - **說明**: 共用表單頁面。當新增時為空白表單，當編輯時填入既有資料。

## 4. 路由骨架程式碼

位於 `app/routes/index.py` 中，我們使用 Flask Blueprint 來組織相關路由，讓後續將 Controller 整合進 `app.py` 更加乾淨。
