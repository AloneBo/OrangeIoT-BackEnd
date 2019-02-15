import redis


class Config(object):
    SECRET_KEY = "SECRET_KEY"

    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:alonebo@127.0.0.1:3306/db_iotweb?charset=utf8"
    SQLALCHEMY_DATABASE_URI = "sqlite:///user.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # refer https://pythonhosted.org/Flask-Session/
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    # PERMANENT_SESSION_LIFETIME = 86400 # 1天
    PERMANENT_SESSION_LIFETIME = 86400

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    WTF_CSRF_TIME_LIMIT = PERMANENT_SESSION_LIFETIME


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config_map = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}