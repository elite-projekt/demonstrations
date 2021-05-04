from flask import Blueprint, request
from flask.helpers import make_response
from flask.json import jsonify
from service.OrchestrationService import OrchestrationService
from service.phishingdemo import PhishingDemo

from time import sleep

orchestration = Blueprint('orchestration', __name__,
                          url_prefix='/orchestration/')
orchestration_service = OrchestrationService()
phishing_service = PhishingDemo()

start_success = {'success': True, 'message': 'Successfully started the Demo.'}
stop_success = {'success': True, 'message': 'Stopped all remaining Demos.'}
no_docker_error = {'success': False,
                   'message': 'The workstation can not start the application!', 'code': 1}
no_mail_server_error = {'success': False,
                        'message': 'The mailserver is not reachable!', 'code': 2}


@orchestration.route('/start/demo/Phishing', methods=['POST', 'GET'])
def start_demo_phishing():
    secure_mode = request.json['secureMode']
    try:
        orchestration_service.docker_compose_start_file('phishing/docker-compose.yml')
    except Exception as e:
        return make_response(jsonify(no_docker_error), 500)

    try:
        phishing_service.check_mail_server_online()
        phishing_service.change_client_profile(secure_mode)
        phishing_service.delete_mailbox()
        phishing_service.send_mail_files()
    except (ConnectionRefusedError, FileNotFoundError):
        return make_response(jsonify(no_mail_server_error), 500)
    return make_response(jsonify(start_success), 201)


@orchestration.route('/stop/demo/Phishing', methods=['POST', 'GET'])
def stop_demo_phishing():
    orchestration_service.docker_compose_stop_file('phishing/docker-compose.yml')
    return make_response(jsonify(stop_success), 200)
