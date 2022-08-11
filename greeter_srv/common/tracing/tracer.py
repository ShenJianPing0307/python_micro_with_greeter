from settings import settings
from jaeger_client import Config


def init_global_tracer():
    jaeger_config = Config(
        config={
            'sampler': {
                'type': settings.JAEGER_CONFIG_SAMPLER_TYPE,
                'param': settings.JAEGER_CONFIG_SAMPLER_PARAM,
            },
            'local_agent': {
                'reporting_host': settings.JAEGER_CONFIG_LOCAL_AGENT_REPORTING_HOST,
                'reporting_port': settings.JAEGER_CONFIG_LOCAL_AGENT_REPORTING_PORT,
            },
            'logging': settings.JAEGER_CONFIG_LOGGING,
        },
        service_name=settings.JAEGER_SERVICE_NAME,
        validate=settings.JAEGER_VALIDATE,
    )
    tracer = jaeger_config.initialize_tracer()
    settings.JAEGER_TRACER = tracer

