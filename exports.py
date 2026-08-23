from os import path, listdir
from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
from tui import Option, TUI
from shortcuts import Key, ERR, INF, OK, RecipeFlags
from datatypes import MenuOptions, StatusList, UIResult
import json
import utilities
import recipe_utilities

def generate_pdf(*, ui: dict[str, str], recipe: Recipe, tui: TUI, **kwargs) -> UIResult:
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

    # Check if recipe was edited and remove asterisk from dish's name
    if recipe.flags & RecipeFlags.EDITED.value:
        recipe.dish_name = recipe.dish_name.removeprefix("*")

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

    recipe.mark_edited()

    options, status = recipe_utilities.select_recipe(recipe=recipe)
    status.append((OK, ui["pdf_generated"]))
    return options, status

def export_json(*, ui: dict[str, str], tui: TUI, recipe: Recipe, **kwargs) -> UIResult:
    if recipe.flags & RecipeFlags.EDITED.value:
        recipe.dish_name = recipe.dish_name.removeprefix("*")
    json_data = {
            "dish_name": recipe.dish_name,
            "tags": recipe.tags,
            "servings": recipe.servings,
            "photo": recipe.photo,
            "ingredients": recipe.ingredients,
            "preparing_steps": recipe.preparing_steps
            }
    filename: str = input(f"{ui['ask_for_filename']}: ")
    if filename == "":
        filename = recipe.dish_name.lower()
    filename += ".json"
    file_path: str = path.join("data", filename)

    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)

    recipe.mark_saved()
    options, status = recipe_utilities.select_recipe(ui=ui, tui=tui, recipe=recipe)
    return options, status
