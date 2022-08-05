#encoding=utf8
from concurrent import futures
import grpc
from groupservice.views import groupservice_pb2_grpc
from groupservice.views import groupservice_pb2
from groupservice.models.database import GroupUser, db2
from groupservice.utils.Logger import logger
import threading
from groupservice.utils.DBHelper import MysqlDBHelper,mysql
import json

class GroupService(groupservice_pb2_grpc.GroupServiceServicer):

    def GetMembers(self, request, context):
        where = "group_id = \"{}\"".format(request.group_id)
        field = "user_id"
        q = mysql.select_all(table='group_user',field=field, where= where)
        members = [m[0] for m in q]
        members = json.dumps(members)
        return groupservice_pb2.membersReply(message=members)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    groupservice_pb2_grpc.add_GroupServiceServicer_to_server(GroupService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

class RpcServerThread(threading.Thread):
    def __init__(self, ThreadID, name, *args):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        self.name = name
    def run(self):
        serve()
