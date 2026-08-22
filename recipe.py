from os import path, get_terminal_size
from textwrap import wrap
from shortcuts import ShowInfo

class AppError(Exception):
    pass

class Recipe:
    def __init__(self, flags: int = 0) -> None:
        self.separator: str = "-" * 15
        self.dish_name: str = None
        self.photo: str = None
        self.tags: list[str] = []
        self.servings: int = 0
        self.ingredients: dict[str, dict[str, str]] = {}
        self.preparing_steps: list[str] = []
        self.flags: int = flags

    def __str__(self):
        return self.dish_name

    # ---
    # Setting and adding propeties

    def set_dish_name(self, name: str) -> None:
        self.dish_name = name

    def add_tag(self, tag: str) -> None:
        if not tag:
            return
        if tag in self.tags:
            raise AppError
            return
        self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if not tag:
            return
        for i, t in enumerate(self.tags):
            if t == tag:
                del self.tags[i]
                return True
        return False

    def set_servings(self, servings: int) -> None:
        self.servings = servings

    def add_ingredient_category(self, category: str) -> None:
        if not category:
            return
        if category in self.ingredients.keys():
            return
        self.ingredients[category] = {}
        self.ingredients[category]["order"] = len(self.ingredients)

    def remove_ingredient_category(self, category: str) -> bool:
        try:
            del self.ingredients[category]
            return True
        except:
            return False

    def add_ingredient(self, category: str, ingredient: str, amount: str) -> None:
        if not ingredient or not amount:
            return
        try:
            self.ingredients[category][ingredient] = amount
        except KeyError:
            raise AppError
            return

    def remove_ingredient(self, category: str, ingredient: str) -> bool:
        if not ingredient:
            return False
        try:
            del self.ingredients[category][ingredient]
            return True
        except:
            return False

    def add_preparing_step(self, step: str, position: int|None = None) -> None:
        if not step:
            return
        if position is None:
            self.preparing_steps.append(step)
        else:
            self.preparing_steps.insert(position, step)

    def remove_preparing_step(self, step_index: int) -> bool:
        if not step_index:
            return False
        try:
            del self.preparing_steps[step_index]
            return True
        except:
            return False

    def add_photo(self, photo: str) -> None:
        if not photo:
            return
        self.photo = path.abspath(path.join("data", photo))

    def mark_not_new(self) -> None:
        self.flags = self.flags ^ RecipeFlags.NEW.value 

    # ---
    # Showing data on call
    def show_preparing_steps(self, table_width: int) -> None:
        no_of_steps: int = 0
        steps_total: int = len(self.preparing_steps)
        for i, step in enumerate(self.preparing_steps):
            steps = wrap(step, table_width - 6 - len(str(steps_total)))
            for s in steps:
                if s == steps[0]:
                    print(f"| {i + 1}. {s:<{table_width - len(str(i)) - 6}} |")
                else:
                    print(f"| {' ':<{len(str(i)) + 2}}{s:<{table_width - len(str(i)) - 6}} |")
            if i != len(self.preparing_steps) - 1:
                print(f"| {' ' * (table_width - 4)} |")

    def show_ingredients(self, table_width: int) -> None:
        for category, ingredients in dict(sorted(self.ingredients.items(), key=lambda x: x[1]["order"])).items():
            print(f"| {category:<{table_width - 4}} |")
            for ingredient, amount in ingredients.items():
                if ingredient == "order":
                    continue
                justify: int = table_width - len(ingredient) - 10
                print(f"|     {ingredient}: {amount:_>{justify}} |")

    def show_info(self, ui: dict[str, str], flags: int=ShowInfo.FULL_INFO.value) -> None:
        terminal_width: int = get_terminal_size().columns
        table_width: int = int(terminal_width / 2) + int(terminal_width * 0.25)
        hr: str = "-" * table_width
        print(hr)
        if self.dish_name and (flags & ShowInfo.DISH_NAME.value):
            print(f"| {self.dish_name:^{table_width - 4}} |")
            print(hr)
        if self.tags and (flags & ShowInfo.TAGS.value):
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
        if self.servings and (flags & ShowInfo.SERVINGS.value):
            print(f"| {ui['servings']}: {self.servings:<{table_width - 6 - len(ui['servings'])}} |")
            print(hr)
        if self.ingredients and (flags & ShowInfo.INGREDIENTS.value):
            self.show_ingredients(table_width)
            print(hr)
        if self.preparing_steps and (flags & ShowInfo.STEPS.value):
            self.show_preparing_steps(table_width)
            print(hr)
