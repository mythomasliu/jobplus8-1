class BaseConfig:
    SECRET_KEY='makesure to set a very secret key'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    INDEX_PER_PAGE=9
    ADMIN_PER_PAGE=9


class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = { 'development' : DevelopmentConfig,
            'production' : ProductionConfig,
            'testing' : TestingConfig
            }
