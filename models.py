from config import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, name, password):
        self.username, self.password = name, password

    def __repr__(self):
        return self.name


class Test(db.Model, UserMixin):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    economic = db.Column(db.Text, nullable=False)
    dyplomatic = db.Column(db.Text, nullable=False)
    civic = db.Column(db.Text, nullable=False)
    social = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, e, d, g, s):
        self.id, self.economic, self.dyplomatic, self.civic, self.social = user_id, e, d, g, s

    def __repr__(self):
        return self.id


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    id_author = db.Column(db.Integer, primary_key=False)
    name = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(400), nullable=False)
    explanation = db.Column(db.String(1600), nullable=True)


class MainComment(db.Model):
    __tablename__ = 'main_comments'
    id = db.Column(db.Integer, primary_key=True)
    id_topic = db.Column(db.Integer, primary_key=False)
    id_author = db.Column(db.Integer, primary_key=False)
    message = db.Column(db.String(1600), nullable=False)


class AdditionalComment(db.Model):
    __tablename__ = 'additional_comments'
    id = db.Column(db.Integer, primary_key=True)
    id_main_comment = db.Column(db.Integer, primary_key=False)
    id_author = db.Column(db.Integer, primary_key=False)
    message = db.Column(db.String(1600), nullable=False)



# db.create_all()