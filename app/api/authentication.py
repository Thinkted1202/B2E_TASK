from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models.users import User
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

#驗證使用者
@auth.verify_password
def verify_password(email_or_token, password):
	if email_or_token == '':
		return False
	#沒有密碼就確認是否使用token
	if password == '':
		g.current_user = User.verify_auth_token(email_or_token)
		g.token_used = True
		return g.current_user is not None
	#使用者驗證取得token會用到
	user = User.query.filter_by(email=email_or_token.lower()).first()
	if not user:
		return False
	g.current_user = user
	g.token_used = False
	return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

#所有的API都需要被驗證
@api.before_request
@auth.login_required
def before_request():
	pass

#取得token
@api.route('/tokens', methods=['POST'])
def get_token():
	if g.token_used:
		return unauthorized('Invalid credentials')
	return jsonify({'token': g.current_user.generate_auth_token(
		expiration=3600), 'expiration': 3600})