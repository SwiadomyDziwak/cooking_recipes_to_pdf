from jinja2 import Template
from weasyprint import HTML, CSS
from recipe import Recipe
import json
from argparse import ArgumentParser
from os import path, listdir

def main() -> None:

    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-l", "--lang", action="store", choices=["pl", "en"], required=True)

    args = parser.parse_args()

    ui_translations_path: str = path.join("data", "ui")
    target_lang: str = args.lang + ".json"
    target_ui_path: str = path.join(ui_translations_path, target_lang)
    with open(target_ui_path) as ui_translation:
        ui: dict[str, str] = json.load(ui_translation)

    recipes_list: dict[str, str] = {}
    no_of_recipes: int = 0
    for file in listdir("data"):
        filepath = path.join("data",file)
        if path.isdir(filepath):
            continue
        no_of_recipes += 1
        recipes_list[str(no_of_recipes)] = filepath

    for recipe_nr, recipe_path in recipes_list.items():
        print(f"{recipe_nr}: {recipe_path}")
        
    select: str = input("Select recipe: ")
    if select in recipes_list.keys():
        with open(recipes_list[select]) as data:
            recipe_data: dict = json.load(data)
        recipe: Recipe = Recipe()
        recipe.ui = ui
        recipe.set_dish_name(recipe_data["dish_name"])
        recipe.set_servings(recipe_data["servings"])
        for tag in recipe_data["tags"]:
            recipe.add_tag(tag)
        for category, ingredients in recipe_data["ingredients"].items():
            recipe.add_ingredient_category(category)
            for ingredient, amount in ingredients.items():
                recipe.add_ingredient(category, ingredient, amount)
        for step in recipe_data["preparing_steps"]:
            recipe.add_preparing_step(step)
    else:
        print("Please enter a valid recipe number.")
        return

    print()
    recipe.show_dish_name()
    recipe.show_servings()
    recipe.show_preparing_steps()
    print()

"""
    with open("templates/cooking1.html") as temp:
        template: Template = Template(temp.read())
    html: str = template.render(recipe=recipe, ui=ui)
    HTML(string=html).write_pdf(
            "pdfs/ziemniaczki_w_sosie_musztardowym.pdf",
            stylesheets=[CSS("templates/cooking1.css")])
"""

if __name__ == "__main__":
    main()
