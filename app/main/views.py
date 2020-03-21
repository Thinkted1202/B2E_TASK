from flask import redirect
from ..models.shorturl import ShortUrl
from app.helpers.redis_helper import RedisHelper
from . import main

@main.route('/<short_key>')
def redirect_to_url(short_key):
	#URL From Redis Cache
	r = RedisHelper()
	url = r.get(short_key)
	if url is not None:
		r.close()
		return redirect(url)

	#URL From DB
	ShortUrlObj = ShortUrl.query.filter_by(shortkey=short_key).first()
	if ShortUrlObj is None:
		return "None Url"
	#Cache 1hr
	r.set(short_key,ShortUrlObj.url,3600)
	r.close()
	return redirect(ShortUrlObj.url)

