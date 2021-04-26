from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=200)])
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')


class RegForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=5, max=200)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=200)])
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Зарегестрироваться')


class ChangePassword(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Изменить пароль')


class CreatePost(FlaskForm):
    name = StringField('Название темы', validators=[DataRequired(), Length(min=5, max=100)])
    question = TextAreaField('Ваш вопрос', validators=[DataRequired(), Length(min=5, max=400)])
    explanation = TextAreaField('Развёрнутый вопрос', validators=[DataRequired(), Length(max=1600)])
    submit = SubmitField('Создать тему')
