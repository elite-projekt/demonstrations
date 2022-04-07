import logging

import flask

from native.src.controller import orchestration_controller
from demos.phishing.native import phishing_demo

phishing_service = phishing_demo.PhishingDemo()

orchestration = flask.Blueprint("phishing", __name__,
                                url_prefix="/orchestration/")


@orchestration.route("/start/demo/phishing", methods=["POST", "GET"])
def start_demo_phishing():
    secure_mode = flask.request.json["secureMode"]
    try:
        logging.info("Starting phishing demo stack")
        orchestration_controller.orchestration_service \
            .docker_compose_start_file(
                "phishing/native/stacks/docker-compose.yml")
    except Exception as e:
        logging.error(e)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error),
            500)

    try:
        phishing_service.thunderbird_init()
        phishing_service.check_mail_server_online()
        phishing_service.change_client_profile(secure_mode)
        phishing_service.delete_mailbox()
        phishing_service.send_mail_files(secure_mode)
        phishing_service.start_mail_application()
    except (ConnectionRefusedError, FileNotFoundError):
        logging.error(ConnectionRefusedError, FileNotFoundError)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_mail_server_error),
            500)
    except Exception as e:
        logging.error(e)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/phishing", methods=["POST", "GET"])
def stop_demo_phishing():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "phishing/native/stacks/docker-compose.yml")
    phishing_service.stop_mail_application()
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/phishing", methods=["GET"])
def status_demo_phishing():
    result = orchestration_controller.orchestration_service \
        .get_status_docker_compose_file(
            "phishing/native/stacks/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/phishing/sum", methods=["GET"])
def status_demo_phishing_sum():
    result = orchestration_controller.orchestration_service \
        .get_sum_status_docker_compose_file(
            "phishing/native/stacks/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)
