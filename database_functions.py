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


def create_new_user(name, password):
    if not check_username(password)[0]:
        return check_username(password)[1]
    if not check_password(password)[0]:
        return check_password(password)[1]
    sql = text(f'select username from users where username = "{name}"')
    results = [row[0] for row in db.engine.execute(sql)]
    if len(results) != 0:
        return [False, 'Данное имя пользователя уже занято']
    i = User(name, password)
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


def search_topics_through_user_id(user_id):
    sql = text(f'select id, id_author, name, question from topics where id_author = {user_id}')
    results = [row for row in db.engine.execute(sql)]
    return results


def search_topics_through_username(username):
    sql = text(f'select id from users where username = "{username}"')
    results = [row for row in db.engine.execute(sql)]
    try:
        sql = text(f'select id, id_author, name, question from topics where id_author = {results[0][0]}')
        results = [row for row in db.engine.execute(sql)]
        return results
    except IndexError:
        return []


def search_topics(max_len, name='', question=''):
    sql = text(f'select id, id_author, name, question from topics')
    results = []
    for row in db.engine.execute(sql):
        if name in row[2] and question in row[3]:
            results.append(row)
            if len(results) == max_len:
                return results
    return results


def search_comments(id_topic):
    sql = text(f'select id,id_topic, id_author, message  from main_comments where id_topic = {id_topic}')
    results = [[row] for row in db.engine.execute(sql)]
    for i in range(len(results)):
        sql = text(
            f'select id,id_main_comment, id_author, message  from additional_comments where id_main_comment = {results[i][0][0]}')
        results[i].append([row for row in db.engine.execute(sql)])
    return results



