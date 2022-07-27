# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Unicode(128), primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128))
    QR_code = db.Column(db.String(512))
    notice = db.Column(db.String(512))
    note = db.Column(db.String(512))
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
    #group_user = relationship("GroupUser", backref="group")
    def __init__(self, *args, **kw):
        super(Group, self).__init__(*args, **kw)

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

class GroupUser(db.Model):
    __tablename__ = 'group_user'
    id = db.Column(db.Unicode(128), primary_key=True, nullable=False)
    group_id = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer)
    nickname = db.Column(db.String(128))
    note = db.Column(db.String(512))

    #group = relationship("Group", backref="group_user")


class GroupAddrBook(db.Model):
    __tablename__ = 'group_addr_book'
    id = db.Column(db.Unicode(128), primary_key=True, nullable=False)
    group_id = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    note = db.Column(db.String(512))

class GroupRoleAu(db.Model):
    __tablename__ = 'group_role_au'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    au_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(512))

class GroupRole(db.Model):
    __tablename__ = 'grouprole'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String(128), nullable=False)
    note = db.Column(db.String(512))

class GroupAu(db.Model):
    __tablename__ = 'groupau'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    au_name = db.Column(db.String(128), nullable=False)
    note = db.Column(db.String(512))

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
