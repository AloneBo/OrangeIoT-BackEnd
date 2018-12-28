from . import api
import flask
from flask import current_app
import logging
from  iotweb import db
from iotweb import models


@api.route('/index')
def index():
    # current_app.logger.error('errt')
    logging.error('loggin error')
    return 'index data'


@api.route('/add_user')
def add_user():
    """
    Just use for testing.
    :return:
    """
    user = models.User(name='alonebo')
    user.password = "alonebo"
    db.session.add(user)
    db.session.commit()
    print('add user success!')
    return 'success'
