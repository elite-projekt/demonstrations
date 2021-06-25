from os import path
import subprocess
import logging
from python_on_whales import docker
from python_on_whales import DockerClient
from config.config import EnvironmentConfig

#t_path = EnvironmentConfig.WORKINGDIR
#stack_folder = path.join(path.dirname(path.dirname(t_path)), 'stacks',)


class OrchestrationService():
    def docker_compose_start_file(self, filename: str):
        try:
            file_path = path.join(EnvironmentConfig.DOCKERSTACKDIR, filename)
            docker = DockerClient(compose_files=[file_path])
            docker.compose.up(detach=True)
        except Exception as e:
            logging.error(e)

    def docker_compose_stop_file(self, filename: str):
        try:
            file_path = path.join(EnvironmentConfig.DOCKERSTACKDIR, filename)
            # subprocess.run(['docker-compose', '-f', '"' + file_path + '"', 'down'], check=True, capture_output=True)
            docker = DockerClient(compose_files=[file_path])
            docker.compose.down()
        except Exception as e:
            logging.error(e)
