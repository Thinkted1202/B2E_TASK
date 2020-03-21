from . import api
from ..models.shorturl import ShortUrl
from ..helpers.redis_helper import RedisHelper
from ..helpers.hashids_helper import HashidsHelper

from flask import request,jsonify
from .errors import errorhandler

@api.route('/shorturl/', methods=['GET','POST'])
def shorturl():
	url = request.get_json().get('url')
	#驗證是否式網址
	check_url = ShortUrl.check_url(url)
	if not check_url:
		return errorhandler('網址不符合規定')
	#判斷url是否存在了
	shorturl_obj = ShortUrl.query.filter_by(url=url).first()
	if shorturl_obj:
		return jsonify(ShortUrl.gen_shortUrl(shorturl_obj.shortkey))

	#先輸入到DB
	shorturl_obj = ShortUrl(url=url).save_to_db()
	#將ID透過hashid加密
	hash_obj = HashidsHelper()
	short_key = hash_obj.hashid(shorturl_obj.id)
	del hash_obj

	# 先輸入到Redis
	redis_obj = RedisHelper()
	redis_obj.set(short_key,url,3600)
	redis_obj.close()
	#回寫DB
	shorturl_obj.shortkey = short_key
	shorturl_obj.update_to_db()
	# #產生短網址
	return jsonify(ShortUrl.gen_shortUrl(short_key))


