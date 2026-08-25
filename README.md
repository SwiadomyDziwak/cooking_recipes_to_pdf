# Recipes to PDF converter

A script that allows to create, edit and export user's cooking recipes.
Current export supports:
- JSON - for recipes storage and eventually loading into other scripts
- PDF - for easy reading, sharing or even printing

Written in Python, it provides a simple TUI to navigate through options.

Current public version: 1.0.0

## Usage

`uv run main.py [args]`

Accepted arguments:
- -l, --lang - Interface language, currently supports "pl" and "en" languages.
    If not provided, defaults to "en".

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
