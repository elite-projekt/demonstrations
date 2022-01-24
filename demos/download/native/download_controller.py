import flask
import time

from native.src.controller import orchestration_controller
from demos.download.native import download_demo

orchestration = flask.Blueprint("download", __name__,
                                url_prefix="/orchestration/")


# download demonstration
@orchestration.route("/start/demo/download", methods=["POST", "GET"])
def start_demo_download():
    secure_mode = flask.request.json["secureMode"]
    try:
        print("start demo")
        download_demo.DownloadDemo.firefox_init()
        print("init success")
        if secure_mode:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                 "download/secure/docker-compose.yml"
                )
            # sleep until container app is ready
            time.sleep(5)
            download_demo.DownloadDemo.start_web_browser(True)
        else:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                 "download/unsecure/docker-compose.yml"
                )
            # sleep until container app is ready
            time.sleep(5)
            download_demo.DownloadDemo.start_web_browser(False)
    except Exception:
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error),
            500)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/download", methods=["POST", "GET"])
def stop_demo_download():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "download/secure/docker-compose.yml")
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "download/unsecure/docker-compose.yml"
    )
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/download", methods=["GET"])
def status_demo_download():
    result = orchestration_controller.orchestration_service \
        .get_status_docker_compose_file(
         "download/secure/docker-compose.yml"
        )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/download/sum", methods=["GET"])
def status_demo_download_sum():
    result = orchestration_controller.orchestration_service\
        .get_sum_status_docker_compose_file(
         "download/secure/docker-compose.yml"
        )

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/download/create_fake_malware", methods=["POST"])
def create_fake_malware():
    download_demo.DownloadDemo.create_fake_malware()
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.fake_malware_success), 200)
