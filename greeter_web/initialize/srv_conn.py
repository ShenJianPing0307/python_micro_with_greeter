import config
import grpc
from utils.consul import Consul
from loguru import logger
from utils.grpc_interceptor.retry import RetryInterceptor


def init_srv_conn():
    # 从consul负载均衡获取可用的ip和port服务
    host, port = Consul(config.CONSUL_HOST, config.CONSUL_PORT).get_host_port(f'{config.CONSUL_FILTER_KEY}=={config.CONSUL_FILTER_VALUE}')
    print(host, port)
    if not host or not port:
        logger.info(f"{config.CONSUL_FILTER_VALUE}服务无可用的实例")
        return

    greeter_channel = grpc.insecure_channel(
        f"{host}:{port}"
    )
    if not greeter_channel:
        logger.info(f"连接{config.CONSUL_FILTER_VALUE}服务失败")
        return
    # 超时机制，使用拦截器进行包装channel,RetryInterceptor中retry_timeout_ms可以设置重试时间
    retry_codes = [grpc.StatusCode.UNKNOWN, grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED]
    retry_interceptor = RetryInterceptor(retry_codes=retry_codes)
    interceptor_channel = grpc.intercept_channel(greeter_channel, retry_interceptor)
    return interceptor_channel
