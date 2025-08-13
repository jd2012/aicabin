from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# initialize extensions

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cabin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from . import routes, models  # noqa: F401
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app
