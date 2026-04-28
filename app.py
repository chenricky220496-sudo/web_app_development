from app import create_app
from app.models.db import init_db
import os

app = create_app()

if __name__ == '__main__':
    # 確保 instance 目錄存在
    os.makedirs('instance', exist_ok=True)
    
    # 如果資料庫尚未初始化，則進行初始化
    if not os.path.exists(os.path.join('instance', 'database.db')):
        print("Initializing database...")
        init_db()
        print("Database initialized.")
        
    app.run(debug=True)
