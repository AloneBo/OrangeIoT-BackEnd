from . import api
from iotweb.libs.captchalib.captcha import get_captcha_img
from iotweb import redis_db
from iotweb import constants
from flask import jsonify, make_response
from iotweb.utils.response_code import RET
import logging


@api.route('image_codes/<image_code_id>')
def get_image_code(image_code_id):
    image_data, text = get_captcha_img()
    try:
        redis_db.setex('image_code:{}'.format(image_code_id), constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片失败')

    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/png'

    return resp
