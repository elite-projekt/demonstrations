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
    HOST = "0.0.0.0"  # nosec No Issue in a docker Container
    PORT = 5000


class EnvironmentConfig:
    WORKINGDIR = "C:\\Program Files (x86)\\hda\\nativeapp\\"
    DOCKERSTACKDIR = WORKINGDIR + "stacks\\"
    PROFILEDIR = WORKINGDIR + "profiles\\"
    ENVDIR = WORKINGDIR


class ApplicationInformation:
    DESCRIPTION = "HDA MPSE Project native app client"
    VERSION = "1.5"
    BUILDDATE = "February 2022"
