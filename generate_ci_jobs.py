#!/usr/bin/env python3

import pathlib
import json


class PipelineTemplate:
    def __init__(self, demo_name, job_name, image="alpine"):
        self.image = image
        self.demo_name = demo_name
        self.job_name = job_name
        self.commands = []
        self.dependencies = []
        self.entrypoint = None
        self.before_script_commands = []
        self.artifacts = []
        self.allow_failure = False
        self.stage = None

    def add_command(self, command):
        self.commands.append(command)

    def add_before_script_command(self, command):
        self.before_script_commands.append(command)

    def add_dependency(self, name):
        self.dependencies.append(name)

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def generate(self):
        output_data = ""
        output_data += f"{self.job_name}-{self.demo_name}:\n"
        output_data += "  image:\n"
        output_data += f"    name: {self.image}\n"
        if self.entrypoint is not None:
            output_data += f"    entrypoint: [\"{self.entrypoint}\"]\n"
        if self.allow_failure:
            output_data += "  allow_failure: true\n"
        output_data += "  script:\n"
        for command in self.commands:
            output_data += f"    - {command}\n"
        if len(self.dependencies) > 0:
            output_data += "  needs:\n"
            for dep in self.dependencies:
                output_data += f"    - job: {dep}\n"
        if len(self.before_script_commands) > 0:
            output_data += "  before_script:\n"
            for cmd in self.before_script_commands:
                output_data += f"    - {cmd}\n"
        if self.stage is not None:
            output_data += f"  stage: {self.stage}\n"
        if len(self.artifacts) > 0:
            output_data += "  artifacts:\n"
            output_data += "    paths:\n"
            for artifact in self.artifacts:
                output_data += f"      - {artifact}\n"

        return output_data


def get_demos():
    demo_dirs = pathlib.Path(__file__).parent / "demos"
    demo_dirs = demo_dirs.glob("*")
    demo_settings = {}
    demos = []
    for demo_dir in demo_dirs:
        demo_json_path = demo_dir / "demo.json"
        if demo_json_path.exists():
            with open(demo_json_path, "r") as json_file:
                json_data = json.loads(json_file.read())
                demo_settings[demo_dir.name] = {}
                if "isAvailable" in json_data:
                    # Skip if it is not available
                    if not json_data["isAvailable"]:
                        continue
            demos.append(demo_dir)
    return demos


def generate_license_ci():
    demos = get_demos()
    print(f"{demos}")
    output_data = ""
    for demo in demos:
        template = PipelineTemplate(demo.name, "license-check")
        template.add_command("apk update && apk add python3")
        template.add_command(f"python3 check_license.py -f demos/{demo.name}")
        output_data += template.generate()
    with open("generated_license_ci.yml", "w") as f:
        f.write(output_data)


def generate_docker_lint_ci():
    demos = get_demos()
    demo_data = ""
    for demo in demos:
        container_info_file = demo / "demo.json"
        if container_info_file.exists():
            with open(container_info_file, "r") as container_info_file:
                json_data = json.loads(container_info_file.read())
            if "container" not in json_data:
                continue
            for container in json_data["container"]:
                # lint job
                name = container["name"]
                template = PipelineTemplate(name, "lint:dockerfile", image="registry.gitlab.com/pipeline-components/hadolint") # noqa: 501
                dockerfile = container["dockerfile"]
                demo_path = pathlib.Path(dockerfile).parent
                template.add_command(f"hadolint \"$CI_PROJECT_DIR/demos/{demo.name}/{dockerfile}\"") # noqa: 501
                template.stage = "lint"
                demo_data += template.generate()
                # build job
                template = PipelineTemplate(name, "build:image", image="gcr.io/kaniko-project/executor:debug") # noqa: 501
                template.entrypoint = ""
                template.add_command(f"image_name=\"$CI_REGISTRY_IMAGE/{name}:$CI_COMMIT_BRANCH\"") # noqa: 501
                template.add_command(f"/kaniko/executor --context \"$CI_PROJECT_DIR/demos/{demo.name}/{demo_path}\" --dockerfile \"$CI_PROJECT_DIR/demos/{demo.name}/{dockerfile}\" --no-push --destination \"$image_name\" --tarPath {name}.tar") # noqa: 501
                template.add_before_script_command("mkdir -p /kaniko/.docker")
                template.add_before_script_command("echo \"{'auths':{'$CI_REGISTRY':{'username':'$CI_REGISTRY_USER','password':'$CI_REGISTRY_PASSWORD'}}}\" > /kaniko/.docker/config.json".replace("'", "\\\"")) # noqa: 501
                template.add_before_script_command("cat /kaniko/.docker/config.json") # noqa: 501
                template.add_artifact(f"{name}.tar")
                template.add_dependency(f"lint:dockerfile-{name}")
                template.stage = "build"
                demo_data += template.generate()
                # scan job
                template = PipelineTemplate(name, "scan:image", image="aquasec/trivy:latest") # noqa: 501
                template.entrypoint = ""
                template.add_command(f"trivy --cache-dir .trivycache/ image -s HIGH,CRITICAL --security-checks vuln --exit-code 1 --no-progress --ignore-unfixed --input {name}.tar") # noqa: 501
                template.add_dependency(f"build:image-{name}")
                template.stage = "scan"
                demo_data += template.generate()

                # push job
                template = PipelineTemplate(name, "push:image", image="gcr.io/go-containerregistry/crane:debug") # noqa: 501
                template.entrypoint = ""
                template.add_command("crane auth login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY") # noqa: 501
                template.add_command(f"crane push {name}.tar $CI_REGISTRY_IMAGE/{name}:$CI_COMMIT_BRANCH") # noqa: 501
                template.add_dependency(f"build:image-{name}")
                template.stage = "push"
                demo_data += template.generate()

                print(container)

    with open("generated_demo_ci.yml", "w") as f:
        if demo_data == "":
            f.write("dummy-job:\n")
            f.write("  script:\n")
            f.write("  - echo 'dummy'\n")
        else:
            f.write("stages:\n")
            f.write("  - lint\n")
            f.write("  - build\n")
            f.write("  - scan\n")
            f.write("  - push\n")
            f.write(demo_data)


if __name__ == "__main__":
    generate_license_ci()
    generate_docker_lint_ci()
