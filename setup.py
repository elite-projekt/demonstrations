#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.install import install

import pathlib


# CC-BY-SA:
# https://stackoverflow.com/questions/40051076/compile-translation-files-when-calling-setup-py-install # noqa: 501
class InstallWithCompile(install):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)

        for demo in pathlib.Path("demos").glob("*"):
            locale_dir = demo / "locales"
            if locale_dir.is_dir():
                print(f"Compiling locale for {demo}")
                compiler.domain = ["base"]
                compiler.directory = locale_dir.absolute()
                compiler.run()

        super().run()


setup(
    packages=find_packages(where="native") +
    find_packages(),
    package_dir={
        "": "native",
        "demos": "demos"
    },
    cmdclass={
            'install': InstallWithCompile,
        },
)
