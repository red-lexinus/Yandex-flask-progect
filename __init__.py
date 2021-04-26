from config import app
import flask
from flask import render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from models import *
from forms import *
from UserLogin import UserLogin
import database_functions as db_f

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизируйтесь пожалуйста'
login_manager.login_message_category = 'alert alert-success'


@login_manager.user_loader
def load_user(info):
    return UserLogin().create_log(info)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)
#
#         flask.flash('Logged in successfully.')
#
#         next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         if not is_safe_url(next):
#             return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')


@app.route('/main', methods=['GET', 'POST'])
# @login_required
def main():
    return render_template('main.html')


@app.route('/prof', methods=['GET', 'POST'])
@login_required
def prof():
    try:
        username = db_f.search_user_id(current_user.get_id())
        return render_template('prof.html', name=username)
    except:
        return prof()


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        db_f.change_password(int(current_user.get_id()), form.password.data)
        flash('Вы успешно изменили свой пароль',
              'alert alert-success')
        return redirect(request.args.get('next') or url_for('prof'))
    if 'password' in form.errors:
        flash('Длина вашего пароля слишком мала', 'alert alert-danger')
    return render_template('change_password.html', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        log_info = db_f.reg_user(form.username.data, form.password.data)
        if log_info[0]:
            # print(log_info[1][0])
            flash('Вы успешно зарегистрировались поздраляем(теперь для запоминания пароля авторизируйтесь)',
                  'alert alert-success')
            # user_login = UserLogin().create_log(log_info[1][0])
            # # # print(user_login.get_id())
            # login_user(user_login, remember=form.remember_me.data)
            return redirect(url_for('login'))
        else:
            flash(log_info[1], 'alert alert-danger')
    if 'username' in form.errors:
        flash('Длина вашего имени слишком мала', 'alert alert-danger')
    if 'password' in form.errors:
        flash('Длина вашего пароля слишком мала', 'alert alert-danger')
    return render_template('reg.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        try:
            if current_user.is_authenticated():
                return redirect(request.args.get('next') or url_for('prof'))
        except:
            pass
        form = LoginForm()
        if form.validate_on_submit():
            log_info = db_f.log_user(form.username.data, form.password.data)
            print(log_info)
            if log_info[0]:
                print(log_info[1][0])
                flash('Вы успешно вошли поздраляем', 'alert alert-success')
                user_login = UserLogin().create_log(log_info[1][0])
                # print(user_login.get_id())
                login_user(user_login, remember=form.remember_me.data)
                return redirect(request.args.get('next') or url_for('prof'))
            else:
                flash(log_info[1], 'alert alert-danger')

        if 'username' in form.errors:
            flash('Длина вашего имени слишком мала', 'alert alert-danger')
        if 'password' in form.errors:
            flash('Длина вашего пароля слишком мала', 'alert alert-danger')
        return render_template('log.html', form=form)
    except:
        login()


# @app.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():


@app.route('/disc', methods=['GET', 'POST'])
def disc():
    return render_template('main.html')


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    try:
        arr = db_f.search_topics(10)
        res = []
        for i in arr:
            new_arr = [d for d in i]
            elem = {'id': new_arr[0], 'id_author': new_arr[1], 'name': new_arr[2], 'info': new_arr[3],
                    'flag_tag': current_user.get_id() in ['1', str(new_arr[0])]}
            res.append(elem)
        return render_template('topics.html', topics=res)
    except:
        topic()


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('8values/index.html')


@app.route('/test/instructions', methods=['GET', 'POST'])
def instructions():
    return render_template('8values/instructions.html')


@app.route('/test/quiz', methods=['GET', 'POST'])
def quiz():
    return render_template('8values/quiz.html')


@app.route('/test/results', methods=['GET', 'POST'])
def res():
    economics = request.args.get('e', default=1, type=float)
    dyplomatic = request.args.get('d', default=1, type=float)
    civil = request.args.get('g', default=1, type=float)
    societal = request.args.get('s', default=1, type=float)
    return render_template('8values/results.html')


@app.route('/create_new_post', methods=['GET', 'POST'])
def create_new_post():
    try:
        form = CreatePost()
        if form.validate_on_submit():
            db_f.create_new_topic(int(current_user.get_id()), form.name.data, form.question.data, form.explanation.data)
            return redirect(url_for('prof'))
        return render_template('create_new_post.html', form=form)
    except:
        create_new_post()

if __name__ == '__main__':
    while True:
        try:
            app.run()
        except Exception as e:
            print(e.__class__.__name__)
