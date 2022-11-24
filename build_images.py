#!/usr/bin/env python3

import pathlib
import json

import subprocess

script_dir = pathlib.Path(__file__).parent
print(script_dir)


def build_image(path, dockerfile, name):
    build_script = script_dir / "build_image.sh"
    p = subprocess.Popen(["/bin/bash", build_script,
                          "-c", path,
                          "-d", dockerfile,
                          "-i", name,
                          "-u",
                          "-p"])
    p.communicate()


container_jsons = (script_dir / "demos").glob("**/demo.json")

for container_json in container_jsons:
    print(container_json)
    with open(container_json, "r") as json_file:
        json_data = json.loads(json_file.read())
        if "container" in json_data:
            for demo in json_data["container"]:
                dockerfile = pathlib.Path(demo["dockerfile"])
                p = container_json.parent / dockerfile.parent
                name = demo["name"]
                build_image(p, dockerfile.name, name)
