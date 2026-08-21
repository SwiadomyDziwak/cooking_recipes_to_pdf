from os import path, listdir
from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
from tui import Option, TUI
from typing import Any
from shortcuts import Key, ERR, INF, OK
from datatypes import MenuOptions, StatusList, UIResult
import json
import utilities
import recipe_utilities

def generate_pdf(*, ui: dict[str, str], recipe: Recipe, last_options: MenuOptions, tui: TUI, **kwargs) -> UIResult:
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

    options, status = select_recipe(ui=ui, recipe=recipe, last_options=last_options[:-1], tui=tui)
    status.append((OK, ui["pdf_generated"]))
    return options, status
