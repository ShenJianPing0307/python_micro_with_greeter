from proto import helloworld_pb2_grpc
from proto import helloworld_pb2
import time
import random
from settings import settings


def second_tracing_business():
    time.sleep(random.randint(1, 5) * 0.1)


# 被调用的函数还可以继续追加链路追踪
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # web层调用srv层的SayHello，然后再调用这个span，通过context找到父span
        with settings.JAEGER_TRACER.start_span('second_business',
                                               child_of=context.get_active_span()) as second_business_span:
            second_tracing_business()
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)


"""
形成如下链路：
greeter_web /Greeter/SayHello
    greeter_srv /Greeter/SayHello
        greeter_srv second_business
"""
