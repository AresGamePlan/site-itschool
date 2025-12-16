from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):

    fullname = StringField("ФИО пользователя", validators=[DataRequired(), Length(min=3, max=50)])

    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=30)])

    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, message="Минимум 6 символов")])

    confirm_password = PasswordField("Подтвердить пароль", validators=[DataRequired(), EqualTo("password", message="Пароли должны совпадать")])

    submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=30)])

    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, message="Минимум 6 символов")])

    remember_me = BooleanField("Запомнить меня")

    submit = SubmitField("Вход")