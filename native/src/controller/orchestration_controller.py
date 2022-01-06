from native.src.service import orchestration_service
from native.src.service.download_demo import download_demo

orchestration_service = orchestration_service.OrchestrationService()

start_success = {
    "success": True,
    "message": "Successfully started the Demo."
}
stop_success = {
    "success": True,
    "message": "Stopped all remaining Demos."
}
stop_failed = {
    "success": False,
    "message": "Failed to stop containers."
}
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

# download demonstration
@orchestration.route("/start/demo/download", methods=["POST", "GET"])
def start_demo_download():
    secure_mode = flask.request.json["secureMode"]
    try:
        if secure_mode:
            orchestration_service.docker_compose_start_file(
                "download/secure/docker-compose.yml"
            )
        else:
            orchestration_service.docker_compose_start_file(
                "download/unsecure/docker-compose.yml"
            )
    except Exception:
        return flask.helpers.make_response(flask.json.jsonify(no_docker_error),
                                           500)
    return flask.helpers.make_response(flask.json.jsonify(start_success), 201)


@orchestration.route("/stop/demo/download", methods=["POST", "GET"])
def stop_demo_download():
    orchestration_service.docker_compose_stop_file(
        "download/secure/docker-compose.yml")
    orchestration_service.docker_compose_stop_file(
        "download/unsecure/docker-compose.yml"
    )
    return flask.helpers.make_response(flask.json.jsonify(stop_success), 200)


@orchestration.route("/status/demo/download", methods=["GET"])
def status_demo_download():
    result = orchestration_service.get_status_docker_compose_file(
        "download/secure/docker-compose.yml"
    )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/download/sum", methods=["GET"])
def status_demo_download_sum():
    result = orchestration_service.get_sum_status_docker_compose_file(
        "download/secure/docker-compose.yml"
    )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/download/create_fake_malware", methods=["POST"])
def create_fake_malware():
    download_demo.create_fake_malware()
    return flask.helpers.make_response(
        flask.json.jsonify(fake_malware_success), 200)
