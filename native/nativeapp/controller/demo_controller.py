from abc import ABC

import logging
import flask
from markupsafe import escape
import queue
import json
import pathlib

from nativeapp.service import orchestration_service
from nativeapp.utils.locale import locale
from nativeapp.utils.web import web_view

from typing import Dict


class DemoStatus:
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class ErrorCodes():
    start_success = DemoStatus("Successfully started the Demo.", 200)
    invalid_state = DemoStatus("Demo is in an invalid state", 500)
    enter_success = DemoStatus("Successfully entered the Demo.", 200)
    stop_success = DemoStatus("Stopped all remaining Demos.", 200)
    stop_success = DemoStatus("Stopped all remaining Demos.", 200)
    stop_failed = DemoStatus("Failed to stop containers.", 500)
    no_docker_error = DemoStatus(
            "The workstation can not start the application!",
            500)
    no_mail_server_error = DemoStatus("The mailserver is not reachable!", 500)
    generic_error = DemoStatus("Unknown error", 500)


class DemoStates():
    OFFLINE = "offline"
    STARTING = "starting"
    RUNNING = "running"
    READY = "ready"
    ERROR = "error"
    STOPPING = "stopping"
    STARTING_CONTAINER = "container_start_state"
    STARTING_APPLICATIONS = "application_start_state"
    STOPPING_CONTAINER = "container_stop_state"
    STOPPING_APPLICATIONS = "application_stop_state"


class DemoController(ABC):

    def __init__(self, name: str, compose_file: str):
        self.compose_file = compose_file
        self.name = name
        self.state = "offline"
        self.extra_state = ""
        self.orchestration = orchestration_service.OrchestrationService()
        self.state_changed_callback = None

        self.title = f"{name}_title"
        self.description = f"{name}_description"
        self.guide_dict = {"guide_intro": f"{name}_guide_intro",
                           "guide_task": f"{name}_guide_task",
                           "guide_goal": f"{name}_guide_goal",
                           "guide_req": f"{name}_guide_req"}
        self.level = "beginner"
        self.time = 0
        self.hardware = []
        self.instructor_id = 3
        self.is_available = False

        self.locale = locale.Locale()

        demo_path = (pathlib.Path(__file__)
                     .parent
                     .parent
                     .parent / "demos" / name / "demo.json").absolute()
        self.load_from_json(demo_path)
        locale_path = (pathlib.Path(__file__)
                       .parent
                       .parent
                       .parent / "demos" / name / "locales").absolute()
        if locale_path.is_dir():
            self.locale.add_locale_dir(locale_path)

    def load_from_json(self, json_path: pathlib.Path):
        json_path = pathlib.Path(json_path)
        if json_path.exists():
            json_data = ""
            with open(json_path, "r") as json_file:
                json_data = json.loads(json_file.read())

            if "title" in json_data:
                self.title = json_data["title"]

            if "description" in json_data:
                self.description = json_data["description"]

            if "time" in json_data:
                self.time = int(json_data["time"])

            if "level" in json_data:
                self.level = json_data["level"]

            if "guide" in json_data:
                self.guide_dict = json_data["guide"]

            if "hardware" in json_data:
                self.hardware = json_data["hardware"]

            if "instructor_id" in json_data:
                self.instructor_id = json_data["instructor_id"]

            if "isAvailable" in json_data:
                self.is_available = json_data["isAvailable"]

    def set_state(self, state: str, extra_state: str = "") -> None:
        """
        Sets the current state of the demo

        :param sate: The current state. Possible states:
            "offline", "starting", "running", "stopping", "error"
        """
        if self.state_changed_callback is not None:
            self.state_changed_callback(self.name,
                                        self.state,
                                        state,
                                        self.locale.translate(state),
                                        self.locale.translate(extra_state))
        self.state = state
        self.extra_state = extra_state

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

    def enter(self, subpath: str) -> Dict[str, object]:
        """
        Enter the demo

        :param subpath: The subpath the request might have had
        """
        return ErrorCodes.enter_success

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

    def get_property_dict(self, lang="en") -> Dict[str, any]:
        self.locale.update_locale(lang)
        data_dict = {}
        data_dict["name"] = self.name
        data_dict["description"] = self.locale.translate(self.description)
        data_dict["state"] = self.state
        data_dict["state_text"] = self.locale.translate(self.state)
        data_dict["title"] = self.locale.translate(self.title)
        data_dict["time"] = self.time
        data_dict["level"] = self.locale.translate(self.level)
        data_dict["guide"] = dict(
            map(lambda tup: (tup[0],
                             self.locale.translate(tup[1])),
                self.guide_dict.items()))
        data_dict["hardware"] = self.hardware
        data_dict["instructor_id"] = self.instructor_id
        data_dict["isAvailable"] = self.is_available
        return data_dict


