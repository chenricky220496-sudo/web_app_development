# 系統架構設計 (System Architecture) - 食譜收藏夾

## 1. 技術架構說明

### 選用技術與原因
- **後端框架：Python + Flask**
  - **原因**：Flask 是一個輕量級的 Web 框架，學習曲線平緩，非常適合用來快速開發中小型專案。對於「食譜收藏夾」這樣的個人工具，Flask 能提供足夠的彈性且不會有過多的冗餘功能。
- **模板引擎：Jinja2**
  - **原因**：內建於 Flask 中，能夠將後端傳遞的資料無縫地整合進 HTML 頁面。不採用前後端分離，有助於降低專案複雜度與開發時間。
- **資料庫：SQLite (透過 SQLAlchemy 或 sqlite3)**
  - **原因**：SQLite 是無伺服器的輕量級關聯式資料庫，資料儲存於單一檔案中，非常容易備份與遷移。對於個人使用的本機端系統，效能與儲存空間都綽綽有餘。
- **前端：HTML + CSS (Vanilla)**
  - **原因**：搭配 Jinja2 渲染畫面，為了維持輕量快速，使用純 HTML 與 CSS 即可滿足需求，且易於客製化響應式與現代感的介面。

### Flask MVC 模式說明
雖然 Flask 本身不強制規定使用 MVC（Model-View-Controller）模式，但本專案將採用類似的結構來確保程式碼可讀性與維護性：
- **Model (資料模型)**：負責定義資料結構與資料庫互動邏輯（如 `Recipe`, `Tag` 等）。如果是透過 SQLAlchemy，會在這裡定義各個 table 對應的 Python Class。
- **View (視圖/模板)**：負責呈現給使用者的介面。在這裡就是 `templates/` 目錄下的 HTML + Jinja2 檔案。
- **Controller (控制器/路由)**：負責接收使用者的請求 (Request)，向 Model 獲取或更新資料，然後決定要渲染哪個 View 返回給使用者 (Response)。對應到 Flask 中的 `routes/` 或是 `@app.route` 裝飾的函式。

## 2. 專案資料夾結構

```text
web_app_development/
├── app/
│   ├── __init__.py      # Flask app 初始化設定
│   ├── models/          # Model：定義 SQLite 資料庫表格與存取邏輯
│   │   └── recipe.py    # 食譜與標籤的資料模型
│   ├── routes/          # Controller：處理 HTTP 請求的路由定義
│   │   └── index.py     # 各頁面路由與 API 邏輯 (新增/刪除/查詢/推薦)
│   ├── templates/       # View：Jinja2 HTML 模板檔案
│   │   ├── base.html    # 共用的網頁骨架結構
│   │   ├── index.html   # 首頁 (食譜列表與隨機推薦)
│   │   ├── recipe.html  # 食譜詳細內容頁
│   │   └── edit.html    # 新增與編輯食譜頁面
│   └── static/          # 靜態資源檔案
│       ├── css/
│       │   └── style.css # 全域樣式設定
│       ├── js/
│       │   └── main.js  # 前端互動邏輯
│       └── images/      # 食譜圖片上傳的儲存目錄或預設圖片
├── instance/            # 存放機密或環境專屬檔案 (通常不會進版控)
│   └── database.db      # SQLite 資料庫檔案
├── docs/                # 文件資料夾
│   ├── PRD.md           # 產品需求文件
│   └── ARCHITECTURE.md  # 系統架構文件 (本文件)
├── app.py               # 專案入口點，負責啟動 Flask 伺服器
└── requirements.txt     # Python 相依套件列表
```

## 3. 元件關係圖

以下是系統運作的資料流與元件互動流程圖：

```mermaid
flowchart LR
    Browser[瀏覽器\n(使用者介面)] -->|HTTP Request\n(GET / POST)| Router(Flask Router\nController)
    Router -->|1. 查詢/更新資料| Model(Models\nSQLAlchemy/sqlite3)
    Model -->|2. 讀/寫| DB[(SQLite 資料庫)]
    DB -->|3. 回傳資料| Model
    Model -->|4. 將資料轉為 Python 物件| Router
    Router -->|5. 傳遞資料並渲染| View(Jinja2 Templates\nView)
    View -->|6. 產出 HTML| Router
    Router -->|HTTP Response\n(HTML 網頁)| Browser
```

## 4. 關鍵設計決策

1. **伺服器端渲染 (SSR)**
   - **決策**：採用 Flask + Jinja2 渲染 HTML 回傳給瀏覽器，而非建立 API 讓 React/Vue 等前端框架透過 AJAX 抓資料。
   - **原因**：專案定位為個人使用的輕量工具，採用 SSR 能最快速地完成開發，避免設定複雜的前後端建置環境，並能確保頁面載入速度極快。
2. **單一資料庫檔案 (SQLite)**
   - **決策**：將所有資料（包含食譜、標籤、關聯表）儲存在 `instance/database.db` 中。
   - **原因**：符合輕量化與容易備份的需求。不需要額外安裝或設定 MySQL/PostgreSQL 伺服器，對本機環境來說非常方便。
3. **圖片直接儲存於本機檔案系統**
   - **決策**：使用者上傳的圖片儲存在 `app/static/images/`，資料庫僅記錄相對檔案路徑。
   - **原因**：將大型二進位檔案寫入 SQLite 可能會拖慢資料庫效能。存在本地資料夾可直接透過 web server (Flask) 作為靜態資源提供，效能更好且簡單。
4. **目錄結構模組化 (Blueprints 概念)**
   - **決策**：雖然目前專案小，但仍規劃了 `app/models/` 與 `app/routes/` 結構。
   - **原因**：避免所有邏輯全塞在 `app.py` 中，導致程式碼難以維護。適度的分層（MVC概念）有助於程式碼的職責分離與未來的擴充可能。
