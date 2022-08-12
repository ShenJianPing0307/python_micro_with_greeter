from flask import Blueprint
from proto import helloworld_pb2, helloworld_pb2_grpc
from initialize.breaker import breaker
import initialize

hello = Blueprint('hello', __name__)


@breaker # 熔断机制
@hello.route('/index')
def index():
    channel = initialize.init_srv_conn()
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    hello_response = stub.SayHello(helloworld_pb2.HelloRequest(name='iveBoy'))
    print(hello_response)
    return hello_response.message
