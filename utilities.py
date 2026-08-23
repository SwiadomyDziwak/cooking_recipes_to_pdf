from os import path, listdir
from tui import TUI, Option
from recipe import Recipe
from shortcuts import Key, RecipeFlags
from datatypes import MenuOptions, StatusList, UIResult
import json
import exports
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

def main_menu(*, ui: dict[str, str], tui: TUI) -> UIResult:
    options = {
            Key.NEW.value: Option(ui["new_recipe"], recipe_utilities.create_recipe),
            Key.RECIPES.value: Option(ui["show_recipes_list"], show_recipes),
            Key.QUIT.value: Option(ui["quit"], quit_app, color="\033[91m")
            }
    status = []
    return options, status

def load_recipes() -> list[Recipe]:
    recipes: list[Recipe] = []
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

        # Add recipe to the list
        recipes.append(recipe)

    return recipes

def show_recipes(*, ui: dict[str, str], tui: TUI, **kwargs) -> UIResult:
    options: MenuOptions = {}
    option_no: int = 1
    for recipe in tui.recipes:
        options[str(option_no)] = Option(recipe.dish_name, recipe_utilities.select_recipe, recipe=recipe)
        option_no += 1

    options[Key.BACK.value] = Option(ui["back"], main_menu)
    options[Key.QUIT.value] = Option(ui["quit"], quit_app, color="\033[91m")
    
    status: StatusList = []
    return options, status

def quit_app(*, ui: dict[str, str], tui: TUI, **kwargs) -> UIResult:
    message: str = f"{ui['ask_quit_unsaved']} ({Key.YES.value}/{Key.NO.value})"
    new_recipe_found: bool = False
    for recipe in tui.recipes:
        if recipe.flags & RecipeFlags.EDITED.value:
            new_recipes_found = True
            break

    if new_recipe_found:
        decision: str = input(f"{message} ")
        if decision.lower() == Key.YES.value:
            tui.app_on = False
        else:
            options, status = main_menu(ui=ui, tui=tui)
            return options, status
    tui.app_on = False
    return {}, []
