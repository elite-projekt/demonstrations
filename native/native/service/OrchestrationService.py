import logging
from os import path

import python_on_whales
import yaml

from native.native.config import config


class OrchestrationService:
    def docker_compose_start_file(self, filename: str):
        try:
            file_path = path.join(config.EnvironmentConfig.DOCKERSTACKDIR,
                                  filename)
            env_path = path.join(config.EnvironmentConfig.ENVDIR, ".env")
            docker = python_on_whales.DockerClient(compose_files=[file_path],compose_env_file=env_path)
            docker.compose.up(detach=True)
        except Exception as e:
            logging.error(e)

    def docker_compose_stop_file(self, filename: str):
        try:
            file_path = path.join(config.EnvironmentConfig.DOCKERSTACKDIR,
                                  filename)
            docker = python_on_whales.DockerClient(compose_files=[file_path])
            docker.compose.down()
        except Exception as e:
            logging.error(e)

    def get_status_docker_compose_file(self, filename: str):
        file_path = path.join(config.EnvironmentConfig.DOCKERSTACKDIR,
                              filename)
        container_name_list = []
        result = {}
        try:
            # Get Container Names from Compose File
            with open(file_path, "r") as file:
                compose_file = yaml.load(file, Loader=yaml.FullLoader)

                for k, v in compose_file["services"].items():
                    if "container_name" in compose_file["services"][k]:
                        container_name_list.append(
                            compose_file["services"][k]["container_name"]
                        )

                # The call is made here because it takes a very long time and
                # otherwise the call duration would only add up in the method
                # call.
                running_container_list = python_on_whales.docker.container\
                    .list(all).copy()

                for container_name in container_name_list:
                    state = self.get_state_specific_container(
                        container_name, running_container_list
                    )
                    result[container_name] = state

        except EnvironmentError:
            # parent of IOError, OSError *and* WindowsError where available
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
