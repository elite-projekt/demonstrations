## Native Access

This component is installed on every workstation. It presents an HTTP-based API. Everything that requires operations on the windows host directly lives inside this component.

## Setup

### Under Windows
```bash
cd native
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd native\

#For Development Config
python -m app dev

#For Production Config
python -m app prod

```

### Under Linux
```bash
cd native
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app/

#For Development Config
python -m app dev

#For Production Config
python -m app prod

```

## Platform Integration

We start containers using `docker-compose`. The command is executed using pythons `subprocess` module. All orchestration related stuff can be found in the `OrchestrationService` class. The endpoints that use the service are defined in the `orchestartion.py` file in the `controller` subfolder.

There will always be endpoints for starting and stopping a demo. For example: `/orchestration/start/demo/Phishing` and `/orchestration/start/demo/Phishing`.
