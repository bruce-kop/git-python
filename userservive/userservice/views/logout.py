#encoding = utf8
from flask import Blueprint, request,jsonify,url_for,g,redirect
from flask_login import (current_user, login_user, logout_user,login_required)
import uuid
import datetime
import re
from userservice.models.database import db, User
from userservice.utils.requestParse import parser
from userservice.utils.responseBuild import responseBuilder
from userservice.utils.verify_util import VerifyUtil
from userservice.utils.RedisOperator import redis
from userservice.utils.Logger import logger

from userservice.utils.res_msg_enum import ResMSG,ResCode

from userservice.models.database import db, User
from userservice.utils.tokenProc import Jwt
from userservice.utils.global_enum import GlobalEnum

user_logout = Blueprint('logout', __name__)

@user_logout.route("/api/logout", methods=['POST'])
def logout():
    if not g.userid:
        return jsonify(responseBuilder.build_response(ResCode.TOKEN_INVALID.value,ResMSG.TOKEN_INVALID.value))
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
