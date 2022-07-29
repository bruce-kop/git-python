#encoding = utf8
from flask import Blueprint, request,jsonify,g
from msgservice.utils.requestParse import parser
from msgservice.utils.responseBuild import responseBuilder
from msgservice.utils.Logger import logger
from sqlalchemy import and_, or_
from msgservice.utils.res_msg_enum import ResMSG, ResCode
import uuid,re
from msgservice.models.database import db,Message
import datetime
from sqlalchemy.orm import relationship
from msgservice.utils.data_conversion import query_res_to_dict_list, query_res_to_dict
from flask_mongoengine import MongoEngine


message_svr = Blueprint('message_svr', __name__)

@message_svr.route('/api/msg/find', methods=['POST'])
def find():
    if request.data:
        data = parser.parse_to_dict(request.data)
        pageSize = data.get("pageSize")
        pageIndex = data.get("pageIndex")
        char_session = data.get('char_session')
        if not pageIndex or not pageSize or not char_session:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        type = char_session.get('type')
        msg_from = char_session.get('msg_from')
        if not type or not msg_from:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        try:
            filter = {"group_id": msg_from} if type == 'group' else {"$or": [{"$and": [{"user_id": g.userid}, {"from_u": msg_from}]},
                     {"$and": [{"user_id": msg_from}, {"from_u": g.userid}]}]}

            msgs = Message.objects(__raw__=filter).order_by('created_at').paginate(page=pageIndex, per_page=pageSize)
            msg_list = [m for m in msgs.items]
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = msgs.total
        totalpage = msgs.pages
        pageIndex = msgs.page
        pageSize = pageSize

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, messages=msg_list,
                                                      totalCount=totalCount, totalpage=totalpage,
                                                      pageIndex=pageIndex, pageSize=pageSize))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                      ResMSG.PARAMS_IS_EMPTY.value))

@message_svr.route('/api/msg/find_by', methods=['POST'])
def find_by():
    if request.data:
        data = parser.parse_to_dict(request.data)
        pageSize = data.get("pageSize")
        pageIndex = data.get("pageIndex")
        msg_type = data.get("msg_type")
        char_session = data.get('char_session')
        if not pageIndex or not pageSize or not char_session or not msg_type:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        type = char_session.get('type')
        msg_from = char_session.get('msg_from')
        if not type or not msg_from:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        try:
            filter = {"$and":[{"group_id": msg_from},{"msg_type":msg_type}]} if type == 'group' else {"$or": [{"$and": [{"user_id": g.userid}, {"from_u": msg_from},{"msg_type": msg_type}]},
                     {"$and": [{"user_id": msg_from}, {"from_u": g.userid},{"msg_type": msg_type}]}]}

            msgs = Message.objects(__raw__=filter).order_by('created_at').paginate(page=pageIndex, per_page=pageSize)
            msg_list = [m for m in msgs.items]
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = msgs.total
        totalpage = msgs.pages
        pageIndex = msgs.page
        pageSize = pageSize

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, messages=msg_list,
                                                      totalCount=totalCount, totalpage=totalpage,
                                                      pageIndex=pageIndex, pageSize=pageSize))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                      ResMSG.PARAMS_IS_EMPTY.value))

@message_svr.route('/api/msg/find_by_kw', methods=['POST'])
def find_by_kw():
    if request.data:
        data = parser.parse_to_dict(request.data)
        pageSize = data.get("pageSize")
        pageIndex = data.get("pageIndex")
        key_word = data.get("key_word")
        char_session = data.get('char_session')
        if not pageIndex or not pageSize or not char_session or not key_word:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        type = char_session.get('type')
        msg_from = char_session.get('msg_from')
        if not type or not msg_from:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        try:
            filter = {"$and":[{"group_id": msg_from},{"content":{"$regex":key_word}}]} if type == 'group' else {"$or": [{"$and": [{"user_id": g.userid}, {"from_u": msg_from},{"content":{"$regex":key_word}}]},
                     {"$and": [{"user_id": msg_from}, {"from_u": g.userid},{"content":{"$regex":key_word}}]}]}

            filter = {"content":{"$in":[re.compile(key_word)]}}
            #filter = {"content":{"$regex":key_word}}

            msgs = Message.objects(__raw__=filter).order_by('created_at').paginate(page=pageIndex, per_page=pageSize)
            msg_list = [m for m in msgs.items]
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = msgs.total
        totalpage = msgs.pages
        pageIndex = msgs.page
        pageSize = pageSize

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, messages=msg_list,
                                                      totalCount=totalCount, totalpage=totalpage,
                                                      pageIndex=pageIndex, pageSize=pageSize))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                      ResMSG.PARAMS_IS_EMPTY.value))

