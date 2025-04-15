from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import configure_routes
from api import api
import argparse


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    configure_routes(app)
    api.init_app(app)

    return app


def setup_cli():
    parser = argparse.ArgumentParser(description='Manage the Flask application')
    parser.add_argument('--init-db', action='store_true', help='Initialize the database')
    parser.add_argument('--create-admin', help='Create admin user (email)')
    return parser


if __name__ == '__main__':
    app = create_app()
    parser = setup_cli()
    args = parser.parse_args()

    with app.app_context():
        if args.init_db:
            db.create_all()
            print("Database initialized!")
        elif args.create_admin:
            # Реализация создания админа
            pass
        else:
            app.run(debug=True)