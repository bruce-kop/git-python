#encoding = utf8
from flask import Blueprint, request,jsonify,g
from msgservice.utils.requestParse import parser
from msgservice.utils.responseBuild import responseBuilder
from msgservice.utils.Logger import logger
from sqlalchemy import and_
from msgservice.utils.res_msg_enum import ResMSG, ResCode
import uuid
from msgservice.models.database import db,Message
import datetime
from sqlalchemy.orm import relationship
from msgservice.utils.data_conversion import query_res_to_dict_list, query_res_to_dict


message_svr = Blueprint('message_svr', __name__)

@message_svr.route('/api/msg/find', methods=['POST'])
def find():
    if request.data:
        msgs = Message.objects.get_or_404()
        #logger.info(msgs)

        return {"message":msgs}
