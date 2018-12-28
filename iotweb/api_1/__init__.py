from flask import Blueprint

# 蓝图对象
api = Blueprint('api_1_0', __name__)

from . import demo

from . import passport

from . import verify_code