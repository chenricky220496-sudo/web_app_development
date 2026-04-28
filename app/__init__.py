from flask import Flask
from app.routes.index import routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key' # 在正式環境請使用環境變數
    
    # 註冊 Blueprint
    app.register_blueprint(routes)
    
    return app
