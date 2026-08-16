from os import path, get_terminal_size
from textwrap import wrap

class AppError(Exception):
    pass

class Recipe:
    def __init__(self) -> None:
        self.separator: str = "-" * 15
        self.dish_name: str = None
        self.photo: str = None
        self.tags: list[str] = []
        self.servings: int = 0
        self.ingredients: dict[str, dict[str, str]] = {}
        self.preparing_steps: list[str] = []

    def __str__(self):
        return self.dish_name

    # ---
    # Setting and adding propeties

    def set_dish_name(self, name: str) -> None:
        self.dish_name = name

    def add_tag(self, tag: str) -> None:
        if tag in self.tags:
            raise AppError
            return
        self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        for i, t in enumerate(self.tags):
            if t == tag:
                del self.tags[i]

    def set_servings(self, servings: int) -> None:
        self.servings = servings

    def add_ingredient_category(self, category: str) -> None:
        if category in self.ingredients.keys():
            raise AppError
            return
        self.ingredients[category] = {}

    def remove_ingredient_category(self, category: str) -> None:
        try:
            del self.ingredients[category]
        except:
            return

    def add_ingredient(self, category: str, ingredient: str, amount: str) -> None:
        try:
            self.ingredients[category][ingredient] = amount
        except KeyError:
            raise AppError
            return

    def remove_ingredient(self, category: str, ingredient: str) -> None:
        try:
            del self.ingredients[category][ingredient]
        except:
            return

    def add_preparing_step(self, step: str) -> None:
        self.preparing_steps.append(step)

    def remove_preparing_step(self, step_index: int) -> None:
        try:
            del self.preparing_steps[step_index]
        except:
            return

    def add_photo(self, photo: str) -> None:
        if photo is None:
            return
        self.photo = path.abspath(path.join("data", photo))

    # ---
    # Showing data on call
    def show_preparing_steps(self, table_width: int) -> None:
        no_of_steps: int = 0
        steps_total: int = len(self.preparing_steps)
        for i, step in enumerate(self.preparing_steps):
            #print(f"| {no_of_steps}. ", end="")
            steps = wrap(step, table_width - 6 - len(str(steps_total)))
            for s in steps:
                print(f"| {s:<{table_width - 4}} |")
            if i != len(self.preparing_steps) - 1:
                print(f"| {' ' * (table_width - 4)} |")

    def show_ingredients(self, table_width: int) -> None:
        for category, ingredients in self.ingredients.items():
            print(f"| {category:<{table_width - 4}} |")
            for ingredient, amount in ingredients.items():
                justify: int = table_width - len(ingredient) - 10
                print(f"|     {ingredient}: {amount:_>{justify}} |")

    def show_info(self, ui: dict[str, str]) -> None:
        terminal_width: int = get_terminal_size().columns
        table_width: int = int(terminal_width / 2) + int(terminal_width * 0.25)
        hr: str = "-" * table_width
        print(hr)
        if self.dish_name:
            print(f"| {self.dish_name:^{table_width - 4}} |")
            print(hr)
        if self.tags:
            tags_length: int = 4
            print("| ", end="")
            for tag in self.tags:
                if tag is self.tags[-1]:
                    print(f"{tag:<{table_width - tags_length}}", end="")
                else:
                    tags_length += 2
                    tags_length += len(tag)
                    print(tag, end=", ")
            print(" |")
            print(hr)
        if self.servings:
            print(f"| {ui['servings']}: {self.servings:<{table_width - 6 - len(ui['servings'])}} |")
            print(hr)
        if self.ingredients:
            self.show_ingredients(table_width)
            print(hr)
        if self.preparing_steps:
            self.show_preparing_steps(table_width)
            print(hr)
