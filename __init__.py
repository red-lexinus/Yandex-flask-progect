from config import app
import flask
from flask import render_template, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from models import *
from forms import *
from UserLogin import UserLogin
import database_functions as db_f


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.create_log(UserLogin(), user_id)


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
def prof():
    return render_template('log.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    print(request.method)
    if request.method == "POST":
        print(2323)
        return render_template('reg.html', form=form)
        # res = database_functions.log_user(form.username, form.password)
    if 'username' in form.errors:
        flash('Длина вашего имени слишком мала', 'error')
    if 'password' in form.errors:
        flash('Длина вашего пароля слишком мала', 'error')
    return render_template('reg.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        log_info = db_f.log_user(form.username.data, form.password.data)
        if log_info[0]:
            flash('Вы успешно вошли поздраляем', 'alert alert-success')
            user_login = UserLogin().create_log(log_info[1])
            # print(user_login.get_id())
            login_user(user_login)
        else:
            flash(log_info[1], 'alert alert-danger')

    if 'username' in form.errors:
        flash('Длина вашего имени слишком мала', 'alert alert-danger')
    if 'password' in form.errors:
        flash('Длина вашего пароля слишком мала', 'alert alert-danger')
    return render_template('log.html', form=form)


# @app.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():



@app.route('/disc', methods=['GET', 'POST'])
def disc():
    return render_template('main.html')


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    return render_template('main.html')


if __name__ == '__main__':
    host = 'localhost'
    while True:
        try:
            app.run(host=host, port=8000, debug=True)
        except Exception as e:
            print(e.__class__.__name__)
