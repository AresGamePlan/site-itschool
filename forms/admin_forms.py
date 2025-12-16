from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class UserFilterForm(FlaskForm):

    name = StringField("Имя пользователя", validators=[Optional()])

    role = SelectField("Роль", choices=[
        ("", "Все"),
        ("admin", "Администратор"),
        ("teacher", "Учитель"),
        ("student", "Студент"),
        ("user", "Пользователь")
    ])

    submit = SubmitField("Фильтровать")

class CreateCourseForm(FlaskForm):

    name = StringField("Название курса", validators=[DataRequired(), Length(min=3, max=20)])

    submit = SubmitField("Создать")

class CreateGroupForm(FlaskForm):

    name = StringField("Название группы", validators=[DataRequired(), Length(min=3, max=20)])

    course = SelectField("Выберите курс", coerce=int, validators=[DataRequired()])

    teacher = SelectField("Выберите преподавателя", coerce=int, validators=[DataRequired()])

    submit = SubmitField("Создать")

class EditUserForm(FlaskForm):
    id = IntegerField("Id",validators=[DataRequired()])

    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=100)])

    role = SelectField("Роль", choices=[
        ("", "Все"),
        ("admin", "Администратор"),
        ("teacher", "Учитель"),
        ("student", "Студент"),
        ("user", "Пользователь")
    ])

    submit = SubmitField("Сохранить")

class CreateScheduleForm(FlaskForm):
    group_id = IntegerField("group_id", validators=[DataRequired()])

    time_start = TimeField("Начало урока", validators=[DataRequired()])

    time_finish = TimeField("Конец урока", validators=[DataRequired()])

    monday = BooleanField("Понедельник")
    tuesday = BooleanField("Вторник")
    wednesday = BooleanField("Среда")
    thursday = BooleanField("Четверг")
    friday = BooleanField("Пятница")
    saturday = BooleanField("Суббота")
    sunday = BooleanField("Воскресенье")

    submit = SubmitField("Создать")

class TransactionForm(FlaskForm):
    user_id = IntegerField("user_id", validators=[DataRequired()])

    count_coins = IntegerField("Сколько коинов списать", validators=[DataRequired()])

    submit = SubmitField("Списать")

class ChangePasswordForm(FlaskForm):
    user_id = IntegerField("user_id", validators=[DataRequired()])

    new_password = StringField("Новый пароль", validators=[DataRequired(), Length(min=6, message="Минимум 6 символов")])

    submit = SubmitField("Изменить")
