from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=5, max=200)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=200)])
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')


class RegForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=5, max=200)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=200)])
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Зарегестрироваться')
