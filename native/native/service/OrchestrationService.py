from os import path
import subprocess
import logging
from config.config import EnvironmentConfig

t_path = EnvironmentConfig.WORKINGDIR
stack_folder = path.join(path.dirname(path.dirname(t_path)), 'stacks',)


class OrchestrationService():
    def docker_compose_start_file(self, filename: str):
        try:
            file_path = path.join(stack_folder, filename)
            subprocess.run(['docker-compose', '-f', file_path, 'up', '-d'], check=True, capture_output=True)
        except Exception as e:
            logging.error(e)

    def docker_compose_stop_file(self, filename: str):
        try:
            file_path = path.join(stack_folder, filename)
            logging.info(file_path)
            subprocess.run(['docker-compose', '-f', file_path, 'down'], check=True, capture_output=True)
        except Exception as e:
            logging.error(e)
