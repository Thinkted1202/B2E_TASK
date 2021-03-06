from .. import db
from flask import current_app
from datetime import datetime
from urllib.parse import urlparse
import hashlib
import base64

class ShortUrl(db.Model):
	__tablename__ = 'shorturls'
	id = db.Column(db.Integer, primary_key=True)
	shortkey = db.Column(db.String(64), unique=True, index=True)
	url = db.Column(db.String(64))
	created_at = db.Column(db.DateTime(), default=datetime.utcnow)

	def __init__(self, **kwargs):
		super(ShortUrl, self).__init__(**kwargs)

	#簡單驗證網址
	def check_url(url):
		return (urlparse(url).scheme == 'http') or (urlparse(url).scheme == 'https')

	#產生出短網址
	def gen_shortUrl(short_key):
		return "http://"+current_app.config['HOST']+"/{}".format(short_key)

	#產生shortkey
	def gen_shortKey(url):
		return base64.b64encode(hashlib.md5(str(url).encode('utf-8')).digest())[0:8]

	#新增到紀錄
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
		return self

	def update_to_db(self):
		db.session.commit()

