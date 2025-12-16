from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash

from models.database import User, db
from forms.auth_forms import RegisterForm, LoginForm

from localization.base import text, language

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

class RegisterView(MethodView):
    decorators = [language]

    def get(self, **kwargs):
        form = RegisterForm()
        
        return render_template("auth/register.html", form = form, data = kwargs)
    
    def post(self, **kwargs):
        form = RegisterForm()
        if form.validate_on_submit(): # Пересмотреть другие подобные участки кода под такой формат
            fullname = form.fullname.data
            username = form.username.data
            password = form.password.data


            if User.query.filter_by(username=username).first():
                flash("Пользователь уже существует!", "warning")
                return redirect(url_for("auth.register"))
            
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            new_user = User(username=username, fullname=fullname, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash("Регистрация успешна! Теперь войдите.", "succes")
            return redirect(url_for("auth.login"))
        return render_template("auth/register.html", form=form, data = kwargs)
    
class LoginView(MethodView):
    decorators = [language]

    def get(self, **kwargs):
        form = LoginForm()
        return render_template("auth/login.html", form=form, data = kwargs)
    
    def post(self, **kwargs):
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user, remember=remember_me)
                return redirect(url_for("main.index"))
            else:
                flash("Неверный логин или пароль", "danger")
                return redirect(url_for("auth.login"))
        return render_template("auth/login.html", form=form, data = kwargs)
        
class LogoutView(MethodView):
    decorators = [login_required]
    def get(self, **kwargs):
        logout_user()
        return redirect(url_for("main.index"))
    
# Регистрация URL маршрутов
auth_bp.add_url_rule("/register", view_func=RegisterView.as_view("register"))
auth_bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
auth_bp.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))