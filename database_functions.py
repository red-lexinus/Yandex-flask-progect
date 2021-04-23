from models import *
from config import db
from sqlalchemy import text


# sql = text('select name from ')
# result = db.engine.execute(sql)
# names = [row[0] for row in result]

def check_username(username):
    return [True, 'сообщение']


def check_password(password):
    return [True, 'сообщение']


def check_username(username):
    return [True, 'сообщение']


def check_password(password):
    return [True, 'сообщение']


def check_new_topic(name, question, explanation):
    return [True, 'сообщение']


def check_new_main_comment(message):
    return [True]


def check_new_additional_comment(message):
    return [True]


def create_new_user(username, password):
    if not check_username(password)[0]:
        return check_username(password)[1]
    if not check_password(password)[0]:
        return check_password(password)[1]
    sql = text(f'select username from users where username = {username}')
    results = [row[0] for row in db.engine.execute(sql)]
    if len(results) != 0:
        return [False, 'Данное имя пользователя уже занято']
    i = User(username, password)
    db.session.add(i)
    db.session.commit()
    return [True, 'Поздравляю с успешной регистрацией']


def create_new_topic(id_author, name, question, explanation):
    if not check_new_topic(name, question, explanation)[0]:
        return check_new_topic(name, question, explanation)[1]

    topic = Topic(id_author=id_author, name=name, question=question, explanation=explanation)
    db.session.add(topic)
    db.session.commit()
    return [True, 'Поздравляю']


def create_new_main_comment(id_topic, id_author, message):
    if not check_new_main_comment(message)[0]:
        return check_new_main_comment(message)[1]
    main_comment = MainComment(id_topic=id_topic, id_author=id_author, message=message)
    db.session.add(main_comment)
    db.session.commit()
    return [True, 'Поздравляю']


def create_new_additional_comments(id_main_comment, id_author, message):
    if not check_new_main_comment(message)[0]:
        return check_new_main_comment(message)[1]
    main_comment = AdditionalComment(id_main_comment=id_main_comment, id_author=id_author, message=message)
    db.session.add(main_comment)
    db.session.commit()
    return [True, 'Поздравляю']
