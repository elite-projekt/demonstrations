import pathlib
import sys

from subprocess import Popen, PIPE  # nosec
from setuptools import setup, find_packages

from typing import List

PYTHON_EXE = sys.executable
PIP_URL = r"git+https://gitlab.com/kevin.koester/python_on_whales"


def call_cmd(command_list: List[str], workdir: pathlib.Path = None):
    print(command_list)
    with Popen(  # nosec
            command_list, stdout=PIPE, cwd=workdir) as process:
        process.communicate()


def install_patched_pow():
    call_cmd([f"{PYTHON_EXE}", "-m", "pip", "install", PIP_URL])


if sys.platform == "win32":
    install_patched_pow()

setup(
    packages=find_packages(where="native") +
    find_packages(),
    package_dir={
        "": "native",
        "demos": "demos"

    }
)
