#encoding = utf8
from flask import Blueprint, request,jsonify,url_for,g,redirect
from flask_login import (current_user, login_user, logout_user,login_required)
import uuid
import datetime
import re
from file_storage_service.models.database import db, User
from file_storage_service.utils.requestParse import parser
from file_storage_service.utils.responseBuild import responseBuilder
from file_storage_service.utils.verify_util import VerifyUtil
from file_storage_service.utils.RedisOperator import redis
from file_storage_service.utils.Logger import logger

from file_storage_service.utils.res_msg_enum import ResMSG,ResCode

from file_storage_service.models.database import db, User
from file_storage_service.utils.tokenProc import Jwt
from file_storage_service.utils.global_enum import GlobalEnum

user_logout = Blueprint('logout', __name__)

@user_logout.route("/api/logout", methods=['POST'])
def logout():
    if request.data:
        try:
            if g.userid:
                redis.delete(g.userid)
            response = responseBuilder.build_response(ResCode.LOGOUT_SUCCESS.value,ResMSG.LOGOUT_SUCCESS.value)
        except Exception as e:
            logger.error(e)
            response = responseBuilder.build_response(ResCode.INNER_ERR.value,ResMSG.INNER_ERR.value)
    else:
        response = responseBuilder.build_response(ResCode.PARAMS_IS_EMPTY.value,ResMSG.PARAMS_IS_EMPTY.value)
    return jsonify(response)
