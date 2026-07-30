from os import path, listdir
import json
from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
from tui import Option, TUI
from typing import Any

def get_recipes_list() -> list[str]:
    recipes_list = []
    for file in listdir("data"):
        if path.isdir(path.join("data", file)):
            continue
        if not file.endswith(".json"):
            continue
        recipes_list.append(file)
    return recipes_list

def load_translation(lang: str) -> dict[str, str]:
    translation_file: str = lang + ".json"
    translation_file_path: str = path.join("data", "ui", translation_file)
    try:
        with open(translation_file_path) as f:
            ui: dict[str, str] = json.load(f)
    except:
        raise Exception("Translation file does not exists")
    return ui

def generate_pdf(ui: dict[str, str], recipe_file: str) -> None:
    # Receives target file's name and load recipe's data
    # Then renders finished PDF file

    # Set recipe's propeties
    recipe: Recipe = Recipe()
    with open(path.join("data", recipe_file)) as f:
        recipe_data: dict[str, any] = json.load(f)
    recipe.dish_name = recipe_data["dish_name"]
    recipe.photo = path.abspath(path.join("data", recipe_data["photo"]))
    for tag in recipe_data["tags"]:
        recipe.add_tag(tag)
    recipe.set_servings(recipe_data["servings"])
    for category, ingredients in recipe_data["ingredients"].items():
        recipe.add_ingredient_category(category)
        for ingredient, amount in ingredients.items():
            recipe.add_ingredient(category, ingredient, amount)
    for preparing_step in recipe_data["preparing_steps"]:
        recipe.add_preparing_step(preparing_step)

    # Set output file's details
    output_file: str = recipe_file.removesuffix(".json") + ".pdf"
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

def get_recipes() -> dict[str, Option]:
    recipe_number: int = 1
    recipes: dict[str, Option] = {}
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
        recipes[str(recipe_number)] = Option(recipe.dish_name, select_recipe, recipe=recipe)
        recipe_number += 1

    return recipes

def select_recipe(recipe: Recipe) -> dict[str, Option]:
    print(f"Selected recipe: {recipe.dish_name}")
    return {}

def back(last_options) -> dict[str, Option]:
    last_menu: dict[str, Option] = last_options.pop()
    return last_menu

def quit_app(tui: TUI):
    tui.app_on = False
    return {}
