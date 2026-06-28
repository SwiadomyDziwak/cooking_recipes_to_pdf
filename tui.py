from os import path
import json

class TUI:
    def __init__(self, lang: str="pl") -> None:
        self.lang: str = lang
        self.ui: dict[str, str] = self._load_translations(lang)
        self.options: dict[str, str] = {
                "1": self.ui["ui_option_convert"],
                "2": self.ui["ui_option_new_recipe"],
                }

    def _load_translations(self, lang: str) -> dict[str, str]:
        # Reads a data/ui file for a selected language and loads ui translations
        filepath = path.join("data", "ui", lang) + ".json"
        with open(filepath) as translations_file:
            ui: dict[str, str] = json.load(translations_file)
        return ui

    def show_main_menu(self) -> None:
        for number, option in self.options.items():
            print(f"{number}. {option}")
