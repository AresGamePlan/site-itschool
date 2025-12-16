from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class EditDataForm(FlaskForm):
    user_id = IntegerField("user_id", validators=[DataRequired()])

    fullname = StringField("ФИО:", validators=[DataRequired()])

    login = StringField("Логин:", validators=[DataRequired()])

    submit = SubmitField("Изменить")