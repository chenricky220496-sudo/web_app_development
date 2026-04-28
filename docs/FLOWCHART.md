# 流程圖設計 (Flowchart) - 食譜收藏夾

本文件基於 PRD 的需求與 ARCHITECTURE 的設計，視覺化「使用者操作路徑」以及「系統內部資料流」，並列出各功能對應的路由規劃。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者進入網站後，如何瀏覽、新增、編輯或隨機挑選食譜：

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁 - 食譜列表]
    
    B --> C{要執行什麼操作？}
    
    C -->|1. 新增食譜| D[進入「新增食譜」表單頁]
    D --> D1[填寫圖文、食材、步驟、分類標籤]
    D1 -->|點擊儲存| D2[儲存成功]
    D2 --> B
    
    C -->|2. 找食譜| E[輸入關鍵字 或 點選分類標籤]
    E --> E1[顯示篩選後的食譜清單]
    E1 -->|點擊卡片| F[進入「食譜詳情頁」]
    
    C -->|3. 不知道吃什麼| G[點擊首頁「隨機推薦」按鈕]
    G --> F
    
    F --> H{在詳情頁的操作}
    H -->|編輯| I[進入「編輯食譜」表單頁]
    I --> I1[修改內容並送出]
    I1 --> F
    
    H -->|刪除| J[點擊刪除並確認]
    J --> B
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖以 **「使用者新增食譜」** 為例，描述從前端表單送出到後端資料庫寫入的完整資料流：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask 路由 (Controller)
    participant Model as 模型層 (Model)
    participant DB as SQLite 資料庫
    
    User->>Browser: 填寫食譜內容並點擊「儲存」
    Browser->>Route: 提交表單資料 (POST /recipes/create)
    Route->>Model: 驗證必填欄位並建立 Recipe 物件
    Model->>DB: 執行 SQL (INSERT INTO recipes)
    DB-->>Model: 回傳成功狀態與新建的 ID
    Model-->>Route: 建立成功
    Route-->>Browser: 重導向 (Redirect) 至首頁或該食譜詳情頁
    Browser-->>User: 顯示最新增的食譜
```

## 3. 功能清單對照表

根據使用者的操作路徑，以下是系統會實作的頁面路由（URL）與對應的 HTTP 請求方法：

| 功能項目 | 說明 | URL 路徑 | HTTP 方法 |
| :--- | :--- | :--- | :--- |
| **首頁 / 列表** | 顯示所有食譜，包含搜尋關鍵字與標籤過濾邏輯 | `/` | GET |
| **新增表單頁** | 顯示提供使用者填寫新食譜的網頁介面 | `/recipes/new` | GET |
| **處理新增** | 接收表單送出的資料並存入資料庫 | `/recipes/create` | POST |
| **食譜詳情頁** | 顯示單一食譜的完整食材、步驟與圖片 | `/recipes/<id>` | GET |
| **編輯表單頁** | 顯示載入既有資料的表單網頁介面 | `/recipes/<id>/edit` | GET |
| **處理編輯** | 接收表單修改後的資料並更新資料庫 | `/recipes/<id>/update` | POST |
| **處理刪除** | 刪除指定的食譜並導回首頁 | `/recipes/<id>/delete` | POST |
| **隨機推薦** | 隨機挑選資料庫中一筆食譜，並重導向至其詳情頁 | `/random` | GET |

> 註：由於原生 HTML 表單僅支援 GET 與 POST 方法，因此修改（Update）與刪除（Delete）操作在此皆配置為 POST 路由。
