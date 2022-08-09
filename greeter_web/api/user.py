from flask import Blueprint, jsonify

user = Blueprint('user', __name__)


@user.route('/index')
def index():
    data = {
        "title": "user"
    }
    return jsonify(data)
