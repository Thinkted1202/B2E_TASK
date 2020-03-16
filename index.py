import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
	load_dotenv(dotenv_path)

from flask_migrate import Migrate
from app import create_app, db
from app.models.users import User
from app.models.shorturl import ShortUrl

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#遷移腳本
migrate = Migrate(app, db)

#新增帳號用
import click
@app.cli.command('add-user')
@click.argument("email")
@click.argument("username")
@click.argument("password")
def addUser(email,username,password):
		"Run the add-user"
		user = User(
			email=email,
			username=username,
			password=password
		)
		db.session.add(user)
		db.session.commit()

