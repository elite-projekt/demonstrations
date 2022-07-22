from abc import ABC

import logging
import flask
from markupsafe import escape

from nativeapp.controller import orchestration_controller

from typing import Dict


class DemoController(ABC):

    def __init__(self, name, compose_file):
        self.compose_file = compose_file
        self.name = name
        self.state = "offline"

    def set_state(self, state: str) -> None:
        self.state = state

    def get_state(self) -> str:
        return self.state

    def stop(self, subpath: str) -> Dict[str, object]:
        """
        Stops the demo
        """
        orchestration_controller.orchestration_service.\
            docker_compose_stop_file(self.compose_file)
        return orchestration_controller.stop_success

    def start(self, subpath: str, params: Dict[str, str]) -> Dict[str, object]:
        """
        Start the demo
        """
        orchestration_controller.orchestration_service.\
            docker_compose_start_file(self.compose_file)
        return orchestration_controller.start_success

    def get_status(self, subpath: str) -> Dict[str, str]:
        """
        Get the status of the demo
        """
        return {"state": self.get_state()}


class DemoManager():
    orchestration = flask.Blueprint(
            "DemoManager", __name__, url_prefix="/orchestration/")
    demos = {}

    @staticmethod
    def register_demo(demo: DemoController):
        logging.info(f"Registering demo {demo.name}")
        DemoManager.demos[demo.name] = demo

    @staticmethod
    def get_flask_response(ret_val):
        return flask.helpers.make_response(flask.json.jsonify(ret_val), 200)

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
        flask.abort(500)

    @staticmethod
    @orchestration.route("/start/demo/<demo_name>", methods=["GET", "POST"])
    @orchestration.route("/start/demo/<demo_name>/<path:subpath>",
                         methods=["GET", "POST"])
    def demo_start(demo_name, subpath=""):
        demo_name = escape(demo_name)
        subpath = escape(subpath)
        if demo_name in DemoManager.demos:
            ret_val = DemoManager.demos[demo_name].\
                    start(subpath=subpath, params=flask.request.json)
            return DemoManager.get_flask_response(ret_val)
        flask.abort(500)

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
        flask.abort(500)
