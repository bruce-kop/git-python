#encoding=utf8
from __future__ import print_function

import logging, sys
import grpc
from groupservice.views import groupservice_pb2_grpc
from groupservice.views import groupservice_pb2

def run():

	with grpc.insecure_channel('localhost:50051') as channel:
		stub = groupservice_pb2_grpc.GroupServiceStub(channel)
		response = stub.GetMembers(groupservice_pb2.membersRequest(group_id="42177ae4-81bf-4bc8-8fc5-74a025cd154f"))
		print(response)

if __name__ == '__main__':
	run()
