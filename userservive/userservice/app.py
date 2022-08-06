#encoding=utf8

import datetime
from gevent import pywsgi

from konfig import Config
from flask import Flask, request, g
from models.database import db
from views import blueprints
from utils.Logger import logger
from utils.requestParse import parser
from utils.global_enum import APIS
from utils.tokenProducer import Jwt,TOKEN_PRODUCE_KEY
from utils.RedisOperator import redis
from utils.parseConfig import xml_parse

def create_app():
    app = Flask(__name__)
    c = Config('.\Docs\settings.ini')
    app.config.update(c.get_map('mysql'))

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    #login_manager.init_app(app)
    db.create_all(app=app)

    return app


app = create_app()

@app.before_request
def authenticate():
    if not request.data:
        g.userid = None
        return

    i = request.url.rfind('/api')
    api = request.url[i:]
    if api in APIS:
        # APIS列表中的API不需要token验证
        g.userid = None
        return

    data = parser.parse_to_dict(request.data)
    token = data.get('token')
    g.token = token

    try:
        res = Jwt.decode(token.encode(), TOKEN_PRODUCE_KEY)
    except ValueError as e:
        logger.debug(e)
        g.userid = None
        return

    #校验token是否过期
    if float(res['exp']) < datetime.datetime.now().timestamp():
        g.userid = None
        return

    #和缓存的token校验，确认该token是否是给这个用户颁发的
    token_in_cache = redis.get(res['userid'])
    if token_in_cache != token:
        logger.debug('token is invalid.')
        g.userid = None
    else:
        logger.info(res)
        g.userid = res['userid']

    return

if __name__ == '__main__':
    logger.info("start userserver")
    addr = xml_parse.parse_service_info()
    server = pywsgi.WSGIServer(addr, app)
    server.serve_forever()
    #app.run()#开发环境运行
