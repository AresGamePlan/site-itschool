from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class AddStudemtForm(FlaskForm):
    pass

class AddCoinsForm(FlaskForm):
    student_id = IntegerField()
    group_id = IntegerField()
    all_lesson = BooleanField("Выполнение всех заданий + активность |+ 200 коинов| (получает только 1 ученик на уроке)")
    noall_lesson = BooleanField("Выполнение не все задачи запланированные на урок |+ 20 коинов|")
    activity_on_lesson = BooleanField("За активность на уроке |+ 10 коинов|")
    help_other = BooleanField("За помощь другим участникам |+ 10 коинов|")
    visit_all_lesson = BooleanField("За посещение всех занятий в месяце |+ 20 коинов|")
    idea_for_school = BooleanField("Идея для школы |+ 15 коинов|")
    discipline_mistake = BooleanField("Нарушение дисциплины |- 10 коинов|")
    no_completed_homework = BooleanField("Не выполнение дз |- 10 коинов|")
    lateness = BooleanField("Опоздание |- 10 коинов|")
    absence = BooleanField("Пропуск занятия |- 10 коинов|")

    comment = TextAreaField("Комментарий")

    submit = SubmitField("Начислить")