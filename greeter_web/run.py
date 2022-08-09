import initialize
import config
import utils
import uuid
from loguru import logger
import sys


def run():
    # 初始化app
    app = initialize.init_app()

    # 服务注册
    register_client = utils.Consul(config.CONSUL_HOST, config.CONSUL_PORT)
    service_id = str(uuid.uuid1())
    if not register_client.register(address=config.SERVICE_HOST, port=config.SERVICE_PORT, name=config.SERVICE_NAME,
                                    tags=config.SERVICE_TAGS, id=service_id, check=None):
        logger.info(f"服务注册失败")
        sys.exit(0)

    logger.info(f"服务注册成功")

    # 启动服务与健康检查
    app.run(host=config.SERVICE_HOST, port=config.SERVICE_PORT)

    # 接收终止信号


if __name__ == '__main__':
    run()
