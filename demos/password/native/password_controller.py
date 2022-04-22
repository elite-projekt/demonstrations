import flask

from nativeapp.controller import orchestration_controller

orchestration = flask.Blueprint("password", __name__,
                                url_prefix="/orchestration/")


@orchestration.route("/start/demo/password", methods=["POST", "GET"])
def start_demo_password():
    secure_mode = flask.request.json["secureMode"]
    try:
        if secure_mode:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "password/native/stacks/secure/docker-compose.yml")
        else:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "password/native/stacks/unsecure/docker-compose.yml")
    except Exception:
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error), 500)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/password", methods=["POST", "GET"])
def stop_demo_password():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "password/native/stacks/secure/docker-compose.yml")
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "password/native/stacks/unsecure/docker-compose.yml"
    )
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/password", methods=["GET"])
def status_demo_password():
    result = orchestration_controller.orchestration_service \
        .get_status_docker_compose_file(
            "password/native/stacks/secure/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/password/sum", methods=["GET"])
def status_demo_password_sum():
    result \
        = orchestration_controller.orchestration_service \
        .get_sum_status_docker_compose_file(
            "password/native/stacks/secure/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)
