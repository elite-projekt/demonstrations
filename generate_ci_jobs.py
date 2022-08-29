#!/usr/bin/env python3

import pathlib


class PipelineTemplate:
    def __init__(self, demo_name, job_name, image="alpine"):
        self.image = image
        self.demo_name = demo_name
        self.job_name = job_name
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def generate(self):
        output_data = ""
        output_data += f"{self.job_name}-{self.demo_name}:\n"
        output_data += f"  image: {self.image}\n"
        output_data += "  allow_failure: true\n"
        output_data += "  script:\n"
        for command in self.commands:
            output_data += f"    - {command}\n"
        return output_data


demos = (pathlib.Path(__file__).parent / "demos").glob("*")
demos = [x for x in demos if x.is_dir() and "__pycache__" not in x.name]

output_data = ""
for demo in demos:
    template = PipelineTemplate(demo.name, "license-check")
    template.add_command("apk update && apk add python3")
    template.add_command(f"python3 check_license.py -f demos/{demo.name}")
    output_data += template.generate()

with open("generated_ci.yml", "w") as f:
    f.write(output_data)
