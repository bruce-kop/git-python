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
    MSG_REVD = 4003
    MSGREAD = 4004

class ReqMethodStr(Enum):
    LOGINMSG = 'login msg'
    SVRTRANMITMSG = 'tranmit msg'
