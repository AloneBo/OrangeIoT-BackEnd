from . import api
from flask_wtf import csrf
from flask import current_app, request, jsonify, make_response
import flask
import logging
from iotweb.utils.response_code import RET
from iotweb.models import User
from iotweb import redis_db
import datetime
from config import Config


@api.route('/csrf')
def get_csrf():
    csrf_token = csrf.generate_csrf()
    resp = flask.make_response()
    logging.error(datetime.datetime.today()+datetime.timedelta(seconds=Config.PERMANENT_SESSION_LIFETIME))
    resp.set_cookie('csrf_token', csrf_token, max_age=Config.PERMANENT_SESSION_LIFETIME)  # 设置cookie
    resp.set_cookie('test_cookie', 'haha')
    return resp


@api.route('/users/sessions', methods=['POST'])
def login():
    req_json = request.get_json()
    user_name = req_json.get('user_name')
    password = req_json.get('password')
    verify_code = req_json.get('verify_code')
    verify_code_id = req_json.get('verify_code_id')
    # 验证密码是否完整
    if not all([user_name, password, verify_code, verify_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 业务逻辑  取出真实的验证码值判断 判断验证码成功再判断用户密码
    try:
        real_image_code = redis_db.get("image_code:{}".format(verify_code_id))
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis 数据异常')

        # 如果查询到的是None
    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmsg='图片验证失败')

        # 销毁验证码
    try:
        redis_db.delete('image_code:%s' % verify_code_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.NODATA, errmsg='redis错误')

        # 验证码错误

    if real_image_code.decode().lower() != verify_code.lower():

        return jsonify(errno=RET.DATAERR, errmsg='验证码错误')

    # 查询用户
    try:
        user = User.query.filter_by(name=user_name).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库错误')

    # 验证
    if user is None or not user.check_password(password):
        return jsonify(errno=RET.NODATA, errmsg='用户名或密码错误')

    # 验证通过， 保存用户状态
    flask.session['name'] = user.name
    flask.session['user_id'] = user.id

    return jsonify(errno=RET.OK, errmsg='登陆成功')


@api.route('/users/sessions', methods=['GET'])
def check_login():
    name = flask.session.get('name')  # 根据sessions(csrf_token)获取用户名

    if name is not  None:
        logging.info('{} has logined'.format(name))
        return jsonify(errno=RET.OK, errmsg='true', data={'name': name})
    else:
        return jsonify(errno=RET.NODATA, errmsg='false')


@api.route('/users/sessions', methods=['DELETE'])
def logout():
    logging.info('exit login')
    old_csrf = flask.session.get('csrf_token')
    flask.session.clear()
    flask.session['csrf_token'] = old_csrf

    # resp = make_response()
    # resp.headers['content-type'] = 'application/json'
    # resp.response = '{"errno": %s, "errmsg"="OK"}' % RET.OK
    # resp.set_cookie('csrf_token', expires=0)
    # return resp
    return jsonify(errno=RET.OK, errmsg='OK')



@api.route('/users/mqttprofile', methods=['GET'])
def get_profile():
    data = {'mqtt_user': 'alonebo', 'mqtt_password': '976447044'}
    return jsonify(errno=RET.OK, errmsg="OK", data=data)