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

    GROUP_ADD_SUCCESS = 1700
    GROUP_ADD_FRIENDS_INVALID = 1701
    GROUP_DEL_SUCCESS = 1800
    GROUP_DEL_GROUPID_INVALID =1801
    GROUP_MEMBERS_DEL_SUCCESS = 1900
    GROUP_MEMBER_DEL_GROUPID_INVALID = 1901
    GROUP_MEMBERS_ADD_SUCCESS = 2000
    GROUP_MEMBER_ADD_GROUPID_INVALID = 2001

    GROUP_SET_NAME_PARAMS_INVALID = 2101
    GROUP_SET_NAME_SUCCESS = 2100

    GROUP_SET_NOTICE_PARAMS_INVALID = 2201
    GROUP_SET_NOTICE_SUCCESS = 2200
    GROUP_SET_NOTE_PARAMS_INVALID = 2301
    GROUP_SET_NOTE_SUCCESS = 2300
    GROUP_LIST_SUCCESS = 2400
    GROUP_SAVE_TO_ADDR_SUCCESS = 2500
    GROUP_PARAM_IS_INVALID = 2501
    GROUP_MEMBER_ROLE_SET_PARAM_INVALID = 2601
    GROUP_MEMBER_ROLE_SET_SUCCESS = 2600

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

    GROUP_ADD_SUCCESS = 'group add success.'
    GROUP_ADD_FRIENDS_INVALID = 'group add  friends field is invalid.'
    GROUP_DEL_SUCCESS = 'group del success.'
    GROUP_DEL_GROUPID_INVALID = 'group del  groupid field is invalid.'
    GROUP_MEMBERS_DEL_SUCCESS = 'group member del success.'
    GROUP_MEMBER_DEL_GROUPID_INVALID = 'group member  del members field is invalid.'
    GROUP_MEMBERS_ADD_SUCCESS = 'group member add success.'
    GROUP_MEMBER_ADD_GROUPID_INVALID = 'group member  add members field is invalid.'

    GROUP_SET_NAME_PARAMS_INVALID = 'group set name param is invalid.'
    GROUP_SET_NAME_SUCCESS = 'group name set success.'
    GROUP_SET_NOTICE_PARAMS_INVALID = 'group set notice param is invalid.'
    GROUP_SET_NOTICE_SUCCESS = 'group notice set success.'
    GROUP_SET_NOTE_PARAMS_INVALID = 'group set note field is invalid.'
    GROUP_SET_NOTE_SUCCESS = 'group note set success.'
    GROUP_LIST_SUCCESS = 'get group list success.'
    GROUP_SAVE_TO_ADDR_SUCCESS = 'save the group to group addr book success'
    GROUP_PARAM_IS_INVALID ="param is invalid."
    GROUP_MEMBER_ROLE_SET_PARAM_INVALID = "member role set param is invalid."
    GROUP_MEMBER_ROLE_SET_SUCCESS = "member role set success."
