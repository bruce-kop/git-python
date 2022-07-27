from flask import Blueprint, request, jsonify
from userservice.utils.responseBuild import responseBuilder
from userservice.utils.VerifyCodeProduce import check_code
from userservice.utils import ImageConvert
from userservice.utils.RedisOperator import redis
from userservice.utils.res_msg_enum import ResMSG,ResCode

verifycode = Blueprint('verifycode', __name__)

@verifycode.route('/api/verifycode', methods=['POST'])
def get_verifycode():
    # generate verify code.
    print(request.data)
    try:
        imge, code = check_code()
        # save the code to redis,key is client, validity is 30s.
        client = request.remote_addr
        redis.setex("{}-code".format(client), 30, code)
        base64_imge = ImageConvert.image_to_base64(imge)
        response = responseBuilder.build_response(ResCode.VERRIFY_CODE_SUCCESS.value, ResMSG.VERRIFY_CODE_SUCCESS.value, verifycode =code,imge = base64_imge)

    except Exception as e:
        response = responseBuilder.build_response(ResCode.VERRIFY_CODE_FAILED.value, ResMSG.VERRIFY_CODE_FAILED.value)
    return jsonify(response)
