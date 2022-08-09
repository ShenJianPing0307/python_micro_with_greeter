from .hello import hello
from .user import user


def register_blueprint(app):
    app.register_blueprint(hello, url_prefix='/hello')
    app.register_blueprint(user, url_prefix='/user')
