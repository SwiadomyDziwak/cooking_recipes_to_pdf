from os import path
import json

class TUI:
    def __init__(self) -> None:
        self.options: dict[str, str] = {}
        self.err: str = "\033[91m[\u2718]\033[0m"
        self.ok: str = "\033[92m[\u2714]\033[0m"
        self.info: str = "\033[96m[i]\033[0m"
        self.warn: str = "\033[93m[!]\033[0m"

    def add_option(self, option: str) -> str:
        if option is None:
            return f"{self.warn} Option cannot be empty"
        options_lenght: int = len(self.options) + 1
        self.options[options_lenght] = option
        return f"{self.ok} Option added"

    def clear_options(self) -> str:
        self.options = {}
        return f"{self.ok} Options cleared"

    def show_options(self) -> None:
        for number, option in self.options.items():
            print(f"{number}. {option}")
