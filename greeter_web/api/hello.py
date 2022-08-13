from flask import Blueprint
from proto import helloworld_pb2, helloworld_pb2_grpc
from initialize.breaker import breaker
from initialize.ratelimit import limits
from config import config
import initialize

hello = Blueprint('hello', __name__)


@hello.route('/index')
@breaker  # 熔断机制
@limits(calls=config.CALLS, period=config.FIFTEEN_MINUTES)  # 限流,900s内调用5次,一旦超过会抛出 ratelimit.RateLimitException 异常
def index(*args, **kwargs):
    if "is_exception" in kwargs:  # 进行限流
        return "请求过于频繁，请稍后重试！"
    channel = initialize.init_srv_conn()
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    hello_response = stub.SayHello(helloworld_pb2.HelloRequest(name='iveBoy'))
    print(hello_response)
    return hello_response.message
