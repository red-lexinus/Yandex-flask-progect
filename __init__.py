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
        e, d, g, s = db_f.search_test_from_id(current_user.get_id())
        return render_template('prof.html', name=username, e=e, d=d, g=g, s=s)
    except Exception as e:
        print(e)
        print(e.__class__.__name__)
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


@app.route('/subject<int:topic_id>')
def subject(topic_id):
    data = db_f.search_comments(topic_id)
    new_data = []
    info = db_f.search_topics(topic_id)
    topic_info = {'id_topic': info[0][0], 'author': db_f.search_user_id(info[0][1]), 'question': info[0][2],
                  'explanation': info[0][3],
                  'author_id': info[0][1]}
    for i in data:
        comments = []
        for d in i[1]:
            new_keys = {
                'id': d[0], 'id_comment': d[1], 'author': db_f.search_user_id(d[2]), 'message': d[3]
            }
            comments.append(new_keys)
        main_keys = {
            'id': i[0][0], 'id_topic': i[0][1], 'author': db_f.search_user_id(i[0][2]), 'message': i[0][3],
            'comments': comments
        }
        new_data.append(main_keys)
    print(len(new_data))
    return render_template('topic.html', comments=new_data, topic_info=topic_info)


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    arr = db_f.search_topics(10)
    res = []
    for i in arr:
        new_arr = [d for d in i]
        elem = {'id': new_arr[0], 'id_author': new_arr[1], 'name': new_arr[2], 'info': new_arr[3],
                'flag_tag': current_user.get_id() in ['1', str(new_arr[0])], 'int_id': int(new_arr[0])}
        res.append(elem)
    return render_template('topics.html', topics=res)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('8values/index.html')


@app.route('/test/instructions', methods=['GET', 'POST'])
def instructions():
    return render_template('8values/instructions.html')


@app.route('/test/quiz', methods=['GET', 'POST'])
def quiz():
    return render_template('8values/quiz.html')


@app.route('/del_post<int:number>', methods=['GET', 'POST'])
def del_post(number):
    db_f.del_post(number)
    return redirect(url_for('topic'))


@app.route('/test/results', methods=['GET', 'POST'])
def res():
    e = request.args.get('e', default=1, type=str)
    d = request.args.get('d', default=1, type=str)
    g = request.args.get('g', default=1, type=str)
    s = request.args.get('s', default=1, type=str)

    db_f.save_test_result(current_user.get_id(), e, d, g, s)

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
