# 定义正则转换器

import werkzeug.routing as wr
from flask import session, jsonify, g
from iotweb.utils.response_code import RET
import functools


class ReConverter(wr.BaseConverter):
    def __init__(self, url_map, regex):
        super(ReConverter, self).__init__(url_map)
        self.regex = regex


def login_required(fun):
    """
    验证登陆状态的装饰器
    :param fun:
    :return:
    """
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        # 判断用户的登陆状态
        user_id = session.get("user_id")
        if user_id is not None:
            g.user_id = user_id  # 将user_id保存到g对象中，让视图函数可以调用
            return fun(*args, **kwargs)
        else:
            # 没有登陆

            return jsonify(errno=RET.SESSIONERR, errmsg="用户没有登陆")

    return wrapper


@login_required
def test():
    user_id = g.user_id
    print(user_id)
