from flask import Blueprint, request,jsonify
from file_storage_service.utils.requestParse import parser
from file_storage_service.utils.responseBuild import responseBuilder
from file_storage_service.utils.RedisOperator import redis
from file_storage_service.utils.Logger import logger
from sqlalchemy import or_
from file_storage_service.utils.res_msg_enum import ResMSG, ResCode

from file_storage_service.models.database import db, User
from file_storage_service.utils.tokenProc import Jwt,TOKEN_PRODUCE_KEY
from file_storage_service.utils.global_enum import GlobalEnum
auth = Blueprint('login', __name__)


def login_err_count_verify(CUI):
    '''Number of logins exceeded, then return False else return True.
    :param CUI, Unique identifier of the client
    '''
    login_err_count = redis.get('{}-login_err_count'.format(CUI))
    print(type(login_err_count))
    if not login_err_count:
        login_err_count = 1
        redis.setex('{}-login_err_count'.format(CUI), 30, login_err_count)
    else:
        login_err_count = int(login_err_count)
        if login_err_count > int(GlobalEnum.LOGIN_ERR_COUNT_LIMIT.value):
            return False

        redis.setex('{}-login_err_count'.format(CUI), 30, login_err_count + 1)
    return True

@auth.route('/api/login', methods=['POST'])
def login():
    if request.data:
        try:
            data = parser.parse_to_dict(request.data)
            q = db.session.query(User).filter(or_(User.name == data.get('username'), User.phone == data.get('phone')))
            user = q.first()
            CUI = request.remote_addr
            if user is not None and user.authenticate(data.get('pwd')):
                userid = user.id
                token = Jwt.encode({"userid": userid}, TOKEN_PRODUCE_KEY, 3600 * 24 * 7)#token 返回的是bytes类型，要转成string类型
                redis.setex(userid,3600 * 24 * 7,token)

                response = responseBuilder.build_response(ResCode.LONIN_SUCCESS.value,ResMSG.LONIN_SUCCESS.value,
                                                          token = token.decode(),
                                                          userid = userid,
                                                          username = user.name,
                                                          phone = user.phone,
                                                          avatar = user.avatar)
                redis.delete('{}-login_err_count'.format(userid))
                return jsonify(response)
            else:
                response = responseBuilder.build_response(ResCode.LOGIN_USER_OR_PWD_ERR.value,ResMSG.LOGIN_USER_OR_PWD_ERR.value)

        except Exception as e:
            logger.error(e)
            response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
    else:
        response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY,ResMSG.PARAMS_IS_EMPTY.value)
    if not login_err_count_verify(CUI):
        response = responseBuilder.build_response(ResCode.LOGIN_EXCEEDS,ResMSG.LOGIN_EXCEEDS.value)
    return jsonify(response)

