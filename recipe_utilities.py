from tui import TUI, Option
from recipe import Recipe
from shortcuts import ERR
import actions

def create_recipe(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    new_recipe: Recipe = Recipe()
    new_dish_name: str = input(f"{ui['enter_dish_name']}: ")
    new_recipe.set_dish_name(new_dish_name)

    options, statuses = actions.select_recipe(ui=ui, last_options=last_options, tui=tui, recipe=new_recipe)
    return options, statuses

def set_servings(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    try:
        servings: int = int(input(f"{ui['servings']}: "))
    except TypeError:
        return last_options, (ERR, ui["enter_number"])
    recipe.set_servings(servings)
    options, status = actions.select_recipe(ui=ui, tui=tui, last_options=last_options, recipe=recipe)
    return options, status

def add_tag(*, ui: dict[str, Option], last_options: dict[str, Options], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    tag: str = input(f"{ui['add_tag']}: ")
    recipe.add_tag(tag)
    return actions.select_recipe(ui=ui, last_options=last_options, tui=tui, recipe=recipe)

def remove_tag(*, ui: dict[str, Option], last_options: dict[str, Options], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    tag_to_remove: str = input(f"{ui['tag_to_remove']}: ")
    recipe.remove_tag(tag_to_remove)
    return actions.select_recipe(ui=ui, last_options=last_options, tui=tui, recipe=recipe)
