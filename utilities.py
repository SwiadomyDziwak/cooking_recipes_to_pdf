from os import path, listdir
from tui import TUI, Option
from recipe import Recipe
from typing import Callable
from shortcuts import Key
import json
import actions
import recipe_utilities

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

def get_recipes(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Loads all saved recipes and associates them with a number for selection."""
    recipe_number: int = 1
    options: dict[str, Option] = {}
    for file in listdir("data"):
        if path.isdir(path.join("data", file)):
            # If path is dir, ignore
            continue
        if not file.endswith(".json"):
            # If path is not .json data, ignore
            continue

        # Load recipe data and set it in the Recipe class
        with open(path.join("data", file)) as f:
            recipe_data: str = json.load(f)
        recipe: Recipe = Recipe()
        recipe.set_dish_name(recipe_data["dish_name"])
        for tag in recipe_data["tags"]:
            recipe.add_tag(tag)
        recipe.set_servings(recipe_data["servings"])
        recipe.add_photo(recipe_data["photo"])
        for category, ingredients in recipe_data["ingredients"].items():
            recipe.add_ingredient_category(category)
            for ingredient, amount in ingredients.items():
                recipe.add_ingredient(category, ingredient, amount)
        for preparing_step in recipe_data["preparing_steps"]:
            recipe.add_preparing_step(preparing_step)

        # Add recipe to list and increase recipes number for the next loop
        options[str(recipe_number)] = Option(recipe.dish_name, recipe_utilities.select_recipe, recipe=recipe)
        recipe_number += 1

    options[Key.BACK.value] = Option(ui["back"], back, last_options=last_options)
    options[Key.QUIT.value] = Option(ui["quit"], quit_app, color="\033[91m", ui=ui, tui=tui)
    return options, []

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
