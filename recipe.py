class Recipe:
    def __init__(self) -> None:
        self.dish_name: str = None
        self.tags: list[str] = []
        self.servings: int = 0
        self.ingredients: dict[str, dict[str, str]] = {}
        self.preparing_steps: list[str] = []

    def set_dish_name(self, name: str) -> None:
        self.dish_name = name

    def add_tag(self, tag: str) -> None:
        if tag in self.tags:
            print("\033[91m[\u2718]\033[0m Tag already exists")
            return
        self.tags.append(tag)

    def set_servings(self, amount: int) -> None:
        self.servings = amount

    def add_ingredient_category(self, category: str) -> None:
        if category in self.ingredients.keys():
            print("\033[91m[\u2718]\033[0m Category already exists.")
            return
        self.ingredients[category] = {}

    def add_ingredient(self, category: str, ingredient: str, amount: str) -> None:
        try:
            self.ingredients[category][ingredient] = amount
        except KeyError:
            print("033[91m[\u2718]\033[0m Wrong ingredient category/element.")
            return

    def add_preparing_step(self, step: str) -> None:
        self.preparing_steps.append(step)
