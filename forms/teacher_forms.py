from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class AddStudemtForm(FlaskForm):
    pass

class AddCoinsForm(FlaskForm):
    student_id = IntegerField()
    group_id = IntegerField()
    lesson = BooleanField("За выполнение задания на уроке")
    hard_lesson = BooleanField("За выполнения сложного задания")
    help_other = BooleanField("За помощь другим участникам")
    visit_all_lesson = BooleanField("За посещение всех занятий в месяце")
    idea_for_school = BooleanField("Идея для школы")
    breach_on_lesson = BooleanField("Нарушение дисциплины, не выполнение дз, пропуск")

    comment = TextAreaField("Комментарий")

    submit = SubmitField("Начислить")