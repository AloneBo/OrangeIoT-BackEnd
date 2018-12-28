import flask
from flask import current_app
from flask_wtf import csrf
from .utils import commons
# 静态文件的蓝图

html = flask.Blueprint('web_html', __name__)


@html.route("/<re(r'.*'):file_name>")
def get_html(file_name):
    """提供html文件"""
    # print('get_html: '+ file_name)

    if not file_name:
        # file_name = 'index.html'
        pass
    if file_name.endswith('.html'):
        # file_name = 'html/' + file_name
        pass

    # 生成csrf
    # csrf_token = csrf.generate_csrf()
    #
    resp = flask.make_response(current_app.send_static_file(file_name))
    # resp.set_cookie('csrf_token', csrf_token)  # 设置cookie
    return resp
