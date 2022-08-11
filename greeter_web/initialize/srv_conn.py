import config
import grpc
from utils.consul import Consul
from loguru import logger
from utils.grpc_interceptor.retry import RetryInterceptor
from jaeger_client import Config
from utils.grpc_opentracing import open_tracing_client_interceptor
from utils.grpc_opentracing.grpcext import intercept_channel


def get_retry_interceptor():
    # 超时机制，使用拦截器进行包装channel,RetryInterceptor中retry_timeout_ms可以设置重试时间
    retry_codes = [grpc.StatusCode.UNKNOWN, grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED]
    retry_interceptor = RetryInterceptor(retry_codes=retry_codes)
    return retry_interceptor


def get_tracing_interceptor():
    jaeger_config = Config(
        config={
            'sampler': {
                'type': config.JAEGER_CONFIG_SAMPLER_TYPE,
                'param': config.JAEGER_CONFIG_SAMPLER_PARAM,
            },
            'local_agent': {
                'reporting_host': config.JAEGER_CONFIG_LOCAL_AGENT_REPORTING_HOST,
                'reporting_port': config.JAEGER_CONFIG_LOCAL_AGENT_REPORTING_PORT,
            },
            'logging': config.JAEGER_CONFIG_LOGGING,
        },
        service_name=config.JAEGER_SERVICE_NAME,
        validate=config.JAEGER_VALIDATE,
    )
    tracer = jaeger_config.initialize_tracer()
    tracing_interceptor = open_tracing_client_interceptor(tracer)
    return tracing_interceptor


def init_srv_conn():
    # 从consul负载均衡获取可用的ip和port服务
    host, port = Consul(config.CONSUL_HOST, config.CONSUL_PORT).get_host_port(
        f'{config.CONSUL_FILTER_KEY}=={config.CONSUL_FILTER_VALUE}')
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
    retry_interceptor = get_retry_interceptor()
    tracing_interceptor = get_tracing_interceptor()
    retry_channel = grpc.intercept_channel(greeter_channel, retry_interceptor)
    tracing_channel = intercept_channel(retry_channel, tracing_interceptor)
    return tracing_channel
