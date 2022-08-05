#encoding=utf8
import json
import struct
from msg_push_service.utils.Logger import logger

#通过value获取字典中的key
def get_dict_key(dic, value):
    key = None
    try:
        key = list(dic.keys())[list(dic.values()).index(value)]
    except Exception as e:
        return key
    finally:
        return key


def parse_head(data):
    '''dec:data format:
        {
        "v": 1.0,
        "l": 0
        }
        len is 8
    '''
    v = 0.0
    l = 0
    if data:
        try:
            v, l = struct.unpack('fi', data)
        except Exception as e:
            logger.debug(e)
            return v, l
        finally:
            return v, l
    else:
        return v, l

def is_methed(data, method):
    if int(data["method"]) != method:
        return False

    return True

def pop_user(unread_list,userid):
    '''the unread_list is a string, it's format is sdhfsfsaf,jlsidjfsidfj,sewerwe,werwerwe,'''
    i = unread_list.find(userid)
    if i != -1:
        tmp = unread_list[0:i] + unread_list[i+len(userid)+1:len(unread_list)]
    else:
        tmp = None
    return tmp

def find_msg(msgs, msg_id):
    '''the msgs is a string, it's format is {"msg_id":"sdfsdf", "content":”fsdfsdf“},{"msg_id":"sdfsd44f", "content":”fsdfs44df“},'''
    i = msgs.find(msg_id)
    if i == -1:
        msg = None
    else:
        j = msgs[0:i].rfind('{')
        k = msgs[i:len(msgs)].find('}')
        msg = msgs[j:k+i+1]

    return msg

def find_msg(msgs, msg_id):
    '''the msgs is a string, it's format is {"msg_id":"sdfsdf", "content":”fsdfsdf“},{"msg_id":"sdfsd44f", "content":”fsdfs44df“},'''
    i = msgs.find(msg_id)
    if i == -1:
        msg = None
    else:
        j = msgs[0:i].rfind('{')
        k = msgs[i:len(msgs)].find('}')
        msg = msgs[j:k+i+1]

    return msg

