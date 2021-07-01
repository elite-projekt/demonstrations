from flask import Flask
from flask_cors import CORS
from config.config import DevelopmentConfig, ProductionConfig
from controller.OrchestrationController import orchestration
import sys
import logging
import argparse

app = Flask(__name__)
CORS(app)

app.register_blueprint(orchestration)

if __name__ == "__main__":
    # set working directory
    app.WORKINGDIR = os.getenv('ProgramFiles(x86)') + r'\hda\nativeapp'

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Basepath of project relative from here files will be accessed. Default is "C:\Program Files (x86)\hda\nativeapp".')
    parser.add_argument('-d', '--dev', help='Starts flask in dev-mode')
    args = parser.parse_args()

    # Only for debugging while developing
    if args.dev is not None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
    if args.path is not None:
        app.WORKINGDIR = args.path

    # initiate logging
    logging.basicConfig(filename=app.WORKINGDIR + '\\service.log', datefmt='%y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)-8s - [%(module)s:%(funcName)s] : %(message)s', level=logging.DEBUG)
    logging.info('Starting service: native app')

    app.run(host=app.config["HOST"], debug=app.config["DEBUG"], port=app.config["PORT"])
