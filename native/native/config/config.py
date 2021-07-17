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
    WORKINGDIR = "C:\\Program Files (x86)\\hda\\nativeapp\\"
    DOCKERSTACKDIR = WORKINGDIR + "stacks\\"
    PROFILEDIR = WORKINGDIR + "profiles\\"