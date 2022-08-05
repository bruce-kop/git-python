#encoding=utf8
import datetime
import uuid

import threading
from msg_push_service.server.send_thread import *
import grpc
from msg_push_service.server import groupservice_pb2_grpc
from msg_push_service.server import groupservice_pb2
from msg_push_service.utils.DBHelper import mongopwd

class GroupMsgSendThread(threading.Thread):
    ''''自定义数据处理线程类，#从队列中获取群消息，已读消息进行转发'''
    def __init__(self, ThreadID, name, *args):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        self.name = name
        self.msg_q = args[0].msg_q
        self.pool = args[0].pool
        self.user_dict = args[0].user_dict

    def run(self):
        while True:
            # 对所有在线客户端发送的消息进行响应
            data = self.msg_q.get()
            if not data:
                continue
            try:
                if not data['message'].get('data_type'):
                    sender = data['message'].get('sender')
                    send_msg(data, sender, self.user_dict)
                    if data['message'].get('group_id'):
                        single_chat_msg_proc(data)
                    #f = self.pool.submit(send_msg, data)
                else:
                    send_read(data, self.user_dict)
                    #f = self.pool.submit(send_read, data)
            except Exception as e:
                logger.debug(e)
                continue

def single_chat_msg_proc(data, userid = None, msg_q = None):
    # 存储数据,缓存unread_list和read_list
    try:
        content = data['message'].get('content')
        msg_id = data['message'].get('msg_id')
        if userid:
            sender = userid
        else:
            sender = data['message'].get('sender')
        receiver = data['message'].get('receiver')
        msg_type = data['message'].get('msg_type')
        group_id = data['message'].get('group_id')
    except Exception as e:
        raise e

    created_at = datetime.datetime.now()
    try:
        # 同时保存到mongoDB

        data_list = [{"id": msg_id, "content": content, "msg_type": msg_type, "created_at": created_at}]
        res = mongodb.insert(table='message', data_list=data_list)

        # 保存发件箱索引
        data_list = [{"user_id": sender, "receiver": receiver, "msg_id": msg_id,"group_id": group_id,}]
        res = mongodb.insert(table='sender_box', data_list=data_list)

        # 保存收件箱索引
        data_list = [{"user_id": receiver, "sender": sender, "msg_id": msg_id, "group_id": group_id,}]
        res = mongodb.insert(table='receiver_box', data_list=data_list)
    except Exception as e:
        logger.error(e)

    try:
        # 缓存消息的unread_list和read_list
        key = msg_id + '-u'
        redis.lpush(key, receiver)

    except Exception as e:
        raise e

    if group_id:
        #如果是群组消息将再重复放进队列中，直接return
        return

    msg = {"message": {"msg_id": msg_id, "content": content, "sender": sender, "receiver": receiver, "group_id": group_id,
                       "msg_type": msg_type,"created_at": created_at.timestamp()}}
    try:
        if msg_q:
            msg_q.put(msg)
    except Exception as e:
        raise e

def group_chat_msg_proc(data, userid, msg_q):
    #获取所有成员，投递到消息发送队列，然后存储消息（离线的还要存储到缓存）,缓存unread_list和read_list
    # 存储数据,缓存unread_list和read_list
    try:
        content = data['message'].get('content')
        msg_id = data['message'].get('msg_id')
        msg_type = data['message'].get('msg_type')
        group_id = data['message'].get('group_id')
    except Exception as e:
        logger.debug(e)

    sender = userid

    # 获取所有群成员,grpc方案，从groupservice获取
    members = None
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = groupservice_pb2_grpc.GroupServiceStub(channel)
            response = stub.GetMembers(groupservice_pb2.membersRequest(group_id=group_id))
            members = json.loads(response.message)
    except Exception as e:
        logger.debug(e)

    # 缓存消息的unread_list和read_list
    key = msg_id + '-u'

    for member in members:
        redis.lpush(key, member)
        #扩散消息，投递到消息队列中
        created_at = datetime.datetime.now().timestamp()
        msg = {"message":{"msg_id": msg_id, "content": content, "sender": sender, "receiver": member, "group_id": group_id, "msg_type": msg_type,"created_at": created_at}}
        try:
            msg_q.put(msg)
        except Exception as e:
            logger.debug(e)

def recvd_msg_proc(data, userid):
    try:
        # 收到确认消息，删除离线消息缓存
        msg_id = data['message'].get('msg_id')
        redis.lrem(userid+'-m', 1, msg_id)
    except Exception as e:
        logger.error(e)

def read_msg_proc(data, userid, msg_q):
    logger.info(data)
    sender_msgs = data['message']
    for sender_msg in sender_msgs:
        sender= sender_msg.get("sender")
        msgs = sender_msg.get('msgs')

        #更新已读未读列表的缓存
        for msg in msgs:
            msg_id = sender_msg.get('msg_id')
            if userid in redis.lrange(msg_id + '-u', 0, -1):
                #未读缓存队列
                redis.lrem(msg_id + '-u', userid, '1')

            #已读缓存队列
            redis.lpush(msg_id + '-r', userid)

        #将发送消息组装好，投入队列，等待线程进行通知消息发送者处理。
        data = {"data_type": "read", 'msg_ids': msgs, "sender": sender, "receiver": userid}
        msg_q.put(data)








