# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Message(db.Document):
    _id = db.StringField(required=True, max_length=128)
    msg_id = db.StringField(required=True, max_length=128)
    user_id = db.StringField(required=True, max_length=128)
    from_u = db.StringField(required=True, max_length=128)
    content = db.StringField(required=True, max_length=1024)
    group_id = db.StringField(required=True, max_length=128)
    msg_type = db.StringField(required=True, max_length=128)
    is_send = db.IntField(required=True, max_length=128)
    created_at = db.DateTimeField(required=True, max_length=128)
    meta = {
        "collection": "message",
        "index": [{
            'fields': ['id'],
            'unique': True,
        }]
    }
    #def __repr__(self):
        #return '{"msg_id":{}, "msg_type":{},"user_id":{}, "group_id":{}, "from_u":{}, "content":{}, “created_at”:{}}'.format(self.msg_id, self.msg_type, self.user_id, self.group_id, self.from_u, self.content, self.created_at)
