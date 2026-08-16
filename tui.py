from typing import Any
from collections.abc import Callable

class Option:
    """A class that represents a single option."""
    
    def __init__(self, display: str, func: Callable, color: str="", **kwargs) -> None:
        """Create an option.

        Args:
            display: Displayed name.
            func: function to execute on option call.
            color: Custom color for option's shortcut.
        """
        self.display: str = display
        self.color: str = color
        self.func: Callable = func
        self.kwargs = {}
        for key, arg in kwargs.items():
            if key in self.kwargs.keys():
                continue
            self.kwargs[key] = arg
    def __str__(self) -> str:
        return self.display
    def __repr__(self) -> str:
        return f'Option(display="{self.display}", func={self.func.__name__}, color={self.color}, kwargs={self.kwargs})'
    def run(self, **kwargs) -> Any:
        # This check is needed to avoid passing the same keyword arguments multiple times
        for key, arg in kwargs.items():
            if key in self.kwargs.keys():
                continue
            self.kwargs[key] = arg
        return self.func(**self.kwargs)

class TUI:
    """A class for Text User Interface"""
    def __init__(self) -> None:
        self.options: dict[str, Option] = {}
        self.statuses: list[tuple[str, str]] = []
        self.app_on: bool = False
    def __str__(self) -> str:
        return "Text User Interface"
    def __repr__(self) -> str:
        return "TUI()"

    def add_option(self, shortcut: str, option: Option) -> None:
        """Adds an option to the menu.

        Args:
            shortcut: A key used to select the option. Can be a number or a letter.
            option: An Option object.
        """
        self.options[shortcut] = option

    def clear_options(self) -> None:
        self.options.clear()

    def show(self) -> None:
        """Displays every option in a table.
        If statuses are present, shows them first."""
        table_width, keys_length = self._get_table_width()
        horizontal_line: str = "-" * table_width
        print(horizontal_line)
        if self.statuses:
            for status in self.statuses:
                status_width: int = table_width - 8
                print(f"| {status[0]} | {status[1]:<{status_width}} |")
            print(horizontal_line)
        for key, option in self.options.items():
            option_width: int = table_width - keys_length - 7
            print(f"| \033[94m{option.color}{key.upper():>{keys_length}}\033[0m | {option.display:<{option_width}} |")
        print(horizontal_line)

    def add_status(self, status) -> None:
        """Appends status icon and text to statuses list.

        Args:
            status: A tuple containing status icon/symbol and status text.
        """
        for s in self.statuses:
            if status[1] == s[1]:
                return
        self.statuses.append(status)
        
    def _get_table_width(self):
        """Calculates a width to draw the manu table according to the length of statuses and options.
        Assumes that status icon is a singular symbol."""
        longest: int = 0
        longest_key: int = 0
        # Check statuses length
        for status in self.statuses:
            length: int = 8
            length += len(status[1])
            if length > longest:
                longest = length

        # Check option lengths
        for key, option in self.options.items():
            if len(key) > longest_key:
                longest_key = len(key)
            length: int = 7
            length += len(key)
            length += len(option.display)
            if length > longest:
                longest = length
        return longest, longest_key
