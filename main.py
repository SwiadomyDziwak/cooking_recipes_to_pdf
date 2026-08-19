from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe, AppError
from argparse import ArgumentParser
from os import path, listdir
from tui import TUI, Option
from shortcuts import Key, INF, ERR, OK
import json
import actions
import utilities
import recipe_utilities

def main() -> None:

    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-l", "--lang", action="store", choices=["pl", "en"], default="en")

    args = parser.parse_args()

    # Load User Interface translations
    ui: dict[str, str] = utilities.load_translation(args.lang)

    # Define and populate Text User Interface
    tui: TUI = TUI()
    tui.add_option(Key.NEW.value, Option(ui["new_recipe"], recipe_utilities.create_recipe, ui=ui, tui=tui))
    tui.add_option(Key.RECIPES.value, Option(ui["show_recipes_list"], utilities.get_recipes))
    tui.add_option(Key.QUIT.value, Option(ui["quit"], utilities.quit_app, color="\033[91m", tui=tui))
    tui.app_on = True
    prev_options: list[dict[str, Option]] = []

    # Main TUI loop
    WRONG_OPTION: str = (ERR, ui["invalid_choice"])

    while tui.app_on:

        tui.show()
        user_choice: str = input(f"{ui['select_option']}: ").lower()
        print()
        try:
            selection: Option = tui.options[user_choice]
            # Clear statuses only on successful choice
            # Else recipe's name dissappears from it even when recipe is selected
            tui.statuses.clear() 
        except KeyError:
            tui.add_status(WRONG_OPTION)
            continue

        # Prevents setting "back" option on infinite loop
        if user_choice != Key.BACK.value:
            prev_options.append(tui.options)

        tui.options, statuses = selection.run(ui=ui, last_options=prev_options, tui=tui)
        for status in statuses:
            tui.add_status(status)

if __name__ == "__main__":
    main()
