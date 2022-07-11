import logging

import pathlib
import python_on_whales
import yaml
import sys
import time
import tempfile

from nativeapp.config import config

from typing import Dict

if sys.platform == "win32":
    DOCKER_CMD_LIST = ["wsl", "--user", "root", "docker"]
else:
    DOCKER_CMD_LIST = ["docker"]


def windows_to_wsl_path(path: pathlib.Path):
    return str(pathlib.Path(path).absolute()).replace("\\", "/").replace("C:", "/mnt/c/")  # noqa: 501


class OrchestrationService:
    def __init__(self):
        self.temp_env_file = tempfile.NamedTemporaryFile()

    def _get_demo_path(self):
        return pathlib.Path(config.EnvironmentConfig.WORKINGDIR) / "demos"

    def get_docker_client(self):
        return python_on_whales.DockerClient(client_call=DOCKER_CMD_LIST)

    def docker_compose_start_file(self, filename: str,
                                  additional_env: Dict[str, str] = {}):
        try:
            # get demo name from first word in path: "password/native/(...)"
            # FIXME
            demo_name = filename.split("/")[0]
            file_path = self._get_demo_path() / filename
            env_path = pathlib.Path(config.EnvironmentConfig.ENVDIR) \
                / ".env"
            self.temp_env_file.file.seek(0)
            self.temp_env_file.file.truncate()
            with open(env_path, "r") as orig_env:
                self.temp_env_file.file.write(orig_env.read().encode())
            for key, val in additional_env.items():
                self.temp_env_file.file.write(f"{key}='{val}'".encode())
            self.temp_env_file.file.flush()

            # we need posix paths for "wsl docker"
            docker = python_on_whales.DockerClient(
                client_call=DOCKER_CMD_LIST,
                compose_files=[windows_to_wsl_path(file_path)],
                compose_env_file=windows_to_wsl_path(self.temp_env_file.name),
                compose_project_name=demo_name)
            docker.compose.up(detach=True)
        except Exception as e:
            logging.error(e)
            raise

    def docker_compose_stop_file(self, filename: str):
        try:
            # get demo name from first word in path: "password/native/(...)"
            # FIXME
            demo_name = filename.split("/")[0]
            file_path = self._get_demo_path() / filename
            docker = python_on_whales.DockerClient(
                client_call=DOCKER_CMD_LIST,
                compose_files=[file_path.as_posix()],
                compose_project_name=demo_name)
            docker.compose.down()
        except Exception as e:
            logging.error(e)
            raise

    def get_status_docker_compose_file(self, filename: str):
        file_path = self._get_demo_path() / filename
        container_name_list = []
        result = {}
        try:
            # Get Container Names from Compose File
            with open(file_path, "r") as file:
                compose_file = yaml.safe_load(file)

                for k, v in compose_file["services"].items():
                    if "container_name" in compose_file["services"][k]:
                        container_name_list.append(
                            compose_file["services"][k]["container_name"]
                        )

                # The call is made here because it takes a very long time and
                # otherwise the call duration would only add up in the method
                # call.
                running_container_list = self.get_docker_client().container\
                    .list(all).copy()

                for container_name in container_name_list:
                    state = self.get_state_specific_container(
                        container_name, running_container_list
                    )
                    result[container_name] = state

        except Exception as e:
            # parent of IOError, OSError *and* WindowsError where available
            logging.error(e)
            logging.error(sys.exc_info()[0])
            return result

        return result

    def get_sum_status_docker_compose_file(self, filename: str):
        container_states = self.get_status_docker_compose_file(filename)
        result = {}
        if len(container_states) == 0:
            return result
        else:
            result = {}

            if len(container_states) == sum(
                    value == "running" for value in container_states.values()
            ):
                result["state"] = "running"
            else:
                result["state"] = "offline"
        return result

    def get_state_specific_container(self, containername: str,
                                     running_container_list):
        result = "not found"

        for running_container in running_container_list:
            if running_container.name == containername:
                result = running_container.state.status

        return result

    # Wait for a container to start
    def wait_for_container(self, name, timeout_ms=10000, check_delay_ms=1000):
        """Checks if the mailserver docker container is up"""
        current_wait = 0
        try:
            container = self.get_docker_client().container.inspect(
                name)
            while current_wait < timeout_ms:
                logging.info(
                   f"Checking if container {name} is running")
                if container.state.running:
                    time.sleep(5)
                    return
                time.sleep(check_delay_ms)
                current_wait += check_delay_ms
        except Exception as e:
            logging.error(e)
