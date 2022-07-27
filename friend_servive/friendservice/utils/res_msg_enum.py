#python
#encoding = utf8

''' file:res_msg_enum.py
    class: ResMSG. defines all response ResMSG for the service
'''

from enum import Enum, unique

@unique
class ResCode(Enum):
    COMMON_SUCCESS = 200
    PARAMS_IS_EMPTY = 201
    INNER_ERR = 202

    VERRIFY_CODE_SUCCESS = 300
    VERRIFY_CODE_FAILED = 301
    REGISTER_SUCCESS = 400
    REGISTER_PWD_INVALID = 401
    REGISTER_PHONE_FORMAT_INVALID = 402
    REGISTER_VERRIFY_CODE_ERROR = 403
    REGISTER_USER_EXISTS = 405

    LONIN_SUCCESS = 500
    LOGIN_USER_OR_PWD_ERR = 501
    LOGIN_VERIFYCODE_ERR = 502
    LOGIN_EXCEEDS = 503

    LOGOUT_SUCCESS = 600
    LOGOUT_FAILED = 601
    TOKEN_INVALID = 602

    UNSUBSCRIBE_SUCCESS = 700
    UNSUBSCRIBE_FAILED = 701
    UNSUBSCRIBE_DELETE_FAILED = 702

    PRECISE_QUERY_SUCCESS = 800
    PRECISE_QUERY_FAIlED = 801

    PWD_MODIFY_SUCCESS = 900
    PWD_MODIFY_FAILED = 901

    PHONE_MODIFY_SUCCESS = 1000
    PHONE_MODIFY_FAILED = 1001

    FRIEND_ADD_SUCCESS = 1100
    FRIEND_ADD_FRIENDID_INVALID = 1101

    FRIEND_DEL_SUCCESS = 1200
    FRIEND_DEL_FRIENDID_INVALID = 1201

    FRIEND_SET_SUCCESS = 1300
    FRIEND_SET_PARAM_INVALID = 1301

    FRIEND_SET_NOTE_SUCCESS = 1400
    FRIEND_SET_NOTE_PARAM_INVALID =1401

    FRIEND_LIST_PARAM_INVALID = 1501
    FRIEND_LIST_SUCCESS = 1500

    FRIEND_SET_LABEL_SUCCESS = 1600
    FRIEND_SET_LABEL_PARAM_INVALID = 1601


@unique
class ResMSG(Enum):
    COMMON_SUCCESS = 'request success.'
    PARAMS_IS_EMPTY = 'request param is empty.'
    INNER_ERR = 'service inner error.'

    VERRIFY_CODE_SUCCESS = 'get verify code success.'
    VERRIFY_CODE_FAILED = 'get verify code faild.'

    REGISTER_SUCCESS = 'register success.'
    REGISTER_PWD_INVALID = "The password is invalid."
    REGISTER_PHONE_FORMAT_INVALID = "phone format is invalid."
    REGISTER_VERRIFY_CODE_ERROR = "verifycode is error."
    REGISTER_USER_EXISTS = 'user exists'

    LONIN_SUCCESS = 'login sucsses.'
    LOGIN_USER_OR_PWD_ERR = 'username or password is error.'
    LOGIN_VERIFYCODE_ERR = 'verify code is error.'
    LOGIN_EXCEEDS = 'login failed exceeds the limit.'

    LOGOUT_SUCCESS = 'log out success.'
    LOGOUT_FAILED = 'log out failed.'
    TOKEN_INVALID = 'token invalid.'

    UNSUBSCRIBE_SUCCESS = 'user unsubscribe success.'
    UNSUBSCRIBE_FAILED = 'user unsubscribe failed.'
    UNSUBSCRIBE_DELETE_FAILED = 'user delete failed.'

    PRECISE_QUERY_SUCCESS = 'user preccise query success.'
    PRECISE_QUERY_FAIlED = 'user preccise query failed.'

    PWD_MODIFY_SUCCESS = 'password is modified.'
    PWD_MODIFY_FAILED = 'password modify failure.'

    PHONE_MODIFY_SUCCESS = 'phone is modified.'
    PHONE_MODIFY_FAILED = 'phone modify failure.'

    FRIEND_ADD_SUCCESS = 'friend add success.'
    FRIEND_ADD_FRIENDID_INVALID = 'ADD friend id is invalid.'

    FRIEND_DEL_SUCCESS = 'friend delete success.'
    FRIEND_DEL_FRIENDID_INVALID = 'DEL friend id is invalid.'

    FRIEND_SET_SUCCESS = 'friend set permission success.'
    FRIEND_SET_PARAM_INVALID = 'friend id or permission is invalid.'

    FRIEND_SET_NOTE_SUCCESS = 'friend set note success.'
    FRIEND_SET_NOTE_PARAM_INVALID = 'friend id or note is invalid.'

    FRIEND_LIST_PARAM_INVALID = 'friend pageSize and currentPage is invalid.'
    FRIEND_LIST_SUCCESS = 'friend list success.'

    FRIEND_SET_LABEL_SUCCESS = 'friend set label success.'
    FRIEND_SET_LABEL_PARAM_INVALID = 'friend id or label is invalid.'