#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.install import install

import pathlib


def compile_locale(path, compiler):
    if path.is_dir():
        compiler.domain = ["base"]
        compiler.directory = path.absolute()
        compiler.run()


# CC-BY-SA:
# https://stackoverflow.com/questions/40051076/compile-translation-files-when-calling-setup-py-install # noqa: 501
class InstallWithCompile(install):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)

        for demo in pathlib.Path("demos").glob("*"):
            print(f"Compiling locale for {demo}")
            locale_dir = demo / "locales"
            compile_locale(locale_dir, compiler)

        compile_locale(pathlib.Path("native/nativeapp/utils/locale/locales"),
                       compiler)

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
