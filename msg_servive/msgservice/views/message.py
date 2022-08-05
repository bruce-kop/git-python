#encoding = utf8
from flask import Blueprint, request,jsonify,g
from msgservice.utils.requestParse import parser
from msgservice.utils.responseBuild import responseBuilder
from msgservice.utils.Logger import logger
from msgservice.utils.res_msg_enum import ResMSG, ResCode
import re
from msgservice.models.database import db,Message,SenderBox,ReceiverBox
import datetime
from msgservice.views.pipeline import *
from msgservice.utils.RedisOperator import redis

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

        try:
            if type == 'user':
                friend = char_session.get('friend')
                match = {
                    'user_id': g.userid,
                    'receiver': friend
                }
                pipeline1 = make_pipeline(document='message', pageSize=pageSize, pageIndex=pageIndex, match=match)
                match = {
                    'user_id': g.userid,
                    'sender': friend
                }
                pipeline2 = make_pipeline(document='message', pageSize=pageSize, pageIndex=pageIndex, match=match)
            elif type == 'group':
                group = char_session.get('group')
                match = {
                    'user_id': g.userid,
                    'group_id': group
                }
                pipeline1 = make_pipeline(document='message', pageSize=pageSize, pageIndex=pageIndex, match=match)
                pipeline2 = make_pipeline(document='message', pageSize=pageSize, pageIndex=pageIndex, match=match)
            else:
                return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                              ResMSG.MESSAGE_FIND_PARAM_INVALID.value))

            results1 = SenderBox.objects().aggregate(pipeline1)
            results2 = ReceiverBox.objects().aggregate(pipeline2)

            totalCount1, msg_list1 = CommandCursor_to_list(results1)
            totalCount2, msg_list2 = CommandCursor_to_list(results2)


            totalCount = totalCount1 + totalCount2
            msg_list = msg_list1 + msg_list2
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = totalCount
        totalpage = int(totalCount/pageSize) + (0 if totalCount%pageSize == 0 else 1)
        pageIndex = pageIndex
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
        type = char_session.get('type')

        if not pageIndex or not pageSize or not char_session or not msg_type:
            return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                          ResMSG.MESSAGE_FIND_PARAM_INVALID.value))

        try:
            if type == 'user':
                friend = char_session.get('friend')
                match = {
                    'user_id': g.userid,
                    'receiver': friend,
                    'msg_type': msg_type
                }
                pipeline1 = make_pipeline(document='message', pageSize=pageSize, pageIndex=pageIndex, match=match)
                match = {
                    'user_id': g.userid,
                    'sender': friend,
                    'msg_type': msg_type
                }
                pipeline2 = make_pipeline2(document='receiver', pageSize=pageSize, pageIndex=pageIndex, match=match)
            elif type == 'group':
                group = char_session.get('group')
                match = {
                    'user_id': g.userid,
                    'group_id': group,
                    'msg_type': msg_type
                }
                pipeline1 = make_pipeline(document='message', pageSize=pageSize, pageIndex=pageIndex, match=match)
                pipeline2 = make_pipeline(document='receiver', pageSize=pageSize, pageIndex=pageIndex, match=match)
            else:
                return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_PARAM_INVALID.value,
                                                              ResMSG.MESSAGE_FIND_PARAM_INVALID.value))

            results1 = SenderBox.objects().aggregate(pipeline1)
            results2 = ReceiverBox.objects().aggregate(pipeline2)

            totalCount1, msg_list1 = CommandCursor_to_list(results1)
            totalCount2, msg_list2 = CommandCursor_to_list(results2)

            print(totalCount1,msg_list1)

            totalCount = totalCount1 + totalCount2
            msg_list = msg_list1 + msg_list2
        except Exception as e:
            logger.debug(e)
            return jsonify(responseBuilder.build_response(ResCode.INNER_ERR.value, ResMSG.INNER_ERR.value))

        totalCount = totalCount
        totalpage = int(totalCount / pageSize) + (0 if totalCount % pageSize == 0 else 1)
        pageIndex = pageIndex
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


@message_svr.route('/api/msg/unreaders', methods=['POST'])
def message_unreads():
    if request.data:
        data = parser.parse_to_dict(request.data)
        msg_ids = data.get("msg_ids")
        unreader_list = list()
        for m in msg_ids:
            try:
                unreader = redis.get(m+'-u')
                reader = redis.get(m + '-u')
            except Exception as e:
                logger.debug(e)
                continue

            ur_num = len(unreader)
            t_receiver = len(unreader) + len(reader)

            unreader_list.append({"msg_id": m, "ur_num": ur_num, "t_receiver": t_receiver})

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, unreaders=unreader_list))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))


@message_svr.route('/api/msg/off_msg_num', methods=['POST'])
def message_off_msg_num():
    if request.data:

        msgs = redis.get(g.userid+ '-m')
        chart_sessions = list()
        charts = {}
        msgs_tmp = list()
        for m in msgs:
            if m["group_id"] == None:
                msgs_tmp.append({"type": "user", "sender": m['sender']})
            else:
                msgs_tmp.append({"type": "group", "group_id": m['group_id']})
        msg_set = set(msgs_tmp)

        for item in msg_set:
            if item["type"] == "group":
                char_session = {"type": "group", "group_id": item["group_id"], "num": msgs_tmp.count(item)}
            else:
                char_session = {"type": "user", "sender": item["group_id"], "num": msgs_tmp.count(item)}
            chart_sessions.append(char_session)

        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, chart_sessions=chart_sessions))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))

@message_svr.route('/api/msg/off_msgs', methods=['POST'])
def message_off_msgs():
    if request.data:
        data = parser.parse_to_dict(request.data)
        char_session = data.get('char_session')

        type = char_session.get('type')
        if type == 'group':
            group_id = char_session.get('group_id')
        elif type == 'user':
            sender = char_session.get('sender')

        msgs = redis.get(g.userid + '-m')
        return_msgs = list()
        for m in msgs:
            if m['type'] == type:
                if type == 'user' and m['sender'] == sender:
                    return_msgs.append(m)
                if type == 'group' and m['group_id'] == group_id:
                    return_msgs.append(m)


        return jsonify(responseBuilder.build_response(ResCode.MESSAGE_FIND_SUCCESS.value,
                                                      ResMSG.MESSAGE_FIND_SUCCESS.value, messages=return_msgs))

    return jsonify(responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                  ResMSG.PARAMS_IS_EMPTY.value))