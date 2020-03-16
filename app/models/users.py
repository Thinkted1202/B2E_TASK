from .. import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app,request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	created_at = db.Column(db.DateTime(), default=datetime.utcnow)

	#設定當有人呼叫password就直接噴錯　不能直接呼叫
	@property #將這個function設定為屬性
	def password(self):
		raise AttributeError('密碼不能直接呼叫')
	#當PASSWORD被assign 值 觸發
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	#驗證密碼
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	#建立驗證的Token
	def generate_auth_token(self, expiration):
		s = Serializer(current_app.config['SECRET_KEY'],
					   expires_in=expiration)
		return s.dumps({'id': self.id}).decode('utf-8')

	#驗證auth token
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		return User.query.get(data['id'])

