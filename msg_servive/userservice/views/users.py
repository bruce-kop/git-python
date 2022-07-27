from flask import Blueprint, request,jsonify,g
from sqlalchemy import or_,and_
import uuid
import datetime
from userservice.models.database import db, User
from userservice.utils.requestParse import parser
from userservice.utils.responseBuild import responseBuilder
from userservice.utils.verify_util import VerifyUtil
from userservice.utils.RedisOperator import redis
from userservice.utils.Logger import logger
from userservice.utils.res_msg_enum import ResMSG, ResCode
import traceback
from sqlalchemy.exc import IntegrityError

users = Blueprint('users', __name__)

@users.route('/api/register', methods=['POST'])
def user_register():
    response = None
    try:
        if request.data:
            user_data = parser.parse_to_dict(request.data)

            if not VerifyUtil.verify_pwd(user_data['pwd']):
                response = responseBuilder.build_response(ResCode.REGISTER_PWD_INVALID.value, ResMSG.REGISTER_PWD_INVALID.value)

            new_user = User()
            new_user.id = uuid.uuid4()
            new_user.name = user_data['username']
            new_user.phone = user_data['phone']
            new_user.set_password(user_data['pwd'])
            verifycode = user_data['verifycode']
            new_user.created_at = datetime.datetime.now()

            if not VerifyUtil.verify_phone(new_user.phone):
                response = responseBuilder.build_response(ResCode.REGISTER_PHONE_FORMAT_INVALID.value,
                                                          ResMSG.REGISTER_PHONE_FORMAT_INVALID.value)


            client = request.remote_addr
            code = redis.get('{}-code'.format(client))
            if verifycode != code:
                response = responseBuilder.build_response(ResCode.REGISTER_VERRIFY_CODE_ERROR.value,
                                                          ResMSG.REGISTER_VERRIFY_CODE_ERROR.value)


            db.session.add(new_user)
            db.session.commit()
            response = responseBuilder.build_response(ResCode.REGISTER_SUCCESS.value,
                                                          ResMSG.REGISTER_SUCCESS.value)
        else:
            response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,
                                                      ResMSG.PARAMS_IS_EMPTY.value)
    except IntegrityError:
        logger.error(traceback.print_exc())
        response = responseBuilder.build_response(ResCode.REGISTER_USER_EXISTS.value, ResMSG.REGISTER_USER_EXISTS.value)
    except Exception as e:
        logger.error(traceback.print_exc())
        response = responseBuilder.build_response(ResCode.INNER_ERR.value,
                                                  ResMSG.INNER_ERR.value)
    return jsonify(response)

@users.route('/api/unsubscribe', methods=['POST'])
def user_unsubscribe():
    '''后续改进，除了删除用户表的记录，还要删除关联表的数据。'''
    if request.data:
        if g.userid:
            try:
                logger.info(g.userid)
                redis.delete(g.userid)
                res = db.session.query(User).filter(User.id == g.userid).delete()
                db.session.commit()
                if res == 1:
                    response = responseBuilder.build_response(ResCode.UNSUBSCRIBE_SUCCESS.value,ResMSG.UNSUBSCRIBE_SUCCESS.value)
                else:
                    response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
            except IntegrityError:
                logger.error(traceback.print_exc())
                response = responseBuilder.build_response(ResCode.UNSUBSCRIBE_DELETE_FAILED.value, ResMSG.UNSUBSCRIBE_DELETE_FAILED.value)
            except Exception as e:
                logger.error(traceback.print_exc())
                response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
        else:
            response = responseBuilder.build_response(ResCode.UNSUBSCRIBE_FAILED.value,ResMSG.UNSUBSCRIBE_FAILED.value)
    else:
        response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,ResMSG.PARAMS_IS_EMPTY.value)
    return jsonify(response)

@users.route('/api/pwd/modify', methods=['POST'])
def user_pwd_modify():
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            logger.info(g.userid)
            old_pwd = data.get('old_pwd')
            new_pwd = data.get('new_pwd')
            q = db.session.query(User).filter(User.id == g.userid)
            db.session.commit()
            user = q.first()
            if user is not None and user.authenticate(old_pwd):
                user.set_password(new_pwd)
                updated_at = datetime.datetime.now()
                q.update({"pwd":user.pwd, "updated_at":updated_at})
                db.session.commit()
                response = responseBuilder.build_response(ResCode.PWD_MODIFY_SUCCESS.value,ResMSG.PWD_MODIFY_SUCCESS.value)
            else:
                response = responseBuilder.build_response(ResCode.PWD_MODIFY_FAILED.value,ResMSG.PWD_MODIFY_FAILED.value)
        except Exception as e:
                logger.error(traceback.print_exc())
                response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
    else:
        response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,ResMSG.PARAMS_IS_EMPTY.value)
    return jsonify(response)

@users.route('/api/phone/modify', methods=['POST'])
def user_phone_modify():
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            logger.info(g.userid)
            old_phone = data.get('old_phone')
            new_phone = data.get('new_phone')
            q = db.session.query(User).filter(User.id == g.userid)
            db.session.commit()
            user = q.first()
            if user is not None and user.phone == old_phone:
                updated_at = datetime.datetime.now()
                q.update({"phone":new_phone, "updated_at":updated_at})
                db.session.commit()
                response = responseBuilder.build_response(ResCode.PHONE_MODIFY_SUCCESS.value,ResMSG.PHONE_MODIFY_SUCCESS.value)
            else:
                response = responseBuilder.build_response(ResCode.PHONE_MODIFY_FAILED.value,ResMSG.PHONE_MODIFY_FAILED.value)
        except Exception as e:
                logger.error(traceback.print_exc())
                response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
    else:
        response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,ResMSG.PARAMS_IS_EMPTY.value)
    return jsonify(response)

@users.route('/api/user/precise_query', methods=['POST'])
def user_precise_query():
    if request.data:
        data = parser.parse_to_dict(request.data)
        try:
            logger.info(g.userid)
            username = data.get('username')
            phone = data.get('phone')
            q = db.session.query(User).filter(or_(User.name == username, User.phone == phone))
            db.session.commit()
            userinfo = q.first()
            if userinfo:
                if username == None:
                    response = responseBuilder.build_response(ResCode.PRECISE_QUERY_SUCCESS.value,ResMSG.PRECISE_QUERY_SUCCESS.value, user_id = userinfo.id, username = '', phone = userinfo.phone )
                else:
                    response = responseBuilder.build_response(ResCode.PRECISE_QUERY_SUCCESS.value, ResMSG.PRECISE_QUERY_SUCCESS.value,
                                                                       user_id=userinfo.id, username=userinfo.name,
                                                                       phone='')
            else:
                response = responseBuilder.build_response(ResCode.PRECISE_QUERY_FAIlED.value, ResMSG.PRECISE_QUERY_FAIlED.value)
        except Exception as e:
                logger.error(traceback.print_exc())
                response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
    else:
        response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,ResMSG.PARAMS_IS_EMPTY.value)
    return jsonify(response)


