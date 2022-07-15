"""
Copyright (C) 2022 Kevin Köster

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""
import flask
import logging

from nativeapp.controller import orchestration_controller
from nativeapp.config import config

from demos.uhh_ducky_mitm.native import uhh_ducky_mitm_demo


orchestration = flask.Blueprint("uhh_ducky_mitm", __name__,
                                url_prefix="/orchestration/")

ducky_service = uhh_ducky_mitm_demo.DuckyDemo()

state = "offline"


def set_state(new_state: str) -> None:
    global state
    state = new_state


def get_state() -> str:
    return state


# uhh_ducky_mitm demonstration
@orchestration.route("/start/demo/uhh_ducky_mitm", methods=["POST", "GET"])
def start_demo_uhh_ducky_mitm():
    try:
        try:
            config.EnvironmentConfig.LANGUAGE = flask.request.json["language"]
        except Exception:
            pass
        logging.info("Starting uhh_ducky_mitm demo stack")
        set_state("starting")
        orchestration_controller.orchestration_service \
            .docker_compose_start_file(
                "uhh_ducky_mitm/native/stacks/docker-compose.yml",
                additional_env={
                    "ELITE_LANG": config.EnvironmentConfig.LANGUAGE
                    })
        orchestration_controller.orchestration_service \
            .wait_for_container("uhh_ducky_mitm_mailserver")
        ducky_service.start()
        set_state("running")
    except Exception as e:
        logging.error(e)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error), 500)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/uhh_ducky_mitm", methods=["POST", "GET"])
def stop_demo_uhh_ducky_mitm():
    set_state("stopping")
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "uhh_ducky_mitm/native/stacks/docker-compose.yml")
    ducky_service.stop()
    set_state("offline")
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/uhh_ducky_mitm", methods=["GET"])
def status_demo_uhh_ducky_mitm():
    result = {"state": get_state()}
    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/uhh_ducky_mitm/sum", methods=["GET"])
def status_demo_uhh_ducky_mitm_sum():
    result = {"state": get_state()}
    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/start/demo/uhh_ducky_mitm/script_downloaded",
                     methods=["GET"])
def on_script_downloaded():
    ducky_service.add_cert()
    ducky_service.show_error_box()
    ducky_service.send_second_mail()

    return flask.helpers.make_response(flask.json.jsonify(1), 200)
