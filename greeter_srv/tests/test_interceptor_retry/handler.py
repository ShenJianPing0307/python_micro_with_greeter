import time

from proto import helloworld_pb2_grpc
from proto import helloworld_pb2


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # 设定超时时间,测定客户端超时机制
        time.sleep(5)
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)
