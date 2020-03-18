from . import api
from ..models.shorturl import ShortUrl
from ..models.redis import RedisHelper
from flask import request,jsonify
from .errors import errorhandler

@api.route('/shorturl/', methods=['GET','POST'])
def shorturl():
	url = request.get_json().get('url')
	#驗證是否式網址
	check_url = ShortUrl.check_url(url)
	if not check_url:
		return errorhandler('網址不符合規定')

	#產生shortkey
	short_key = ShortUrl.gen_shortKey(url)
	# return short_key
	#判斷shortkey和url是否已經存在
	if ShortUrl.query.filter_by(shortkey=short_key,url=url).first():
		return jsonify(ShortUrl.gen_shortUrl(short_key))
	#若有碰撞要另外處理

	#先輸入到Redis
	r = RedisHelper()
	r.set(short_key,url,3600)
	r.close()
	#產生短網址
	ShortUrl.add_url(short_key,url)
	return jsonify(ShortUrl.gen_shortUrl(short_key))


