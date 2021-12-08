import logging

import flask

from native.src.service import OrchestrationService
from native.src.service import phishingdemo

orchestration = flask.Blueprint("orchestration", __name__,
                                url_prefix="/orchestration/")
orchestration_service = OrchestrationService.OrchestrationService()
phishing_service = phishingdemo.PhishingDemo()

start_success = {"success": True, "message": "Successfully started the Demo."}
stop_success = {"success": True, "message": "Stopped all remaining Demos."}
stop_failed = {"success": False, "message": "Failed to stop containers."}
no_docker_error = {
    "success": False,
    "message": "The workstation can not start the application!",
    "code": 1,
}
no_mail_server_error = {
    "success": False,
    "message": "The mailserver is not reachable!",
    "code": 2,
}


@orchestration.route("/start/demo/phishing", methods=["POST", "GET"])
def start_demo_phishing():
    secure_mode = flask.request.json["secureMode"]
    try:
        logging.info("Starting phishing demo stack")
        orchestration_service.docker_compose_start_file(
            "phishing/docker-compose.yml")
    except Exception as e:
        logging.error(e)
        return flask.helpers.make_response(flask.json.jsonify(no_docker_error),
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
            flask.json.jsonify(no_mail_server_error), 500)
    except Exception as e:
        logging.error(e)
    return flask.helpers.make_response(flask.json.jsonify(start_success), 201)


@orchestration.route("/stop/demo/phishing", methods=["POST", "GET"])
def stop_demo_phishing():
    orchestration_service.docker_compose_stop_file(
        "phishing/docker-compose.yml")
    phishing_service.stop_mail_application()
    return flask.helpers.make_response(flask.json.jsonify(stop_success), 200)


@orchestration.route("/start/demo/password", methods=["POST", "GET"])
def start_demo_password():
    secure_mode = flask.request.json["secureMode"]
    try:
        if secure_mode:
            orchestration_service.docker_compose_start_file(
                "password/secure/docker-compose.yml"
            )
        else:
            orchestration_service.docker_compose_start_file(
                "password/unsecure/docker-compose.yml"
            )
    except Exception:
        return flask.helpers.make_response(flask.json.jsonify(no_docker_error),
                                           500)
    return flask.helpers.make_response(flask.json.jsonify(start_success), 201)


@orchestration.route("/stop/demo/password", methods=["POST", "GET"])
def stop_demo_password():
    orchestration_service.docker_compose_stop_file(
        "password/secure/docker-compose.yml")
    orchestration_service.docker_compose_stop_file(
        "password/unsecure/docker-compose.yml"
    )
    return flask.helpers.make_response(flask.json.jsonify(stop_success), 200)


@orchestration.route("/status/demo/phishing", methods=["GET"])
def status_demo_phising():
    result = orchestration_service.get_status_docker_compose_file(
        "phishing/docker-compose.yml"
    )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/phishing/sum", methods=["GET"])
def status_demo_phising_sum():
    result = orchestration_service.get_sum_status_docker_compose_file(
        "phishing/docker-compose.yml"
    )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/password", methods=["GET"])
def status_demo_password():
    result = orchestration_service.get_status_docker_compose_file(
        "password/secure/docker-compose.yml"
    )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/password/sum", methods=["GET"])
def status_demo_password_sum():
    result = orchestration_service.get_sum_status_docker_compose_file(
        "password/secure/docker-compose.yml"
    )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)
