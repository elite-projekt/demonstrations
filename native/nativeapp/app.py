import argparse
from datetime import datetime
import logging
import os

import flask
import flask_cors
from native.src.config import config

# import demo controllers
from demos.download.native import download_controller
from demos.password.native import password_controller
from demos.phishing.native import phishing_controller

app = flask.Flask(__name__)
flask_cors.CORS(app)

# register demo controllers
app.register_blueprint(download_controller.orchestration)
app.register_blueprint(phishing_controller.orchestration)
app.register_blueprint(password_controller.orchestration)


def main():
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
        config.EnvironmentConfig.ENVDIR = args.path

    logging_path = config.EnvironmentConfig.WORKINGDIR + "\\nativeapp.log"
    # initiate logging
    logging.basicConfig(
        filename=logging_path,
        datefmt="%y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s - [%(module)s:%(funcName)s] : "
               "%(message)s",
        level=logging.DEBUG,
    )
    logging.info("Starting service: native app")

    # display application information
    if not (hasattr(config.ApplicationInformation, "VERSION")
            and hasattr(config.ApplicationInformation, "BUILDDATE")):
        setattr(config.ApplicationInformation, "VERSION", "LOCAL DEV")
        setattr(config.ApplicationInformation, "BUILDDATE",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    logging.info(
        "\n\nVERSION: {}\nBUILDDATE: {}".format(
            config.ApplicationInformation.VERSION,
            config.ApplicationInformation.BUILDDATE
        )
    )

    # print for display in console window
    print(
        "\n>> {} <<\n{:15s} {}\n{:15s} {}\n{:15s} {}\n".format(
            config.ApplicationInformation.DESCRIPTION,
            "VERSION:",
            config.ApplicationInformation.VERSION,
            "BUILDDATE:",
            config.ApplicationInformation.BUILDDATE,
            "DEBUG LOG:",
            logging_path
        )
    )

    # start flask
    app.run(host=app.config["HOST"], debug=app.config["DEBUG"],
            port=app.config["PORT"])


if __name__ == "__main__":
    main()
