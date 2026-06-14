from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
import json

def main() -> None:
    with open("data/kremowe_kokosowe_ramen_z_kurczakiem_katsu.json") as data:
        recipe = Recipe(json.load(data))
    with open("templates/cooking1.html") as temp:
        template: Template = Template(temp.read())
    html: str = template.render(recipe=recipe)
    HTML(string=html).write_pdf(
            "test.pdf",
            stylesheets=[CSS("templates/cooking1.css")])

if __name__ == "__main__":
    main()
