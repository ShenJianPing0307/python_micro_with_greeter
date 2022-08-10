import initialize
from proto import helloworld_pb2_grpc, helloworld_pb2


def test_retry_test():
    channel = initialize.init_srv_conn()
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    hello_response = stub.SayHello(helloworld_pb2.HelloRequest(name='iveBoy'), timeout=2)  # 通过timeout=2测试重试机制
    print(hello_response)
    return hello_response.message


if __name__ == '__main__':
    test_retry_test()
