from argparse import ArgumentParser
from tui import TUI, Option
from shortcuts import Key, ERR
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
    tui.recipes = utilities.load_recipes()
    tui.add_option(Key.NEW.value, Option(ui["new_recipe"], recipe_utilities.create_recipe))
    tui.add_option(Key.RECIPES.value, Option(ui["show_recipes_list"], utilities.show_recipes))
    tui.add_option(Key.QUIT.value, Option(ui["quit"], utilities.quit_app, color="\033[91m"))
    tui.app_on = True

    # Main TUI loop
    WRONG_OPTION: str = (ERR, ui["invalid_choice"])

    while tui.app_on:

        tui.show()
        user_choice: str = input(f"{ui['select_option']}: ").lower()
        print()
        try:
            selection: Option = tui.options[user_choice]
            # Clear statuses only on successful choice
            tui.statuses.clear() 
        except KeyError:
            tui.add_status(WRONG_OPTION)
            continue

        tui.options, tui.statuses = selection.run(ui=ui, tui=tui)

if __name__ == "__main__":
    main()
