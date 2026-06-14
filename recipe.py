import json

class Recipe:
    def __init__(self, data: dict) -> None:
        self.dish_name: str = data["dish_name"]
        self.cousine: list[str] = data["cousine"]
        self.servings: int = data["servings"]
        self.ingredients: dict = data["ingredients"]
        self.preparing_steps: list[str] = data["preparing_steps"]
