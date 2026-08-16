from tui import TUI, Option
from recipe import Recipe
from shortcuts import Key, ERR, INF, OK
import actions
import utilities

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

def edit_tags(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, recipe: Recipe) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    options: dict[str, Option] = {
            Key.ADD_TAG.value: Option(ui["add_tag"], add_tag, recipe=recipe),
            Key.REMOVE_TAG.value: Option(ui["remove_tag"], remove_tag, recipe=recipe),
            Key.BACK.value: Option(ui["back"], utilities.back, last_options=last_options),
            Key.QUIT.value: Option(ui["quit"], utilities.quit_app, color="\033[91m", ui=ui, tui=tui)
            }
    status = [(INF, recipe.dish_name)]
    return options, status

def add_tag(*, ui: dict[str, Option], last_options: dict[str, Options], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    tag: str = input(f"{ui['add_tag']}: ")
    recipe.add_tag(tag)
    options, status = edit_tags(ui=ui, last_options=last_options, tui=tui, recipe=recipe)
    status.append((OK, ui["tag_added"]))
    return options, status

def remove_tag(*, ui: dict[str, Option], last_options: dict[str, Options], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]|None]:
    tag_to_remove: str = input(f"{ui['remove_tag']}: ")
    removed = recipe.remove_tag(tag_to_remove)
    options, status = edit_tags(ui=ui, last_options=last_options, tui=tui, recipe=recipe)
    if removed:
        status.append((OK, ui["tag_removed"]))
    return options, status
