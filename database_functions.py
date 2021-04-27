from models import *
from config import db
from sqlalchemy import text


# sql = text('select name from ')
# result = db.engine.execute(sql)
# names = [row[0] for row in result]


def check_new_topic(name, question, explanation):
    return [True, 'сообщение']


def check_new_main_comment(message):
    return [True]


def check_new_additional_comment(message):
    return [True]


def search_user(name):
    sql = text(f'select * from users where username = "{name}"')
    results = [row for row in db.engine.execute(sql)]
    if len(results) != 0:
        return [True, [elem for elem in results[0]]]
    return [False, 'Пользователя с таким именем не существует']


def log_user(name, password):
    sql = text(f'select * from users where username = "{name}"')
    results = [row for row in db.engine.execute(sql)]
    # print(results)
    if len(results) != 0:
        if results[0][2] == password:
            return [True, [elem for elem in results[0]]]
        return [False, 'Вы указали неверный пароль']
    return [False, 'Пользователя с таким именем не существует']


def reg_user(name, password):
    sql = text(f'select username from users where username = "{name}"')
    results = [row[0] for row in db.engine.execute(sql)]
    if len(results) != 0:
        return [False, 'Пользователь с таким именем уже существует']
    i = User(name, password)
    db.session.add(i)
    db.session.commit()
    return search_user(name)


def create_new_user(name, password):
    sql = text(f'select username from users where username = "{name}"')
    results = [row[0] for row in db.engine.execute(sql)]
    if len(results) != 0:
        return False
    i = User(name, password)
    db.session.add(i)
    db.session.commit()
    return True


def save_test_result(user_id, e, d, g, s):
    print(user_id)
    sql = text(f'select id from tests where id = {user_id}')
    results = [row[0] for row in db.engine.execute(sql)]
    print(results)
    if len(results) != 0:

        i = Test.query.get(user_id)
        i.economic = e
        i.dyplomatic = d
        i.civic = g
        i.social = s
    else:
        i = Test(user_id, e, d, g, s)
    db.session.add(i)
    db.session.commit()
    return True


def search_test_from_id(user_id):
    try:
        sql = text(f'select * from tests where id = {user_id}')
        results = [row[1:] for row in db.engine.execute(sql)]
        if results[0]:
            return results[0]
        return [50, 50, 50, 50]
    except:
        return [50, 50, 50, 50]


def search_user_id(user_id):
    sql = text(f'select username from users where id = "{user_id}"')
    results = [row[0] for row in db.engine.execute(sql)]
    return results[0]


def create_new_topic(id_author, name, question, explanation):
    if not check_new_topic(name, question, explanation)[0]:
        return check_new_topic(name, question, explanation)[1]

    topic = Topic(id_author=id_author, name=name, question=question, explanation=explanation)
    db.session.add(topic)
    db.session.commit()
    return True


def create_new_main_comment(id_topic, id_author, message):
    if not check_new_main_comment(message)[0]:
        return check_new_main_comment(message)[1]
    try:
        main_comment = MainComment(id_topic=id_topic, id_author=id_author, message=message)
        db.session.add(main_comment)
        db.session.commit()
        return True
    except:
        main_comment = MainComment(id_topic=id_topic, id_author=id_author, message=message)
        db.session.add(main_comment)
        db.session.commit()
        return True


def create_new_additional_comments(id_main_comment, id_author, message):
    if not check_new_main_comment(message)[0]:
        return check_new_main_comment(message)[1]
    try:
        main_comment = AdditionalComment(id_main_comment=id_main_comment, id_author=id_author, message=message)
        db.session.add(main_comment)
        db.session.commit()
        return True
    except:
        main_comment = AdditionalComment(id_main_comment=id_main_comment, id_author=id_author, message=message)
        db.session.add(main_comment)
        db.session.commit()
        return True


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


def search_topic(id_topic):
    sql = text(f'select id, id_author, name, question from topics where id = {id_topic}')
    results = [row for row in db.engine.execute(sql)]
    return results


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


def del_post(id_topic):
    db.engine.execute(text(f'DELETE  FROM  topics WHERE id = {id_topic}'))


def change_password(user_id, new_password):
    item = User.query.get(user_id)
    item.password = new_password
    db.session.commit()
