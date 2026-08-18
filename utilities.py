from os import path
from tui import TUI, Option
from recipe import Recipe
import json
import actions

def load_translation(lang: str) -> dict[str, str]:
    """Loads UI translations

    Args:
        lang: Name of the desired translations.

    Returns:
        ui: Dict of translations.
    """
    translation_file: str = lang + ".json"
    translation_file_path: str = path.join("data", "ui", translation_file)
    try:
        with open(translation_file_path) as f:
            ui: dict[str, str] = json.load(f)
    except:
        raise Exception("Translation file does not exists")
    return ui

def back(*, ui: dict[str, str], last_options: dict[str, Option], **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    status: list[tuple[str, str]] = []
    try:
        for s in kwargs["status_list"]:
            status.append(s)
    except KeyError:
        pass
    last_menu: dict[str, Option] = last_options.pop()
    return last_menu, status

def quit_app(*, ui: dict[str, str], tui: TUI, **kwargs) -> tuple[dict, list]:
    tui.app_on = False
    return {}, []