@message_svr.route('/api/msg/find_by_date', methods=['POST'])
def find_by_data():
    if request.data:
        data = parser.parse_to_dict(request.data)

        pageSize = data.get("pageSize")
        pageIndex = data.get("pageIndex")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        char_session = data.get('char_session')

        if not pageIndex or not pageSize or not end_date or not start_date or not char_session:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        type = char_session.get('type')
        msg_from = char_session.get('msg_from')
        if not type or not msg_from:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))

        try:
            s = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            e = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

            filter = {"$and":[{"group_id": msg_from}, {"created_at": {"$lt": e, "$gt": s}}]} if type == 'group' else {"$and":[{"created_at": {"$lt": e, "$gt": s}},{
                "$or": [{"$and": [{"user_id": g.userid}, {"from_u": msg_from}]},
                        {"$and": [{"user_id": msg_from}, {"from_u": g.userid}]}]}]}

            msgs = Message.objects(__raw__=filter).order_by('created_at').paginate(page=pageIndex, per_page=pageSize)
            msg_list = [m for m in msgs.items]
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = msgs.total
        totalpage = msgs.pages
        pageIndex = msgs.page
        pageSize = pageSize

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, messages=msg_list,
                                                      totalCount=totalCount, totalpage=totalpage,
                                                      pageIndex=pageIndex, pageSize=pageSize))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@message_svr.route('/api/msg/find_by_member', methods=['POST'])
def find_by_member():
    if request.data:
        data = parser.parse_to_dict(request.data)
        pageSize = data.get("pageSize")
        pageIndex = data.get("pageIndex")
        groupid = data.get("groupid")
        memberid = data.get("memberid")
        logger.info(data)

        if not pageIndex or not pageSize or not groupid or not memberid:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        try:
            msgs = Message.objects(__raw__={"$and": [{"user_id": groupid}, {"from_u": memberid}, {"group_id":groupid}]}).order_by(
                'created_at').paginate(page=pageIndex, per_page=pageSize)
            msg_list = [m for m in msgs.items]
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = msgs.total
        totalpage = msgs.pages
        pageIndex = msgs.page
        pageSize = pageSize

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, messages=msg_list,
                                                      totalCount=totalCount, totalpage=totalpage,
                                                      pageIndex=pageIndex, pageSize=pageSize))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@message_svr.route('/api/msg/del', methods=['POST'])
def message_del():
    if request.data:
        data = parser.parse_to_dict(request.data)
        char_session = data.get('char_session')
        pass
    return


@message_svr.route('/api/msg/find_chats', methods=['POST'])
def find_chats():
    if request.data:
        data = parser.parse_to_dict(request.data)

        pageSize = data.get("pageSize")
        pageIndex = data.get("pageIndex")

        if not pageIndex or not pageSize:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))
        try:

            #chats = Message.objects().only('from_u', "user_id")
            pipeline = [{'$group' : {'_id' : "$from_u", 'groupid':{'$last' : '$group_id'},'created_at':{'$last' : "$created_at"} ,'last_msg' : {'$last' : "$content"}}}]
            chats = Message.objects().aggregate(pipeline)
            chat_list = [c for c in chats]

        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, chat_session=chat_list))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))


@message_svr.route('/api/msg/read', methods=['POST'])
def message_read():
    pass
