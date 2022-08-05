#encoding = utf8
from flask import Blueprint, request,jsonify,g
from groupservice.utils.requestParse import parser
from groupservice.utils.responseBuild import responseBuilder
from groupservice.utils.Logger import logger
from sqlalchemy import and_
from groupservice.utils.res_msg_enum import ResMSG, ResCode
import uuid
from groupservice.models.database import db, Group,GroupAddrBook,GroupAu,GroupRole,GroupRoleAu,GroupUser,User
import datetime
from sqlalchemy.orm import relationship
from groupservice.utils.data_conversion import query_res_to_dict_list, query_res_to_dict

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
            db.session.query(GroupUser).filter(and_(GroupUser.group_id == groupid, GroupUser.user_id.in_(member_list))).delete()
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
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value, ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        try:
            q = db.session.query(Group.id,Group.name,Group.avatar).filter(Group.id == GroupUser.group_id).filter(GroupUser.user_id == g.userid)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        groups = query_res_to_dict_list(q)
        count = len(groups)

        return jsonify(responseBuilder.build_response(ResCode.GROUP_LIST_SUCCESS.value,
                                                      ResMSG.GROUP_LIST_SUCCESS.value,count = count,groups = groups))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/save_to_addr', methods=['POST'])
def save_to_addr():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value, ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            groupid =data.get('groupid')
        except Exception as e:
            logger.debug(e)

        try:
            q = db.session.query(Group.id).filter(Group.id == groupid)
            logger.info(q.first())
            if q:
                grou_addr_book =GroupAddrBook()
                grou_addr_book.id = uuid.uuid4()
                grou_addr_book.group_id = groupid
                grou_addr_book.user_id = g.userid
                db.session.add(grou_addr_book)
                db.session.commit()
            else:
                return jsonify(responseBuilder.build_response(ResCode.GROUP_PARAM_IS_INVALID,
                                                              ResMSG.GROUP_PARAM_IS_INVALID.value))
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        return jsonify(responseBuilder.build_response(ResCode.GROUP_SAVE_TO_ADDR_SUCCESS.value,
                                                      ResMSG.GROUP_SAVE_TO_ADDR_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/QR_code', methods=['POST'])
def get_QR_code():
    pass

@group_svr.route('/api/group/set_member_role', methods=['POST'])
def set_member_role():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value, ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            groupid= data.get('groupid')
            members = data.get('members')
        except  Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_ROLE_SET_PARAM_INVALID.value,
                                                          ResMSG.GROUP_MEMBER_ROLE_SET_PARAM_INVALID.value))
        try:
            group_user = GroupUser()
            role_id = data.get('role_id')
            member_list = [member['memberid'] for member in members]
            logger.info(member_list)
            logger.info(role_id)
            q = db.session.query(GroupUser).filter(and_(GroupUser.group_id == groupid, GroupUser.user_id.in_(member_list))).update({"role_id":role_id})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_ROLE_SET_SUCCESS.value,
                                                      ResMSG.GROUP_MEMBER_ROLE_SET_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/member_list', methods=['POST'])
def member_list():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value, ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            groupid = data.get('groupid')
        except  Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_LIST_PARAM_INVALID.value,
                                                          ResMSG.GROUP_MEMBER_LIST_PARAM_INVALID.value))

        try:
            q = db.session.query(User.id, User.name, User.avatar).filter(User.id == GroupUser.user_id).filter(
                GroupUser.group_id == groupid)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        users = query_res_to_dict_list(q)
        count = len(users)

        return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_LIST_SUCCESS.value,
                                                      ResMSG.GROUP_MEMBER_LIST_SUCCESS.value, count=count,
                                                      users=users))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/member_info', methods=['POST'])
def member_info():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value, ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            groupid = data.get('groupid')
            memberid = data.get('memberid')
        except  Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_INFO_PARAM_INVALID.value,
                                                          ResMSG.GROUP_MEMBER_INFO_PARAM_INVALID.value))

        try:
            q = db.session.query(User.id, User.name, User.avatar).filter(User.id == GroupUser.user_id).filter(
                GroupUser.user_id == memberid)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        member = query_res_to_dict(q)

        return jsonify(responseBuilder.build_response(ResCode.GROUP_MEMBER_INFO_SUCCESS.value,
                                                      ResMSG.GROUP_MEMBER_INFO_SUCCESS.value,
                                                      member=member))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@group_svr.route('/api/group/groups_in_addr_book', methods=['POST'])
def groups_in_addr_book():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value, ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        try:
            q = db.session.query(Group.id, Group.name, Group.avatar).filter(Group.id == GroupAddrBook.group_id).filter(
                GroupAddrBook.user_id == g.userid)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        groups = query_res_to_dict_list(q)
        count = len(groups)

        return jsonify(responseBuilder.build_response(ResCode.GROUP_LIST_IN_ADDR_BOOK_SUCCESS.value,
                                                      ResMSG.GROUP_LIST_IN_ADDR_BOOK_SUCCESS.value, count=count, groups=groups))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

