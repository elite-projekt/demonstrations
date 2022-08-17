import flask

from nativeapp.controller import orchestration_controller

orchestration = flask.Blueprint("hda_password", __name__,
                                url_prefix="/orchestration/")


@orchestration.route("/start/demo/hda_password", methods=["POST", "GET"])
def start_demo_password():
    secure_mode = flask.request.json["secureMode"]
    try:
        if secure_mode:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "hda_password/native/stacks/secure/docker-compose.yml")
        else:
            orchestration_controller.orchestration_service \
                .docker_compose_start_file(
                    "hda_password/native/stacks/unsecure/docker-compose.yml")
    except Exception:
        return flask.helpers.make_response(
            flask.json.jsonify(orchestration_controller.no_docker_error), 500)
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.start_success), 201)


@orchestration.route("/stop/demo/hda_password", methods=["POST", "GET"])
def stop_demo_password():
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "hda_password/native/stacks/secure/docker-compose.yml")
    orchestration_controller.orchestration_service.docker_compose_stop_file(
        "hda_password/native/stacks/unsecure/docker-compose.yml"
    )
    return flask.helpers.make_response(
        flask.json.jsonify(orchestration_controller.stop_success), 200)


@orchestration.route("/status/demo/hda_password", methods=["GET"])
def status_demo_password():
    result = orchestration_controller.orchestration_service \
        .get_status_docker_compose_file(
            "hda_password/native/stacks/secure/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


@orchestration.route("/status/demo/hda_password/sum", methods=["GET"])
def status_demo_password_sum():
    result \
        = orchestration_controller.orchestration_service \
        .get_sum_status_docker_compose_file(
            "hda_password/native/stacks/secure/docker-compose.yml")

    if len(result) > 0:
        return flask.helpers.make_response(flask.json.jsonify(result), 200)
    else:
        flask.abort(500)


# import logging

# from nativeapp.controller import demo_controller

# class PasswordController(demo_controller.DemoController):
#     def init(self):
#         super().init("hda_password",
#                          "hda_password/native/stacks/secure/docker-compose.yml")

#     def start(self, subpath, params):
#         secure_mode = True
#         self.set_state("starting")
#         if "secureMode" in params:
#             secure_mode = params["secureMode"]
#         if secure_mode == True:
#             super().init("hda_password",
#                          "hda_password/native/stacks/secure/docker-compose.yml")
#         else:
#             super().init("hda_password",
#                          "hda_password/native/stacks/unsecure/docker-compose.yml")
#         try:
#             logging.info("Starting phishing demo stack")
#             self.start_container()
#         except Exception as e:
#             logging.error(e)
#             self.set_state("offline")
#             return demo_controller.ErrorCodes.no_docker_error
#         self.set_state("running")
#         return demo_controller.ErrorCodes.start_success

#     def stop(self, subpath):
#         self.set_state("stopping")
#         self.stop_container()
#         self.set_state("offline")
#         return demo_controller.ErrorCodes.stop_success

#     def get_controller():
#         return PasswordController()