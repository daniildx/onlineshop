from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # Создание экземпляра приложения
    app = Flask(__name__)

    # Загрузка конфигурации
    app.config.from_object(Config)

    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)

    # Настройка системы аутентификации
    login_manager.login_view = 'auth.login'  # Эндпоинт для входа
    login_manager.login_message_category = 'info'

    # Регистрация Blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.products import products_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')

    # Создание таблиц в базе данных
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    # Запуск приложения в режиме разработки
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)