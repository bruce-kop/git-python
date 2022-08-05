# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Message(db.Document):
    _id = db.StringField(required=True, max_length=128)
    id = db.StringField(required=True, max_length=128)
    content = db.StringField(required=True, max_length=1024)
    msg_type = db.StringField(required=True, max_length=128)
    created_at = db.DateTimeField(required=True, max_length=128)
    meta = {
        "collection": "message",
        "index": [{
            'fields': ['id'],
            'unique': True,
        }]
    }

class SenderBox(db.Document):
    _id = db.StringField(required=True, max_length=128)
    user_id = db.StringField(required=True, max_length=128)
    receiver = db.StringField(required=True, max_length=128)
    msg_id = db.StringField(required=True, max_length=128)
    gruop_id = db.StringField(required=True, max_length=128)

    meta = {
        "collection": "sender_box",
    }

class ReceiverBox(db.Document):
    _id = db.StringField(required=True, max_length=128)
    user_id = db.StringField(required=True, max_length=128)
    sender = db.StringField(required=True, max_length=128)
    msg_id = db.StringField(required=True, max_length=128)
    gruop_id = db.StringField(required=True, max_length=128)

    meta = {
        "collection": "receiver_box",
    }