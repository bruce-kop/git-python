#encoding = utf8
from flask import Blueprint, request,jsonify,url_for,g,redirect
from flask_login import (current_user, login_user, logout_user,login_required)
import uuid
import datetime
import re
from groupservice.models.database import db, User
from groupservice.utils.requestParse import parser
from groupservice.utils.responseBuild import responseBuilder
from groupservice.utils.verify_util import VerifyUtil
from groupservice.utils.RedisOperator import redis
from groupservice.utils.Logger import logger

from groupservice.utils.res_msg_enum import ResMSG,ResCode

from groupservice.models.database import db, User
from groupservice.utils.tokenProc import Jwt
from groupservice.utils.global_enum import GlobalEnum

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
