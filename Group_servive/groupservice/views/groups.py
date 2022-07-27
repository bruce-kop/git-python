#encoding = utf8
from flask import Blueprint, request,jsonify,g
from ..utils.requestParse import parser
from ..utils.responseBuild import responseBuilder
from ..utils.RedisOperator import redis
from ..utils.Logger import logger
from sqlalchemy import and_
from ..utils.res_msg_enum import ResMSG, ResCode
import uuid
from ..models.database import db, Group,GroupAddrBook,GroupAu,GroupRole,GroupRoleAu,GroupUser
from ..utils.tokenProc import Jwt,TOKEN_PRODUCE_KEY
from ..utils.global_enum import GlobalEnum
from sqlalchemy import func
import datetime

group_svr = Blueprint('group_svr', __name__)

@group_svr.route('/api/group/add', methods=['POST'])
def add_group():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        new_group = Group()
        new_group.id = uuid.uuid4()
        new_group.name = 'name' in data and data['name'] or ' '
        #QR_code生成，可能是实时生成，存在缓冲中，有效期7天，数据库中不存储
        members= data.get('members')
        if len(members) == 0:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_ADD_FRIENDS_INVALID.value, ResMSG.FRIEND_ADD_FRIENDS_INVALID.value))

        new_group.created_at = datetime.datetime.now()
        group_user_list = list()
        #群主添加
        group_user = GroupUser()
        group_user.id = uuid.uuid4()
        group_user.group_id = new_group.id
        group_user.user_id = g.userid
        group_user.role_id = 1 #1是群主的角色id
        group_user_list.append(group_user)
        #添加成员
        for member in members:
            group_user = GroupUser()
            group_user.id = uuid.uuid4()
            group_user.group_id = new_group.id
            # 此处应该校验成员是否是真实用户
            group_user.user_id = 'member_id' in member and member['member_id'] or ' '
            group_user.role_id = 3
            group_user_list.append(group_user)
        try:
            db.session.add(new_group)
            db.session.commit()
            db.session.add_all(group_user_list)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_ADD_SUCCESS.value,
                                                      ResMSG.GROUP_ADD_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/del', methods=['POST'])
def del_group():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        groupid = 'groupid' in data and data['groupid'] or None
        if not groupid:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_DEL_GROUPID_INVALID.value, ResMSG.GROUP_DEL_GROUPID_INVALID.value))
        try:
            db.session.query(Group).filter(groupid == groupid).delete()
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_DEL_SUCCESS.value,
                                                      ResMSG.GROUP_DEL_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/del_member', methods=['POST'])
def del_members():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        groupid = 'groupid' in data and data['groupid'] or None

        members = data.get('members')
        if not members or len(members) == 0:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_DEL_GROUPID_INVALID.value, ResMSG.GROUP_MEMBER_DEL_GROUPID_INVALID.value))

        member_list = [member['memberid'] for member in members]
        try:
            db.session.query(GroupUser).filter(and_(groupid == groupid, GroupUser.user_id.in_(member_list))).delete()
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBERS_DEL_SUCCESS.value,
                                                      ResMSG.GROUP_MEMBERS_DEL_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/add_member', methods=['POST'])
def add_members():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        groupid = 'groupid' in data and data['groupid'] or None

        members = data.get('members')
        if not members or len(members) == 0:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_ADD_GROUPID_INVALID.value, ResMSG.GROUP_MEMBER_ADD_GROUPID_INVALID.value))

        member_list = list()
        for member in members:
            group_user = GroupUser()
            group_user.id = uuid.uuid4()
            group_user.group_id = groupid
            # 此处应该校验成员是否是真实用户
            group_user.user_id = 'memberid' in member and member['memberid'] or ' '
            group_user.role_id = 3
            member_list.append(group_user)
        try:
            db.session.add_all(member_list)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBERS_ADD_SUCCESS.value,
                                                      ResMSG.GROUP_MEMBERS_ADD_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/set_name', methods=['POST'])
def set_group_name():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        groupid = 'groupid' in data and data['groupid'] or None
        name = 'name' in data and data['name'] or None
        logger.info(data)
        logger.info(name)
        if not groupid or not name:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_SET_NAME_PARAMS_INVALID.value, ResMSG.GROUP_SET_NAME_PARAMS_INVALID.value))
        try:
            db.session.query(Group).filter(Group.id == groupid).update({'name':name})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_SET_NAME_SUCCESS.value,
                                                      ResMSG.GROUP_SET_NAME_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/set_notice', methods=['POST'])
def set_group_notice():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        groupid = 'groupid' in data and data['groupid'] or None
        notice = 'notice' in data and data['notice'] or None
        if not groupid or not notice:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_SET_NOTICE_PARAMS_INVALID.value, ResMSG.GROUP_SET_NOTICE_PARAMS_INVALID.value))
        try:
            db.session.query(Group).filter(Group.id == groupid).update({'notice':notice})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_SET_NOTICE_SUCCESS.value,
                                                      ResMSG.GROUP_SET_NOTICE_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/set_note', methods=['POST'])
def set_group_note():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        groupid = 'groupid' in data and data['groupid'] or None
        note = 'note' in data and data['note'] or None
        if not groupid or not note:
            return jsonify(responseBuilder.build_response(ResCode.GROUP_SET_NAME_PARAMS_INVALID.value, ResMSG.GROUP_SET_NAME_PARAMS_INVALID.value))
        try:
            db.session.query(Group).filter(Group.id == groupid).update({'note':note})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.GROUP_SET_NOTE_SUCCESS.value,
                                                      ResMSG.GROUP_SET_NOTE_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/get_groups', methods=['POST'])
def get_groups():
    pass

@group_svr.route('/api/group/save_to_addr', methods=['POST'])
def save_to_addr():
    pass

@group_svr.route('/api/group/QR_code', methods=['POST'])
def get_QR_code():
    pass

@group_svr.route('/api/group/set_member_role', methods=['POST'])
def set_member_role():
    pass

@group_svr.route('/api/group/member_list', methods=['POST'])
def member_list():
    pass

@group_svr.route('/api/group/member_info', methods=['POST'])
def member_list():
    pass
