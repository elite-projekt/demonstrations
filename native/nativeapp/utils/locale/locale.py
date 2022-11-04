import pathlib
import gettext
import logging

from collections.abc import Callable


class Locale():
    def __init__(self):
        self.locale_dirs = []
        self.translation = None
        self.add_locale_dir(pathlib.Path(__file__).parent / "locales")
        self.update_locale("en")

    def add_locale_dir(self, locale_dir: pathlib.Path):
        self.locale_dirs.append(pathlib.Path(locale_dir))

    def update_locale(self, language: str):
        for locale_dir in self.locale_dirs:
            try:
                translation = gettext.translation("base",
                                                  localedir=locale_dir.absolute(), # noqa: 501
                                                  languages=[language])
                if self.translation is None:
                    self.translation = translation
                else:
                    self.translation.add_fallback(translation)
            except Exception:
                logging.warn(f"Unable to load locale in dir {locale_dir}")

        if self.translation is None:
            self.translation = gettext.NullTranslations()
        self.translation.install()

    def get_translator(self) -> Callable[[str], str]:
        return self.translation.gettext

    def translate(self, text: str) -> str:
        return self.translation.gettext(text)
