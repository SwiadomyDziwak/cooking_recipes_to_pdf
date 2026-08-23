# Recipes to PDF converter

A script that converts a recipe's json data to PDF format, which is easy to share and print.
Written in Python, it provides a simple TUI to create and edit recipes.

Current public version: 1.0.0

## Usage

`uv run main.py [args]`

Accepted arguments:
    - -l, --lang - Interface language, currently supports "pl" and "en" languages.
        If not given, defaults to "en".

## Requirements

- Python 3.12.3

Additional Python libraries:
- Jinja2
- weasyprint
- pillow

## Personal note

I've primarly created this to finally sort my evergrowing collection of screenshots
with cooking recipes. During development I learned a ton of useful stuff and I
plan to extend functionality even further.
