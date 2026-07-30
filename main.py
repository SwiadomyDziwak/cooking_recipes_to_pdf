from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe, AppError
import json
from argparse import ArgumentParser
from os import path, listdir
from tui import TUI, Option
import actions
from shortcuts import Key

ERR: str = "\033[91m[ \u2718 ]\033[0m"
INFO: str = "\033[96m[i]\033[0m"

def main() -> None:

    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-l", "--lang", action="store", choices=["pl", "en"], default="en")

    args = parser.parse_args()

    # Load User Interface translations
    ui: dict[str, str] = actions.load_translation(args.lang)

    # Define and populate Text User Interface
    tui: TUI = TUI()
    tui.add_option(Key.RECIPES.value, Option(ui["show_recipes_list"], actions.get_recipes))
    tui.add_option(Key.QUIT.value, Option(ui["quit"], actions.quit_app, tui=tui))
    tui.app_on = True
    prev_options: list[dict[str, Option]] = []

    # Main TUI loop
    WRONG_OPTION: str = f"{ERR} {ui['invalid_choice']}"
    SEPARATOR: str    = "\033[94m----------\033[0m"

    while tui.app_on:

        print(SEPARATOR)
        tui.show_status()
        tui.show_options()
        user_choice: str = input(f"{ui['select_option']}: ").lower()
        try:
            selection: Option = tui.options[user_choice]
        except KeyError:
            print(WRONG_OPTION)
            continue

        if user_choice != Key.BACK.value:
            prev_options.append(tui.options)

        tui.options = selection.run()
        if prev_options:
            tui.add_option(Key.BACK.value, Option(ui["back"], actions.back, last_options=prev_options))
        else:
            tui.add_option(Key.QUIT.value, Option(ui["quit"], actions.quit_app, tui=tui))

if __name__ == "__main__":
    main()
