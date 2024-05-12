import os
from pathlib import Path

from libqtile.command import lazy
from libqtile.config import Group, Match, Screen, Key
from libqtile import bar, widget, hook, layout


# VARIABLES
mod = "mod4" # Tecla Windows
browser = "brave" # Navegador
terminal = "alacritty" # Consola
explorer = f"{terminal} -e ranger" # Explorador de archivos
music = "spotify-launcher" # Reproductor de musica
menu = "dmenu_run" # Lanzador de aplicaciones
tabs = "rofi -show" # Ver apps abiernas


def start_autostart():
    wallpaper = "/home/marco/.config/qtile/wallpaper.jpg" #Path(__file__).parent / "wallpaper.jpg"
    commands = [
        "picom &",
        f"feh --bg-fill {wallpaper} &",
    ]
    for command in commands:
        os.system(command)


# Shortcuts
keys = [
    # System
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Cerrar sesion"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Recargar QTile"),

    # Window
    Key([mod], "w", lazy.window.kill(), desc="Cerrar ventana"),

    # Apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Abrir el terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Abrir navegador"),
    Key([mod], "l", lazy.spawn(music), desc="Abrir reproductor de musica"),
    Key([mod], "e", lazy.spawn(explorer), desc="Abrir explorador de archivos"),
    Key([mod], "m", lazy.spawn(menu), desc="Abrir menu de aplicaciones"),
    Key([mod, "shift"], "m", lazy.spawn(tabs), desc="Ver aplicaciones abiertas")
   ]


# Groups
_items = ["   ", "   ", "   ", " 󰯉  ", "   ", "   ", "   ", "   ", "   "]
groups = []
for i, item in enumerate(_items):
    group = Group(item, layout="monadtall")
    groups.append(group)
    keys.extend([
        Key([mod], str(i + 1), lazy.group[group.name].toscreen(), desc="Cambiar de Workspace"),
        Key([mod, "shift"], str(i + 1), lazy.window.togroup(group.name, switch_group=True), desc="Mover ventana a workspace"),
    ])


layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(),
    layout.Stack(num_stacks=2)
]


screens = [
    Screen(top=bar.Bar([
        widget.GroupBox(),    # display the current Group
        widget.Battery(),      # display the battery state
        widget.CurrentLayout()
       ], 30))
   ]
lazy.group.setlayout("monadtall")


# Startup Once
@hook.subscribe.startup_once
def autostart():
    start_autostart()
