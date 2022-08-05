#encoding =utf8
import json
import uuid
import datetime
from msg_push_service.utils.RedisOperator import redis
from msg_push_service.utils.DBHelper import *

def send_msg(data, userid, user_dict):
    #消息转发给接收方
    try:
        content = data['message'].get('content')
        msg_id = data['message'].get('msg_id')
        sender = userid
        receiver = data['message'].get('receiver')
        msg_type = data['message'].get('msg_type')
        created_at = data['message'].get('created_at')
        group_id = 'group_id' in data['message'] and data['message']['group_id'] or ""
    except Exception as e:
        raise e
        return

    socket = user_dict.get(receiver)
    if socket:
        #如果用户在线，转发消息
        msg = dg = {"method":"4002", "message": {"msg_id": msg_id, "content":content, "sender":sender, "group_id": group_id, "msg_type": msg_type, "created_at": created_at}}
        msg = json.dumps(msg)
        logger.debug(msg)
        r = socket.send(msg.encode(encoding='utf-8'))
    #存入离线缓存
    try:

        value = {"id": msg_id,  "content": content, "msg_type": msg_type, "sender":sender, "receiver":receiver, "group_id":group_id, "created_at": created_at}
        value = json.dumps(value)
        redis.lpush(receiver+'-m', value)
    except Exception as e:
        logger.error(e)

def send_read(data, user_dict):
    '''data is a dict, format is {"data_type": "read", 'msg_ids': msgs, "sender": sender, "reciever": userid}'''
    logger.info(data)
    msg_ids = data.get('msg_ids')
    sender = data.get('sender')
    receiver = data.get('receiver')
    socket = user_dict.get(sender)

    #socket = redis.get(sender)
    msg = dg = {"method": "4004", "message":{"msg_ids": msg_ids, "receiver": receiver}}
    msg = json.dumps(msg)
    socket.send(msg.encode(encoding='utf-8'))
