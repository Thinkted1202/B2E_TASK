from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	#取得組態物件
	app.config.from_object(config[config_name])
	#啟用設定檔 開始初始化相關的設定
	config[config_name].init_app(app)
	#將實例化的app 分派給各個套件
	db.init_app(app)

	if app.config['SSL_REDIRECT']:
		from flask_sslify import SSLify
		sslify = SSLify(app)

	#匯入藍圖
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	#匯入藍圖
	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/v1')

	return app