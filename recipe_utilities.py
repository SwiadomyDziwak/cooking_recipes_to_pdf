from tui import TUI, Option
from recipe import Recipe
from shortcuts import Key, ERR, INF, OK, ShowInfo
import actions
import utilities

def create_recipe(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Creates a new blank recipe."""
    new_recipe: Recipe = Recipe()
    new_dish_name: str = input(f"{ui['enter_dish_name']}: ")
    new_recipe.set_dish_name(new_dish_name)

    options, statuses = actions.select_recipe(ui=ui, last_options=last_options, tui=tui, recipe=new_recipe)
    return options, statuses

def set_servings(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Asks for user's input and sets selected recipe's servings to received value."""
    try:
        servings: int = int(input(f"{ui['servings']}: "))
    except TypeError:
        return last_options, (ERR, ui["enter_number"])
    recipe.set_servings(servings)
    options, status = actions.select_recipe(ui=ui, tui=tui, last_options=last_options, recipe=recipe)
    return options, status

# -- Tag editing --
def edit_tags(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, recipe: Recipe) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Displays options to add or remove recipe's tag."""

    recipe.show_info(ui=ui, flags=ShowInfo.TAGS.value)

    options: dict[str, Option] = {
            Key.ADD.value: Option(ui["add_tag"], add_tag, recipe=recipe),
            Key.REMOVE.value: Option(ui["remove_tag"], remove_tag, recipe=recipe),
            Key.BACK.value: Option(ui["back"], utilities.back, last_options=last_options, status_list=[(INF, recipe.dish_name)]),
            Key.QUIT.value: Option(ui["quit"], utilities.quit_app, color="\033[91m", ui=ui, tui=tui)
            }
    status = [(INF, recipe.dish_name)]
    return options, status

def add_tag(*, ui: dict[str, Option], last_options: dict[str, Option], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Asks for user input and adds received text as a new tag."""
    tag: str = input(f"{ui['add_tag']}: ")
    recipe.add_tag(tag)
    options, status = edit_tags(ui=ui, last_options=last_options, tui=tui, recipe=recipe)
    status.append((OK, ui["tag_added"]))
    return options, status

def remove_tag(*, ui: dict[str, Option], last_options: dict[str, Option], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Asks for user input and if it exists in recipe's tags, removes it."""
    tag_to_remove: str = input(f"{ui['remove_tag']}: ")
    removed = recipe.remove_tag(tag_to_remove)
    options, status = edit_tags(ui=ui, last_options=last_options, tui=tui, recipe=recipe)
    if removed:
        status.append((OK, ui["tag_removed"]))
    return options, status

# -- Ingredient categories editing --
def categories_menu(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, recipe: Recipe, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    """Displays options to add, edit and remove ingredient categories.
    Also allows to select category to interact with ingredients."""

    recipe.show_info(ui=ui, flags=ShowInfo.INGREDIENTS.value)
    
    options = {}
    category_counter: int = 1
    for category in recipe.ingredients.keys():
        options[str(category_counter)] = Option(category, select_category, recipe=recipe, category=category)
        category_counter += 1

    options[Key.BACK.value] = Option(ui["back"], utilities.back, last_options=last_options, status_list=[(INF, recipe.dish_name)])
    options[Key.QUIT.value] = Option(ui["quit"], utilities.quit_app, color="\033[91m", ui=ui, tui=tui)

    status = [(INF, recipe.dish_name)]
    return options, status

def select_category(*, ui: dict[str, str], last_options: dict[str, Option], tui: TUI, recipe: Recipe, category: str, **kwargs) -> tuple[dict[str, Option], list[tuple[str, str]]]:
    options: dict[str, Option] = {}
    status: list[tuple[str, str]] = [(INF, f"{recipe.dish_name} - {category}")]

    options[Key.BACK.value] = Option(ui["back"], utilities.back, last_options=last_options, status_list=[(INF, recipe.dish_name)])
    options[Key.QUIT.value] = Option(ui["quit"], utilities.quit_app, color="\033[91m", ui=ui, tui=tui)

    return options, status

def new_category() -> None:
    pass

def edit_category() -> None:
    pass

def del_category() -> None:
    pass

# -- Ingredients editing --
def add_ingredient() -> None:
    pass

def edit_ingredient() -> None:
    # Ask for both name and amount for simplicity
    pass

def del_ingredient() -> None:
    pass

# -- Preparing steps editing --
def add_step() -> None:
    # Ask where to add - if empty, append to the end of the list
    pass

def del_step() -> None:
    pass
