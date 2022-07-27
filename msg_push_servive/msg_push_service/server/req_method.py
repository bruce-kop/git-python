#python
#encoding = utf8

''' file:req_method.py
    class: ReqMethod. defines all request methods for the service
'''

from enum import Enum, unique, IntEnum
@unique
class ReqMethod(IntEnum):
    LOGINMSG = 4001
    SENDMSG = 4002
    SVRTRANMITMSG = 4003

    MSGREAD = 4004
    MSGSEARCHBY_USER = 4005
    MSGSEARCHBY_DATE = 4006
    MSGSEARCH_BY_PI_RREC = 4007
    MSGSEARCHBY_FILE = 4008
    MSGSEARCHBY_LINK = 4009
    MSGSEARCHBY_KEYWORD = 4010
    MSGSEARCHBY_CHAT = 4011
    MSGDELETE = 4012

class ReqMethodStr(Enum):
    LOGINMSG = 'login msg'
    SVRTRANMITMSG = 'tranmit msg'
