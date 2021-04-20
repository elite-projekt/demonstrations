from os import path
import subprocess

t_path = path.abspath(path.dirname(__file__))
stack_folder = path.join(path.dirname(path.dirname(t_path)), 'stacks',)


class OrchestrationService():

    def docker_compose_start_file(self, filename: str):
        file_path = path.join(stack_folder, filename)
        subprocess.run(['docker-compose', '-f', file_path, 'up',
                        '-d'], check=True, capture_output=True)

    def docker_compose_stop_file(self, filename: str):
        file_path = path.join(stack_folder, filename)
        subprocess.run(['docker-compose', '-f', file_path,
                        'down'], check=True, capture_output=True)
