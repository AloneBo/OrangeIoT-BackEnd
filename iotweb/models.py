
from datetime import datetime


from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_enc = db.Column(db.String(128), nullable=False)


    @property
    def password(self):
        raise AttributeError('这个属性只能设置， 使用password_enc代替')

    @password.setter
    def password(self, original_pwd):
        self.password_enc = generate_password_hash(original_pwd)


    def check_password(self, original_pwd):
        return check_password_hash(self.password_enc, original_pwd)


