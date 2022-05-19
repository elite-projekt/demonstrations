import flask
import logging
from nativeapp.controller import orchestration_controller
from demos.fokusrnware.native import fokusrnware_demo

orchestration = flask.Blueprint("fokusrnware", __name__,
                                url_prefix="/orchestration/")

fokusrnware_service = fokusrnware_demo.fokusrnwareDemo()


# fokusrnware demonstration
@orchestration.route("/start/demo/fokusrnware", methods=["POST", "GET"])
def start_demo_fokusrnware():
    secure_mode = flask.request.json["secureMode"]
    try:
        logging.info("Starting phishing demo stack")
        orchestration_controller.orchestration_service \
            .docker_compose_start_file(
                "fokusrnware/native/stacks/docker-compose.yml")
    except Exception as e:
        logging.error(e)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error),
            500)

    try:
        fokusrnware_service.create_desktop_files()
        fokusrnware_service.thunderbird_init()
        fokusrnware_service.check_mail_server_online()
        fokusrnware_service.change_client_profile(secure_mode)
        fokusrnware_service.delete_mailbox()
        fokusrnware_service.send_mail_files(secure_mode)
        fokusrnware_service.start_mail_application()
    except (ConnectionRefusedError, FileNotFoundError):
        logging.error(ConnectionRefusedError, FileNotFoundError)
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_mail_server_error),
            500)
    except Exception as e:
        logging.error(e)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)
    '''try:
        if secure_mode:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "fokusrnware/native/stacks/secure/docker-compose.yml")
        else:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "fokusrnware/native/stacks/unsecure/docker-compose.yml")
    except Exception:
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error), 500)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)'''


@orchestration.route("/stop/demo/fokusrnware", methods=["POST", "GET"])
def stop_demo_fokusrnware():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "fokusrnware/secure/docker-compose.yml")
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "fokusrnware/unsecure/docker-compose.yml")
    fokusrnware_service.reset()
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/fokusrnware", methods=["GET"])
def status_demo_fokusrnware():
    result = orchestration_controller.orchestration_service \
        .get_status_docker_compose_file(
            "fokusrnware/secure/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/fokusrnware/sum", methods=["GET"])
def status_demo_fokusrnware_sum():
    result \
        = orchestration_controller.orchestration_service \
        .get_sum_status_docker_compose_file(
            "fokusrnware/secure/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/run/prog", methods=["GET"])
def run_prog():
    # subprocess.Popen(["taskkill", "/f", "/im", "chrome.exe"], shell = True)
    fokusrnware_service.exec_rnsm()
