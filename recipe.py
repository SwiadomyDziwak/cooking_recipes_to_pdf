from os import path

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

    def remove_tag(self, tag_index: int) -> None:
        try:
            del self.tags[tag_index]
        except:
            return

    def set_servings(self, amount: int) -> None:
        self.servings = amount

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
    def show_preparing_steps(self) -> None:
        no_of_steps: int = 0
        for step in self.preparing_steps:
            no_of_steps += 1
            print(f"{no_of_steps}. {step}")
