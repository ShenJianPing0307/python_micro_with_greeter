from concurrent import futures
from proto import helloworld_pb2_grpc
from handler.helloworld import Greeter
from common.register.consul import consul
from settings import settings

from common.grpc_health.v1 import health_pb2, health_pb2_grpc, health

import grpc
from loguru import logger
from functools import partial

import sys
import signal

def on_exit(signo, frame, service_id):
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    logger.info(f"注销 {service_id} 服务")
    register.deregister(service_id=service_id)
    logger.info("注销成功")
    sys.exit(0)

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册helloword服务
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # 注册健康检查
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)

    server.add_insecure_port(f'{settings.ADDRESS_IP}:{settings.ADDRESS_PORT}')

    server.start()



    logger.info(f"服务注册开始")

    import uuid
    service_id = str(uuid.uuid1())

    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)

    if not register.register(name=settings.SERVICE_NAME, id=service_id,
                             address=settings.ADDRESS_IP, port=settings.ADDRESS_PORT, tags=settings.SERVICE_TAGS, check=None):
        logger.info(f"服务注册失败")
        sys.exit(0)

    logger.info(f"服务注册成功")

    # 主进程退出信号监听
    """
        windows下支持的信号是有限的：
            SIGINT ctrl+C终端
            SIGTERM kill发出的软件终止
    """
    signal.signal(signal.SIGINT, partial(on_exit, service_id=service_id))
    signal.signal(signal.SIGTERM, partial(on_exit, service_id=service_id))

    server.wait_for_termination()


if __name__ == '__main__':
    server()
