import argparse
import importlib
import logging
import pathlib
import pkgutil
import subprocess  # nosec
from datetime import datetime

import flask
import flask_cors
from nativeapp.config import config
from nativeapp.controller import native_controller

import demos

app = flask.Flask(__name__)
flask_cors.CORS(app)

app.register_blueprint(native_controller)
for _, name, ispkg in pkgutil.iter_modules(demos.__path__):
    if ispkg:
        controller_path = 'demos.' + name + '.native.' + name + '_controller'
        try:
            # import demo controllers
            controller = importlib.import_module(controller_path)
            # register blueprints from controllers
            app.register_blueprint(controller.orchestration)
        except ModuleNotFoundError:
            print("ERROR while importing controller for: {} demo".format(name))
            print("Please check the existence of: {}".format(controller_path))
            raise
        except Exception as e:
            raise e


def main():
    # argument parser
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-p",
        "--path",
        help='Basepath of project relative from here files will be accessed. '
             'If passed path - '
             'structure is fixed on current repo relative placement of '
             'files!!',
        default="C:\\Program Files (x86)\\hda\\nativeapp"
    )
    parser.add_argument("-d", "--dev", help="Starts flask in dev-mode")
    args = parser.parse_args()

    # Only for debugging while developing
    if args.dev is not None:
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.ProductionConfig)
    arg_path = pathlib.Path(args.path)
    config.EnvironmentConfig.WORKINGDIR = arg_path
    config.EnvironmentConfig.PROFILEDIR = arg_path / "profiles"
    config.EnvironmentConfig.ENVDIR = arg_path

    logging_path = pathlib.Path(config.EnvironmentConfig.WORKINGDIR) / \
        "nativeapp.log"
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
    if config.ApplicationInformation.VERSION is None:
        config.ApplicationInformation.VERSION = "LOCAL DEV"
    if config.ApplicationInformation.BUILDDATE is None:
        config.ApplicationInformation.BUILDDATE = \
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    # ensure dockerd is running. it won't start if it is already running
    subprocess.Popen(["wsl", "--user", "root", "dockerd"],  # nosec
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     cwd=pathlib.Path().home())

    # start flask
    app.run(host=app.config["HOST"], debug=app.config["DEBUG"],
            port=app.config["PORT"])


if __name__ == "__main__":
    main()
