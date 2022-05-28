import flask
import logging

from nativeapp.controller import orchestration_controller
from nativeapp.config import config

from demos.uhh_ducky_mitm.native import uhh_ducky_mitm_demo

orchestration = flask.Blueprint("uhh_ducky_mitm", __name__,
                                url_prefix="/orchestration/")

ducky_service = uhh_ducky_mitm_demo.DuckyDemo()


# uhh_ducky_mitm demonstration
@orchestration.route("/start/demo/uhh_ducky_mitm", methods=["POST", "GET"])
def start_demo_uhh_ducky_mitm():
    # secure_mode = flask.request.json["secureMode"]
    try:
        logging.info("Starting uhh_ducky_mitm demo stack")
        if (config.EnvironmentConfig.LANGUAGE == "de"):
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "uhh_ducky_mitm/native/stacks/docker-compose.yml")
        else:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "uhh_ducky_mitm/native/stacks/docker-compose-en.yml")
        orchestration_controller.orchestration_service \
            .wait_for_container("uhh_ducky_mitm_mailserver")
        ducky_service.start()
    except Exception as e:
        logging.error(e)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error), 500)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/uhh_ducky_mitm", methods=["POST", "GET"])
def stop_demo_uhh_ducky_mitm():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "uhh_ducky_mitm/native/stacks/docker-compose.yml")
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "uhh_ducky_mitm/native/stacks/docker-compose-en.yml")
    ducky_service.stop()
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/uhh_ducky_mitm", methods=["GET"])
def status_demo_uhh_ducky_mitm():
    if (config.EnvironmentConfig.LANGUAGE == "de"):
        result = orchestration_controller.orchestration_service \
            .get_status_docker_compose_file(
                "uhh_ducky_mitm/native/stacks/secure/docker-compose.yml")
    else:
        result = orchestration_controller.orchestration_service \
            .get_status_docker_compose_file(
                "uhh_ducky_mitm/native/stacks/secure/docker-compose-en.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/uhh_ducky_mitm/sum", methods=["GET"])
def status_demo_uhh_ducky_mitm_sum():
    result \
        = orchestration_controller.orchestration_service \
        .get_sum_status_docker_compose_file(
            "uhh_ducky_mitm/native/stacks/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/start/demo/uhh_ducky_mitm/stick", methods=["GET"])
def on_stick_insert():
    ducky_service.send_second_mail()

    return flask.helpers.make_response(flask.json.jsonify(1), 200)


@orchestration.route("/start/demo/uhh_ducky_mitm/script_downloaded",
                     methods=["GET"])
def on_script_downloaded():
    ducky_service.add_cert()
    ducky_service.send_second_mail()

    return flask.helpers.make_response(flask.json.jsonify(1), 200)
