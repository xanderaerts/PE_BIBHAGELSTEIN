from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def create_app():
    #configuration app and db
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "bibhagelstein"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/dbbibhagelstein'
    db.init_app(app)

    from .main import main
    from .login import login

    app.register_blueprint(main,url_prefix='/')
    app.register_blueprint(login,url_prefix='/')


    #configuration login-manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'login.load_user'
    login_manager.init_app(app)

    from .dbmodels import Users

    @login_manager.user_loader
    def load_user(UserID):
        return Users.query.get(int(UserID))


    return app
