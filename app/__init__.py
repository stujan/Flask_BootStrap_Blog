__author__ = 'sanjay'

from flask import  Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_sqlalchemy import  SQLAlchemy
from config import config
from flask_login import  LoginManager
from flask_pagedown import  PageDown

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    from . main import  main as blueprint

    app.register_blueprint(blueprint)

    from .auth import auth as auth
    app.register_blueprint(auth,url_prefix='/auth')
    login_manager.init_app(app)
    return app

