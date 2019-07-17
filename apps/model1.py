from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import  datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    login_time = db.Column(db.Integer)
    session_token='123213dsfw3432'

    def __init__(self,id,username,password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return self.session_token

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def update(self):
        return session_commit()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def __repr__(self):
        return '<User %r>' % self.username

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    order = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return '<Menu %r>' % self.name

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(32))
    disabled = db.Column(db.Boolean, default=False)
    comment_type = db.Column(db.String(64), default='comment')
    reply_to = db.Column(db.String(128), default='notReply')

    def __str__(self):
        return "Comment(id='%s')" % self.id

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason