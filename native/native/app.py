from flask import Flask
from flask_cors import CORS
from config.config import DevelopmentConfig, ProductionConfig
from controller.OrchestrationController import orchestration
import sys
import logging

app = Flask(__name__)
CORS(app)

app.register_blueprint(orchestration)

if __name__ == "__main__":
    # set working directory
    app.WORKINGDIR = os.getenv('ProgramFiles(x86)') + r'\hda\nativeapp'

    # initiate logging
    logging.basicConfig(filename=app.WORKINGDIR + '\\service.log', datefmt='%y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)-8s - [%(module)s:%(funcName)s] : %(message)s', level=logging.DEBUG)
    logging.info('Starting service: native app')

    # Only for debugging while developing
    if len(sys.argv) > 1:
        if sys.argv[1] == "prod":
            app.config.from_object(ProductionConfig)
        elif sys.argv[1] == "dev":
            app.config.from_object(DevelopmentConfig)
        elif sys.argv[1] == "path":
            app.WORKINGDIR = str(sys.argv[2])
    else:
        app.config.from_object(DevelopmentConfig)

    app.run(host=app.config["HOST"], debug=app.config["DEBUG"], port=app.config["PORT"])
