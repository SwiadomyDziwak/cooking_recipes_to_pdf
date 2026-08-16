from os import path, listdir
import json
from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
from tui import Option, TUI
from typing import Any
from shortcuts import Key, ERR, INF, OK
import utilities
import recipe_utilities

def generate_pdf(*, ui: dict[str, str], recipe: Recipe, last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    """Generates and creates a PDF file for passed in recipe

    Kwargs:
        ui: A dict containing UI translations.
        recipe: A Recipe object containing all necessary data.
        last_options: A dict containing shortcut-Option pair to be able to use "Back" option.
        tui: A TUI object, required for the "Quit" option to function properly.

    Returns:
        A pair (tuple) containing:
            options: A dict of previously used shortcut-Option pair.
            status_list: A list of symbol-message tuple to display statuses
    """

    # Set output file's details
    output_file: str = recipe.dish_name.replace(" ", "_").lower() + ".pdf"
    output_path: str = path.join("pdfs", output_file)

    # Set template and render the PDF
    template_path: str = path.join("templates", "cooking1.html")
    style_path: str = path.join("templates", "cooking1.css")
    with open(path.join(template_path)) as t:
        template: Template = Template(t.read())
    html: str = template.render(recipe=recipe, ui=ui)
    HTML(string=html).write_pdf(
            output_path,
            stylesheets=[CSS(style_path)]
            )

    options, status_list = select_recipe(ui=ui, recipe=recipe, last_options=last_options[:-1], tui=tui)
    status_list.append((OK, ui["pdf_generated"]))
    return options, status_list

def get_recipes(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
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
        options[str(recipe_number)] = Option(recipe.dish_name, select_recipe, recipe=recipe)
        recipe_number += 1

    options[Key.BACK.value] = Option(ui["back"], utilities.back, last_options=last_options)
    options[Key.QUIT.value] = Option(ui["quit"], utilities.quit_app, color="\033[91m", ui=ui, tui=tui)
    return options, []

def select_recipe(*, ui: dict[str, str], recipe: Recipe, last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    # Display recipe's info here
    recipe.show_info(ui=ui)

    # Set available options
    recipe_options: dict[str, Option] = {
            Key.GENERATE.value: Option(ui["generate_pdf"], generate_pdf, recipe=recipe),
            Key.ADD_SERVINGS.value: Option(ui["servings"], recipe_utilities.set_servings, recipe=recipe),
            Key.TAG_OPTIONS.value: Option(ui["edit_tags"], recipe_utilities.edit_tags, recipe=recipe),
            Key.BACK.value: Option(ui["back"], utilities.back, last_options=last_options),
            Key.QUIT.value: Option(ui["quit"], utilities.quit_app, color="\033[91m", ui=ui, tui=tui)
            }
    return recipe_options, [(INF, recipe.dish_name)]
