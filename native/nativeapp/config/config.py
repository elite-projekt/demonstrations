# SPDX-License-Identifier: AGPL-3.0-only

import pathlib


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


class EnvironmentConfig():
    WORKINGDIR: pathlib.Path
    PROFILEDIR: pathlib.Path
    ENVDIR: pathlib.Path
    LANGUAGE = "de"


class ApplicationInformation:
    DESCRIPTION = "NativeApp Client for ELITE Platform"
    VERSION = None
    BUILDDATE = None


class AdminConfig:
    LISTEN_PORT = 5005
