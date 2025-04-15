from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Article
from forms import RegistrationForm, LoginForm
from config import Config

def configure_routes(app):
    @app.route('/')
    def index():
        articles = Article.query.order_by(Article.created_at.desc()).all()
        return render_template('index.html', articles=articles)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                city=form.city.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно!')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            flash('Неверный email или пароль')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))