class DemoManager():
    orchestration = flask.Blueprint(
            "DemoManager", __name__, url_prefix="/orchestration/")
    demos = {}
    status_event_queues = []

    @staticmethod
    def on_state_changed(name,
                         old_state,
                         new_state,
                         new_state_translation,
                         extra_state=""):
        status_dict = {"name": name,
                       "old_state_id": old_state,
                       "state_id": new_state,
                       "state": new_state_translation,
                       "extra_state": extra_state}
        print(f"State changed for demo {name} from {old_state} to {new_state}")
        for q in DemoManager.status_event_queues:
            q.put(status_dict)

    @staticmethod
    def register_demo(demo: DemoController):
        logging.info(f"Registering demo {demo.name}")
        demo.state_changed_callback = DemoManager.on_state_changed
        DemoManager.demos[demo.name] = demo

    @staticmethod
    def get_flask_response(status: DemoStatus):
        return flask.helpers.make_response(
                flask.json.jsonify(status.message), status.status_code)

    @staticmethod
    @orchestration.route("/getdemos", methods=["GET", "POST"])
    def getDemos():
        params = flask.request.get_json(silent=True)
        lang = "en"
        if params is not None and "language" in params:
            lang = params["language"]
        send_dict = {}
        local_locale = locale.Locale()
        local_locale.update_locale(lang)
        common_translation_ids = [
                "start_button",
                "stop_button",
                "learn_button",
                "usb-stick",
                "wifi-stick",
                "phone",
                "tooltip_time",
                "tooltip_difficulty",
                "tooltip_hardware",
                "guide_intro",
                "guide_task",
                "guide_goal",
                "guide_req"
                ]
        common_translations = {}
        for x in common_translation_ids:
            common_translations[x] = local_locale.translate(x)
        demo_list = []
        for demo in DemoManager.demos.values():
            new_demo = demo.get_property_dict(lang)
            if new_demo["isAvailable"]:
                demo_list.append(new_demo)
        send_dict = {"demos": demo_list,
                     "common_translations": common_translations}
        return flask.jsonify(send_dict)

    @staticmethod
    @orchestration.route("/status/stream", methods=["GET", "POST"])
    def demo_status_stream():
        logging.info("Got new stream client")

        def eventStream():
            q = queue.Queue()
            for demo in DemoManager.demos.values():
                state = demo.get_state()
                extra_state = demo.locale.translate(demo.extra_state)
                status_dict = {"name": demo.name,
                               "old_state_id": state,
                               "state_id": state,
                               "state": demo.locale.translate(state),
                               "extra_state": extra_state}
                q.put(status_dict)

            DemoManager.status_event_queues.append(q)
            try:
                while True:
                    item = q.get()
                    item_json = json.dumps(item)
                    q.task_done()
                    yield f"data: {item_json}\n\n"
            finally:
                DemoManager.status_event_queues.remove(q)
                logging.info("Client disconnected")
        return flask.Response(eventStream(), mimetype="text/event-stream")

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
        skip_enter = False
        try:
            web_view.RemoteControlClient().set_on_top(True)
        except Exception:
            # No web view client -> skip enter phase
            skip_enter = True
        if demo_name in DemoManager.demos:
            params = flask.request.get_json(silent=True)
            if params is None:
                params = []
            ret_val = DemoManager.demos[demo_name].\
                start(subpath=subpath, params=params)
            if skip_enter:
                ret_val = DemoManager.demos[demo_name].\
                          enter(subpath=subpath)
            return DemoManager.get_flask_response(ret_val)
        return DemoManager.get_flask_response(ErrorCodes.generic_error)

    @staticmethod
    @orchestration.route("/enter/demo/<demo_name>", methods=["GET", "POST"])
    @orchestration.route("/enter/demo/<demo_name>/<path:subpath>",
                         methods=["GET", "POST"])
    def demo_enter(demo_name, subpath=""):
        try:
            client = web_view.RemoteControlClient()
            client.minimize()
            client.set_on_top(False)
        except Exception:
            pass

        demo_name = escape(demo_name)
        subpath = escape(subpath)
        if demo_name in DemoManager.demos:
            ret_val = DemoManager.demos[demo_name].enter(subpath=subpath)
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
