#encoding = utf8
from flask import Blueprint, request,jsonify,g
from friendservice.utils.requestParse import parser
from friendservice.utils.responseBuild import responseBuilder
from friendservice.utils.RedisOperator import redis
from friendservice.utils.Logger import logger
from sqlalchemy import or_
from friendservice.utils.res_msg_enum import ResMSG, ResCode
import uuid
from friendservice.models.database import db, Friend,User
from friendservice.utils.tokenProc import Jwt,TOKEN_PRODUCE_KEY
from friendservice.utils.global_enum import GlobalEnum
from sqlalchemy import func
import datetime

friend_svr = Blueprint('friend_svr', __name__)

@friend_svr.route('/api/friend/add', methods=['POST'])
def add_friend():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        new_friend = Friend()
        new_friend.id = uuid.uuid4()
        new_friend.user_id = g.userid

        if 'friend_id' not in data:
            return jsonify(responseBuilder.build_response(ResCode.FRIEND_ADD_FRIENDID_INVALID.value, ResMSG.FRIEND_ADD_FRIENDID_INVALID.value))
        new_friend.friend_id = data['friend_id']
        new_friend.friend_label = 'friend_label' in data and data['friend_label'] or ''
        new_friend.friend_au = 'friend_au' in data and data['friend_au'] or '0'
        new_friend.note = new_friend.friend_au = 'friend_au' in data and data['friend_au'] or ''
        new_friend.created_at = datetime.datetime.now()

        try:
            db.session.add(new_friend)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.FRIEND_ADD_SUCCESS.value,
                                                      ResMSG.FRIEND_ADD_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@friend_svr.route('/api/friend/del', methods=['POST'])
def del_friend():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        friend_id = 'friend_id' in data and data['friend_id'] or None
        logger.info(friend_id)
        if not friend_id:
            return jsonify(responseBuilder.build_response(ResCode.FRIEND_DEL_FRIENDID_INVALID.value, ResMSG.FRIEND_DEL_FRIENDID_INVALID.value))
        try:
            db.session.query(Friend).filter(friend_id == friend_id).delete()
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))
        return jsonify(responseBuilder.build_response(ResCode.FRIEND_DEL_SUCCESS.value,
                                                      ResMSG.FRIEND_DEL_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))
def query_res_to_dict(query_res):
    friends = list()
    descripsions = query_res.column_descriptions
    for u in query_res:
        f = {}
        for key in descripsions:
            f.update({key['name']:getattr(u,key['name'])})
        friends.append(f)
    return friends

@friend_svr.route('/api/friend/list', methods=['POST'])
def list_friend():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        user_id = g.userid
        pageSize = 'pageSize' in data and data['pageSize'] or 0
        #currentPage = 'currentPage' in data and data['currentPage'] or 1
        currentPage=data.get('currentPage')
        logger.info(currentPage)
        totalCount = 0
        friends = None
        if pageSize <= 0 or currentPage < 1:
            return jsonify(responseBuilder.build_response(ResCode.FRIEND_LIST_PARAM_INVALID.value,
                                                          ResMSG.FRIEND_LIST_PARAM_INVALID.value))
        try:
            q = db.session.query(Friend.friend_id).filter(user_id == user_id).order_by(Friend.created_at).limit(pageSize).offset((currentPage - 1) * pageSize)
            db.session.commit()
            totalCount = db.session.query(func.count(Friend.friend_id)).filter(user_id == user_id).scalar()
            db.session.commit()

            friend_list = [u[0] for u in q]
            logger.info(friend_list)
            q_friends_info = db.session.query(User.id,User.name,User.avatar).filter(User.id.in_(friend_list))
            friends = query_res_to_dict(q_friends_info)

        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        currentPage = currentPage
        pageSize = pageSize
        pageCount = (int(totalCount/pageSize) if totalCount%pageSize == 0 else
                 int(totalCount / pageSize)+1 if totalCount%pageSize >0 else 0)
        response = responseBuilder.build_response(ResCode.FRIEND_LIST_SUCCESS.value,ResMSG.FRIEND_LIST_SUCCESS.value,
                                                  currentPage = currentPage, pageSize = pageSize,pageCount = pageCount,
                                                  totalCount = totalCount, friends = friends)
        logger.info(response)
        return jsonify(response)
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))


@friend_svr.route('/api/friend/set_permission', methods=['POST'])
def set_permission_friend():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)

        friend_id = 'friend_id' in data and data['friend_id'] or None
        friend_au = 'friend_au' in data and data['friend_au'] or None
        if not friend_id or not friend_au:
            return jsonify(responseBuilder.build_response(ResCode.FRIEND_SET_PARAM_INVALID.value,
                                                          ResMSG.FRIEND_SET_PARAM_INVALID.value))
        try:
            updated_at = datetime.datetime.now()
            q = db.session.query(Friend).filter(friend_id==friend_id).update({"friend_au":friend_au, "updated_at":updated_at})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        return jsonify(responseBuilder.build_response(ResCode.FRIEND_SET_SUCCESS.value,
                                                      ResMSG.FRIEND_SET_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))


@friend_svr.route('/api/friend/set_note', methods=['POST'])
def set_note_friend():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        logger.info(data)
        friend_id = 'friend_id' in data and data['friend_id'] or None
        note = 'note' in data and data['note'] or None
        if not friend_id or not note:
            return jsonify(responseBuilder.build_response(ResCode.FRIEND_SET_NOTE_PARAM_INVALID.value,
                                                          ResMSG.FRIEND_SET_NOTE_PARAM_INVALID.value))
        try:
            updated_at = datetime.datetime.now()
            q = db.session.query(Friend).filter(friend_id==friend_id).update({"note": note, "updated_at":updated_at})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        return jsonify(responseBuilder.build_response(ResCode.FRIEND_SET_NOTE_SUCCESS.value,
                                                      ResMSG.FRIEND_SET_NOTE_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@friend_svr.route('/api/friend/set_label', methods=['POST'])
def set_label_friend():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
    if request.data:
        data = parser.parse_to_dict(request.data)
        logger.info(data)
        friend_id = 'friend_id' in data and data['friend_id'] or None
        label = 'friend_label' in data and data['friend_label'] or None
        if not friend_id or not label:
            return jsonify(responseBuilder.build_response(ResCode.FRIEND_SET_LABEL_PARAM_INVALID.value,
                                                          ResMSG.FRIEND_SET_LABEL_PARAM_INVALID.value))
        try:
            updated_at = datetime.datetime.now()
            q = db.session.query(Friend).filter(friend_id==friend_id).update({"friend_label": label, "updated_at":updated_at})
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                          ResMSG.INNER_ERR.value))

        return jsonify(responseBuilder.build_response(ResCode.FRIEND_SET_LABEL_SUCCESS.value,
                                                      ResMSG.FRIEND_SET_LABEL_SUCCESS.value))
    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))