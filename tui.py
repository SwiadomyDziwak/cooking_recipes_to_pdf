from typing import Any
from collections.abc import Callable

class Option:
    def __init__(self, display: str, func: Callable, **kwargs) -> None:
        self.display: str = display
        self.func: Callable = func
        self.kwargs = kwargs
    def __str__(self) -> str:
        return self.display
    def run(self) -> Any:
        return self.func(**self.kwargs)

class TUI:
    def __init__(self) -> None:
        self.options: dict[str, Option] = {}
        self.statuses: list[str] = []
        self.app_on: bool = False

    def add_option(self, shortcut: str, option: Option) -> None:
        self.options[shortcut] = option

    def clear_options(self) -> None:
        self.options.clear()

    def show_options(self) -> None:
        for key, option in self.options.items():
            print(f"[ \033[95m{key.upper()}\033[0m ] {option.display}")
        return self.options

    def show_status(self) -> None:
        if not self.statuses:
            return
        for status in self.statuses:
            print(status)
        self.statuses.clear()
        print()

    def add_status(self, status) -> None:
        self.statuses.append(status)
