from flask import Flask

import api


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_path = os.path.join(BASE_DIR, 'config', 'config.py')



def init_app():
    # 实例化app
    app = Flask(__name__)

    # 导入配置项
    # app.config.from_object(config)
    app.config.from_pyfile(config_path)

    # 注册蓝图
    api.register_blueprint(app)

    # 健康检查
    @app.route('/health', methods=['GET'])  # 健康检查url
    def check():
        return 'success'

    return app
