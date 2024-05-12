import os
from pathlib import Path

from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile import bar, widget, hook, layout


# VARIABLES
mod = "mod4" # Tecla Windows
browser = "brave" # Navegador
terminal = "alacritty" # Consola
explorer = f"{terminal} -e ranger" # Explorador de archivos
music = "spotify-launcher" # Reproductor de musica
menu = "dmenu_run" # Lanzador de aplicaciones
tabs = "rofi -show" # Ver apps abiernas
font = "Hack Nerd Font Mono"


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
    Key([mod], "tab", lazy.next_layout(), desc="Cambio de layout arriba"),
    Key([mod, "shift"], "tab", lazy.prev_layout(), desc="Cambio de layout abajo"),

    # Window
    Key([mod], "w", lazy.window.kill(), desc="Cerrar ventana"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover focus abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover focus arriba"),
    Key([mod], "Left", lazy.layout.left(), desc="Mover focus izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover focus derecha"),
    Key([mod, "shift"], "h", lazy.layout.grow(), desc="Mas grande"),
    Key([mod, "shift"], "s", lazy.layout.shrink(), desc="Mas chico"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Cambiar entre flotante"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Cambio de ventana abajo"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Cambio de ventana arriba"),

    # Apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Abrir el terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Abrir navegador"),
    Key([mod], "l", lazy.spawn(music), desc="Abrir reproductor de musica"),
    Key([mod], "e", lazy.spawn(explorer), desc="Abrir explorador de archivos"),
    Key([mod], "m", lazy.spawn(menu), desc="Abrir menu de aplicaciones"),
    Key([mod, "shift"], "m", lazy.spawn(tabs), desc="Ver aplicaciones abiertas")
   ]


# Mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


# Groups
_items = ["  ", "  ", "  ", " 󰯉 ", "  ", "  ", "  ", "  ", "  "]
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

# Configs
groups_configs = {
    "font": font,
    "fontsize": 25,
    "disable_drag": True
}


screens = [
    Screen(top=bar.Bar([
        widget.GroupBox(**groups_configs),      # display the current Group
        widget.Battery(),                       # display the battery state
        widget.CurrentLayout()
       ], 30))
   ]
lazy.group.setlayout("monadtall")


# Startup Once
@hook.subscribe.startup_once
def autostart():
    start_autostart()
