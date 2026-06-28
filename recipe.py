from os import path

class Recipe:
    def __init__(self) -> None:
        self.ui: dict[str, str] = None
        self.separator: str = "-" * 15
        self.dish_name: str = None
        self.photo: str = None
        self.tags: list[str] = []
        self.servings: int = 0
        self.ingredients: dict[str, dict[str, str]] = {}
        self.preparing_steps: list[str] = []

    # ---
    # Setting and adding propeties

    def set_dish_name(self, name: str) -> None:
        self.dish_name = name

    def add_tag(self, tag: str) -> None:
        if tag in self.tags:
            print(f"\033[91m[\u2718]\033[0m {self.ui['error_tag_exists']}")
            return
        self.tags.append(tag)

    def set_servings(self, amount: int) -> None:
        self.servings = amount

    def add_ingredient_category(self, category: str) -> None:
        if category in self.ingredients.keys():
            print(f"\033[91m[\u2718]\033[0m {self.ui['error_category_exists']}")
            return
        self.ingredients[category] = {}

    def add_ingredient(self, category: str, ingredient: str, amount: str) -> None:
        try:
            self.ingredients[category][ingredient] = amount
        except KeyError:
            print(f"033[91m[\u2718]\033[0m {self.ui['error_wrong_category']}")
            return

    def add_preparing_step(self, step: str) -> None:
        self.preparing_steps.append(step)

    def add_photo(self, photo: str) -> None:
        if photo is None:
            return
        self.photo = path.abspath(path.join("data", photo))

    # ---
    # Showing data on call

    def show_dish_name(self) -> None:
        print(f"\033[94m-- {self.dish_name}\033[0m")

    def show_servings(self) -> None:
        print(f"\033[96mServings:\033[0m {self.servings}") 

    def show_preparing_steps(self) -> None:
        no_of_steps: int = 0
        print(f"\033[96m{self.ui['preparing_steps']}\033[0m")
        for step in self.preparing_steps:
            no_of_steps += 1
            print(f"{no_of_steps}. {step}")
