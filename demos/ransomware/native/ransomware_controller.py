import flask
import logging
from demos.ransomware.native import ransomware_code

from nativeapp.controller import orchestration_controller
from demos.ransomware.native import ransomware_demo

ransomware_service = ransomware_demo.RansomwareDemo()


orchestration = flask.Blueprint("ransomware", __name__,
                                url_prefix="/orchestration/")


# ransomware demonstration
@orchestration.route("/start/demo/ransomware", methods=["POST", "GET"])
def start_demo_ransomware():
    secure_mode = flask.request.json["secureMode"]
    try:
        logging.info("Starting ransomware demo stack")
        orchestration_controller.orchestration_service \
            .docker_compose_start_file(
                "ransomware/native/stacks/docker-compose.yml")
    except Exception as e:
        logging.error(e)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error), 500)
    try:
        ransomware_code.prep()
        ransomware_service.thunderbird_init()
        ransomware_service.check_mail_server_online()
        ransomware_service.change_client_profile(secure_mode)
        ransomware_service.delete_mailbox()
        ransomware_service.start_mail_application()
        ransomware_service.send_mail_files(secure_mode)
    except (ConnectionRefusedError, FileNotFoundError):
        logging.error(ConnectionRefusedError, FileNotFoundError)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_mail_server_error),
            500)
    except Exception as e:
        logging.error(e)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/ransomware", methods=["POST", "GET"])
def stop_demo_ransomware():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "ransomware/native/stacks/docker-compose.yml")
    ransomware_service.stop_mail_application()
    ransomware_service.stop_excel_application()
    ransomware_code.reset()
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/ransomware", methods=["GET"])
def status_demo_ransomware():
    result = orchestration_controller.orchestration_service \
        .get_status_docker_compose_file(
            "ransomware/native/stacks/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/ransomware/sum", methods=["GET"])
def status_demo_ransomware_sum():
    result \
        = orchestration_controller.orchestration_service \
        .get_sum_status_docker_compose_file(
            "ransomware/native/stacks/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/run/demo/ransomware", methods=["POST", "GET"])
def run_demo_ransomware():
    ransomware_code.run()
    return flask.helpers.make_response(flask.json.jsonify(1), 200)
