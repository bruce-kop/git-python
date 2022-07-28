# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Message(db.Document):
    _id = db.StringField(required=True , max_length=128)
    user_id = db.StringField(required=True , max_length=128)
    from_u = db.StringField(required=True , max_length=128)
    centent = db.StringField(required=True , max_length=1024)
    group_id = db.StringField(required=True , max_length=128)
    is_send = db.StringField(required=True , max_length=128)
    create_data = db.StringField(required=True , max_length=128)
    meta = {
        "collection": "message",
        "index": [{
            'fields': ['id'],
            'unique': True,
        }]
    }
