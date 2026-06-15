from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
import json
from argparse import ArgumentParser
from os import path

def main() -> None:

    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-l", "--lang", action="store", choices=["pl", "en"], required=True)

    args = parser.parse_args()

    ui_translations_path: str = path.join("data", "ui")
    target_lang: str = args.lang + ".json"
    target_ui_path: str = path.join(ui_translations_path, target_lang)
    with open(target_ui_path) as ui_translation:
        ui: dict[str, str] = json.load(ui_translation)

    with open("data/kremowe_kokosowe_ramen_z_kurczakiem_katsu.json") as data:
        recipe: Recipe = Recipe(json.load(data))
    with open("templates/cooking1.html") as temp:
        template: Template = Template(temp.read())
    html: str = template.render(recipe=recipe, ui=ui)
    HTML(string=html).write_pdf(
            "pdfs/kremowe_kokosowe_ramen_z_kurczakiem_katsu.pdf",
            stylesheets=[CSS("templates/cooking1.css")])

if __name__ == "__main__":
    main()
