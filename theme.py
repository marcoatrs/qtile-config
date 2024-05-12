import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ColorTheme:
    dark: list
    grey: list
    light: list
    text: list
    focus: list
    active: list
    inactive: list
    urgent: list
    color1: list
    color2: list
    color3: list
    color4: list


def get_default() -> ColorTheme:
    return ColorTheme(
        dark=["#0f101a", "#0f101a"],
        grey=["#37383b", "#37383b"],
        ligth=["#f1ffff", "#f1ffff"],
        text=["#f1ffff", "#f1ffff"],
        focus=["#66818d", "#66818d"],
        active=["#f1ffff", "#f1ffff"],
        inactive=["#4c566a", "#4c566a"],
        urgent=["#3f575b", "#3f575b"],
        color1=["#0f101a", "#0f101a"],
        color2=["#334148", "#334148"],
        color3=["#3f575b", "#3f575b"],
        color4=["#556a74", "#556a74"]
    )


def get_theme(theme: str = "dracula") -> ColorTheme:
    theme_path = Path(__file__).parent / "themes" / f"{theme}.json"
    if not theme_path.exists:
        return get_default()
    with open(theme_path, "r") as theme_file:
        theme_info: dict = json.load(theme_file)
    return ColorTheme(**theme_info)
