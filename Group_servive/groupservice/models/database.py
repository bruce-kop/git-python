# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Unicode(128), primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    pwd = db.Column(db.String(128))
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)

    def set_password(self, password):
        self.pwd = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.pwd, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

class oauths(db.Model):
    __tablename__ = 'oauths'
    id = db.Column(db.Unicode(128), primary_key=True, nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    oauth_type = db.Column(db.String(128), nullable=False)
    oauth_id = db.Column(db.String(128), nullable=False)
    unionid = db.Column(db.String(512))
    credentail = db.Column(db.String(512))

class user_extends(db.Model):
    __tablename__ = 'user_extends'
    id = db.Column(db.Unicode(128), primary_key=True, nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    is_online = db.Column(db.Integer)
    field = db.Column(db.String(128))
    value = db.Column(db.String(512))
