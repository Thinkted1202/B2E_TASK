import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	# SECRET KEY 設定
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'b2e_api'
	SSL_REDIRECT = True
	#SQLALCHEMY ORM 設定
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_RECORD_QUERIES = True
	# DB SLOW QUERY
	FLASKY_SLOW_DB_QUERY_TIME = 0.5
	#HTTP DOMAIN
	HOST = 'python.thinkted.com.tw'
	#REDIS
	REDIS_CONFIG={
		'CACHE_TYPE': 'redis',
		'CACHE_REDIS_HOST':os.environ.get('REDIS_HOST'),
		'CACHE_REDIS_PORT':os.environ.get('REDIS_PORT'),
		'CACHE_KEY_PREFIX':'b2e_api'
	}
	#與下面的環境區分出不同的子類別
	@staticmethod
	def init_app(app):
		pass

#開發環境 SIT
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'mysql+pymysql://' + os.environ.get('DB_ACCOUNT') +':' + os.environ.get('DB_PWD') + '@'+ os.environ.get('DB_HOST') +':3306/api'

#測試環境 UAT
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'mysql+pymysql://' + os.environ.get('DB_ACCOUNT') +':' + os.environ.get('DB_PWD') + '@'+ os.environ.get('DB_HOST') +':3306/api'

# 正式環境 Production
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'mysql+pymysql://' + os.environ.get('DB_ACCOUNT') +':' + os.environ.get('DB_PWD') + '@'+ os.environ.get('DB_HOST') +':3306/api'

	#實做一個init_app的類別 區分不同的環境
	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

#設定預設的環境和其他環境的Object
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
