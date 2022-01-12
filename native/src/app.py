import argparse
import logging
import os

import flask
import flask_cors

from demos.download.native import download_controller
from demos.password.native import password_controller
from demos.phishing.native import phishing_controller
from native.src.config import config

app = flask.Flask(__name__)
flask_cors.CORS(app)

app.register_blueprint(download_controller.orchestration)
app.register_blueprint(phishing_controller.orchestration)
app.register_blueprint(password_controller.orchestration)

if __name__ == "__main__":
    # set working directory
    config.EnvironmentConfig.WORKINGDIR = os.getenv(
        "ProgramFiles(x86)") + r"\hda\nativeapp"

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help='Basepath of project relative from here files will be accessed. '
             'Default is "C:\\Program Files (x86)\\hda\\nativeapp". If passed '
             'path - structure is fixed on current repo relative placement of '
             'files!!\n\nno trailing slashes',
    )
    parser.add_argument("-d", "--dev", help="Starts flask in dev-mode")
    args = parser.parse_args()

    # Only for debugging while developing
    if args.dev is not None:
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.ProductionConfig)
    if args.path is not None:
        config.EnvironmentConfig.WORKINGDIR = args.path
        config.EnvironmentConfig.DOCKERSTACKDIR = args.path + '\\..\\stacks\\'
        config.EnvironmentConfig.PROFILEDIR = args.path + '\\profiles\\'
        config.EnvironmentConfig.ENVDIR = args.path + '\\..\\..\\'

    # initiate logging
    logging.basicConfig(
        filename=config.EnvironmentConfig.WORKINGDIR + "\\service.log",
        datefmt="%y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s - [%(module)s:%(funcName)s] : "
               "%(message)s",
        level=logging.DEBUG,
    )
    logging.info("Starting service: native app")

    # display application information
    logging.info(
        "\n\nVERSION: {}\nBUILDDATE: {}".format(
            config.ApplicationInformation.VERSION,
            config.ApplicationInformation.BUILDDATE
        )
    )

    # print for display in console window
    print(
        "\n>> {} <<\n{:15s} {}\n{:15s} {}\n".format(
            config.ApplicationInformation.DESCRIPTION,
            "VERSION:",
            config.ApplicationInformation.VERSION,
            "BUILDDATE:",
            config.ApplicationInformation.BUILDDATE,
        )
    )

    # start flask
    app.run(host=app.config["HOST"], debug=app.config["DEBUG"],
            port=app.config["PORT"])
