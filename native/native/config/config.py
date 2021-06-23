class Config(object):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "development"
    HOST = "localhost"
    PORT = 5000

class ProductionConfig(Config):
    ENV = "production"
    HOST = "0.0.0.0"
    PORT = 5000

class EnvironmentConfig():
    WORKINGDIR = "C:\\Users\\dummy\\Documents\\GIT\\demonstrations\\native\\native\\"