import grpc
import logging
from proto import helloworld_pb2, helloworld_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="iveBoy"))
    print("Greeter client received:", response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
