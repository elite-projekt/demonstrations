from flask import Flask
from flask_cors import CORS
from config.config import DevelopmentConfig, ProductionConfig
from controller.OrchestrationController import orchestration
import sys

app = Flask(__name__)
CORS(app)

app.register_blueprint(orchestration)

if __name__ == "__main__":
    # Only for debugging while developing
    if len(sys.argv) > 1:
        if sys.argv[1] == "prod":
            app.config.from_object(ProductionConfig)
        elif sys.argv[1] == "dev":
            app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    app.run(host=app.config["HOST"], debug=app.config["DEBUG"], port=app.config["PORT"])
