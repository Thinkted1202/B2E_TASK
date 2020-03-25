from flask import current_app,redirect
from flask_caching import Cache
from ..models.shorturl import ShortUrl
from . import main

@main.route('/<short_key>')
def redirect_to_url(short_key):
	#URL From Redis Cache
    cache = Cache(current_app, config=current_app.config['REDIS_CONFIG'])
    url = cache.get(short_key)
    if url is not None:
        return redirect(url)

	#URL From DB
    ShortUrlObj = ShortUrl.query.filter_by(shortkey=short_key).first()
    if ShortUrlObj is None:
        return "None Url"
    cache.set(short_key, ShortUrlObj.url)
    #return redirect(ShortUrlObj.url)