import tempfile
import pathlib
import tarfile
import sys

from subprocess import Popen, PIPE  # nosec
from setuptools import setup, find_packages

from typing import List


WSL_PATCH = """
--- a/python_on_whales/client_config.py
+++ b/python_on_whales/client_config.py
@@ -85,7 +85,7 @@ class ClientConfig:
     @property
     def docker_cmd(self) -> Command:

-        result = Command([self.get_docker_path()])
+        result = Command(["wsl", "--user", "root", "docker"])

         if self.config is not None:
             result += ["--config", self.config]
"""

PYTHON_EXE = sys.executable


def call_cmd(command_list: List[str], workdir: pathlib.Path):
    with Popen(  # nosec
            command_list, stdout=PIPE, cwd=workdir) as process:
        process.communicate()


def install_patched_pow():
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = pathlib.Path(tmpdirname)
        # Download python on whales
        call_cmd([f"{PYTHON_EXE}",
                  "-m", "pip", "download",
                  "--no-deps", "--no-binary", ":all:", "python-on-whales"],
                 tmpdir)
        call_cmd([f"{PYTHON_EXE}", "-m", "pip", "install", "patch"], tmpdir)
        tar_files = list(tmpdir.glob("*.tar.gz"))
        if len(tar_files) != 1:
            print("ERROR while downloading dependencies")
            sys.exit(1)
        tar_file = tar_files[0]

        with tarfile.open(tar_file) as tar:
            tar.extractall(path=tmpdir)
        pow_folder = tmpdir / pathlib.Path(tar_file.stem).stem

        if not pow_folder.exists():
            print("ERROR while extracting python on whales")
            sys.exit(1)

        with open(pow_folder / "wsl.patch", "w") as patch_file:
            patch_file.write(WSL_PATCH)
        call_cmd([f"{PYTHON_EXE}", "-m", "patch", "wsl.patch"], pow_folder)
        call_cmd([f"{PYTHON_EXE}", "-m", "pip", "install", "-I", "."],
                 pow_folder)


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
