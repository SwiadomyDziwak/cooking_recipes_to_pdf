from recipe import Recipe
from tui import TUI, Option
from typing import Any
from shortcuts import Key, ERR, INF, OK
import actions

def create(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    new_recipe: Recipe = Recipe()
    new_dish_name: str = input(f"{ui['enter_dish_name']}: ")
    new_recipe.set_dish_name(new_dish_name)

    options, statuses = actions.select_recipe(ui=ui, last_options=last_options, tui=tui, recipe=new_recipe)
    return options, statuses

