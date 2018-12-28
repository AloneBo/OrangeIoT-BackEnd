import flask
import config
import redis
import flask_sqlalchemy
import flask_session
import flask_wtf
import logging

from logging.handlers import RotatingFileHandler


db = flask_sqlalchemy.SQLAlchemy()


# redis数据库
redis_db = None

mongo_db = None


# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile = 'logs/log.txt'
fh = RotatingFileHandler("logs/log.txt", maxBytes=1024*1024*100, backupCount=10)
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)


def create_app(*, config_name):
    assert isinstance(config_name, str)
    app = flask.Flask(__name__)
    # app = flask.Flask(__name__, static_folder='static', static_url_path='/test')

    # 根据模式名字匹配参数
    config_class = config.config_map.get(config_name)
    app.config.from_object(config_class)

    # 数据库初始化
    db.init_app(app)

    # session 初始化
    flask_session.Session(app)

    # csrf 防护
    flask_wtf.CSRFProtect(app)

    # 初始化redis
    global redis_db
    redis_db = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 注册转换器
    from iotweb.utils import commons
    app.url_map.converters["re"] = commons.ReConverter

    # 蓝图注册
    from . import api_1
    app.register_blueprint(api_1.api, url_prefix='/api/v1.0')

    return app
