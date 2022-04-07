# NativeApp

This component is installed on every workstation. It presents an HTTP-based API. Everything that requires operations on the Windows host directly lives inside this component.

## Setup

Please look into the Wiki!

## Platform Integration

We start containers using `docker-compose`. The command is executed using pythons `subprocess` module. All orchestration related stuff can be found in the `OrchestrationService` class. The endpoints that use the service are defined in the `orchestartion.py` file in the `controller` subfolder.

There will always be endpoints for starting and stopping a demo. For example: `/orchestration/start/demo/Phishing` and `/orchestration/start/demo/Phishing`.
