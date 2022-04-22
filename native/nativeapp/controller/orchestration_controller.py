from nativeapp.service import orchestration_service

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
