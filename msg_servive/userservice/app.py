import os
from flask import Flask, Blueprint,request,g
from gevent import pywsgi
from userservice.models.database import db, User
from userservice.views import blueprints
from userservice.utils.Logger import logger
from userservice.utils.requestParse import parser
from userservice.utils.global_enum import APIS
from userservice.utils.tokenProc import Jwt,TOKEN_PRODUCE_KEY
import datetime
from konfig import Config

#from flask_cache import Cache

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
    if request.data:
        i = request.url.rfind('/api')
        api =request.url[i:]
        logger.info(api)
        if api not in APIS:
            data = parser.parse_to_dict(request.data)
            token = data.get('token')
            g.token = token
            logger.debug(token)

            res = Jwt.decode(token.encode(), TOKEN_PRODUCE_KEY)
            if float(res['exp']) < datetime.datetime.now().timestamp():
                logger.info(datetime.datetime.now().timestamp())
                g.userid = None
            else:
                logger.info(res)
                g.userid = res['userid']
        else:
            logger.info("reuquest api:{}".format(api))
            g.userid = None
    else:
        g.userid = None

if __name__ == '__main__':

    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()
    #app.run()#开发环境运行
