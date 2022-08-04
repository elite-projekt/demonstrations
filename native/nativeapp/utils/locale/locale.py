import pathlib
import gettext

from collections.abc import Callable


class Locale():
    def __init__(self, locale_dir: pathlib.Path):
        self.locale_dir = pathlib.Path(locale_dir)
        self.update_locale("en")

    def update_locale(self, language: str):
        self.translation = gettext.translation("base",
                                               localedir=self.locale_dir.absolute(), # noqa: 501
                                               languages=[language])
        self.translation.install()

    def get_translator(self) -> Callable[[str], str]:
        return self.translation.gettext

    def translate(self, text: str) -> str:
        return self.translation.gettext(text)
