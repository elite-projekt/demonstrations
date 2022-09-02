from abc import ABC

import logging
import flask
from markupsafe import escape

from nativeapp.service import orchestration_service

from typing import Dict


class DemoStatus:
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class ErrorCodes():
    start_success = DemoStatus("Successfully started the Demo.", 200)
    invalid_state = DemoStatus("Demo is in an invalid state", 500)
    stop_success = DemoStatus("Stopped all remaining Demos.", 200)
    stop_failed = DemoStatus("Failed to stop containers.", 500)
    no_docker_error = DemoStatus(
            "The workstation can not start the application!",
            500)
    no_mail_server_error = DemoStatus("The mailserver is not reachable!", 500)
    generic_error = DemoStatus("Unknown error", 500)


class DemoController(ABC):

    def __init__(self, name: str, compose_file: str):
        self.compose_file = compose_file
        self.name = name
        self.state = "offline"
        self.orchestration = orchestration_service.OrchestrationService()

    def set_state(self, state: str) -> None:
        """
        Sets the current state of the demo

        :param sate: The current state. Possible states:
            "offline", "starting", "running", "stopping", "error"
        """
        self.state = state

    def get_state(self) -> str:
        """
        Returns the current state

        :return: The current state as a string
        """
        return self.state

    def stop(self, subpath: str) -> Dict[str, object]:
        """
        Stops the demo

        :param subpath: The subpath the request might have had
        """
        self.stop_container()
        return ErrorCodes.stop_success

    def start(self, subpath: str, params: Dict[str, str]) -> Dict[str, object]:
        """
        Start the demo

        :param subpath: The subpath the request might have had
        :param params: A dict of additional options.
            For example language settings
        """
        self.start_container()
        return ErrorCodes.start_success

    def get_status(self, subpath: str) -> Dict[str, str]:
        """
        Get the status of the demo
        """
        return DemoStatus({"state": self.get_state()}, 200)

    def start_container(self, additional_env={}):
        self.orchestration.docker_compose_start_file(
                self.compose_file,
                additional_env=additional_env)

    def stop_container(self):
        self.orchestration.docker_compose_stop_file(self.compose_file)


class DemoManager():
    orchestration = flask.Blueprint(
            "DemoManager", __name__, url_prefix="/orchestration/")
    demos = {}

    @staticmethod
    def register_demo(demo: DemoController):
        logging.info(f"Registering demo {demo.name}")
        DemoManager.demos[demo.name] = demo

    @staticmethod
    def get_flask_response(status: DemoStatus):
        return flask.helpers.make_response(
                    flask.json.jsonify(status.message), status.status_code)

    @staticmethod
    @orchestration.route("/status/demo/<demo_name>", methods=["GET", "POST"])
    @orchestration.route("/status/demo/<demo_name>/<path:subpath>",
                         methods=["GET", "POST"])
    def demo_status(demo_name, subpath=""):
        demo_name = escape(demo_name)
        subpath = escape(subpath)
        if demo_name in DemoManager.demos:
            ret_val = DemoManager.demos[demo_name].get_status(subpath)
            return DemoManager.get_flask_response(ret_val)
        return DemoManager.get_flask_response(ErrorCodes.generic_error)

    @staticmethod
    @orchestration.route("/start/demo/<demo_name>", methods=["GET", "POST"])
    @orchestration.route("/start/demo/<demo_name>/<path:subpath>",
                         methods=["GET", "POST"])
    def demo_start(demo_name, subpath=""):
        demo_name = escape(demo_name)
        subpath = escape(subpath)
        if demo_name in DemoManager.demos:
            ret_val = DemoManager.demos[demo_name].\
                start(subpath=subpath,
                      params=flask.request.get_json(silent=True))
            return DemoManager.get_flask_response(ret_val)
        return DemoManager.get_flask_response(ErrorCodes.generic_error)

    @staticmethod
    @orchestration.route("/stop/demo/<demo_name>", methods=["GET", "POST"])
    @orchestration.route("/stop/demo/<demo_name>/<path:subpath>",
                         methods=["GET", "POST"])
    def demo_stop(demo_name, subpath=""):
        demo_name = escape(demo_name)
        subpath = escape(subpath)
        if demo_name in DemoManager.demos:
            ret_val = DemoManager.demos[demo_name].stop(subpath)
            return DemoManager.get_flask_response(ret_val)
        return DemoManager.get_flask_response(ErrorCodes.generic_error)
