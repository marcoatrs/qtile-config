import os
from pathlib import Path

from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile import bar, widget, hook, layout

from theme import ColorTheme, get_theme


# VARIABLES
mod = "mod4" # Tecla Windows
browser = "brave" # Navegador
terminal = "alacritty" # Consola
explorer = f"{terminal} -e ranger" # Explorador de archivos
explorer2 = "Thunar" # Explorador alternativo (GUI)
music = "spotify-launcher" # Reproductor de musica
menu = "dmenu_run" # Lanzador de aplicaciones
tabs = "rofi -show" # Ver apps abiernas
font = "Hack Nerd Font Mono" #  Fuente
theme = get_theme("material-darker") # Tema
power_menu_script = Path(__file__).parent / "rofi-power-menu"
power_menu = f"rofi -show power-menu -modi power-menu:{power_menu_script}"


def start_autostart():
    wallpaper = Path(__file__).parent / "nss-wallpaper.jpg"
    commands = [
        "picom &",
        f"feh --bg-fill {wallpaper} &",
    ]
    for command in commands:
        os.system(command)


# Shortcuts
keys = [
    # System
    Key([mod, "shift"], "q", lazy.spawn(power_menu), desc="Menu de apagado"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Recargar QTile"),
    Key([mod], "tab", lazy.next_layout(), desc="Cambio de layout arriba"),
    Key([mod, "shift"], "tab", lazy.prev_layout(), desc="Cambio de layout abajo"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Subir volumen"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Bajar volumen"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Subir brillo"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Bajar brillo"),

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
_items = ["", "", "", "󰯉", "", "", "", "", ""]
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

def base_colors(fg: str, bg: str):
    return {"foreground": fg, "background": bg}


# Configs
groups_configs = {
    "font": font,
    "fontsize": 30,
    "disable_drag": True,
    **base_colors(theme.light, theme.dark),
    "active": theme.active,
    "inactive": theme.inactive,
    "margin_y": 3,
    "margin_x": 0,
    "padding_y": 8,
    "padding_x": 5,
    "borderwidth": 1,
    "rounded": False,
    "highlight_method": 'block',
    "urgent_alert_method": 'block',
    "urgent_border": theme.urgent,
    "this_current_screen_border": theme.focus,
    "this_screen_border": theme.grey,
    "other_current_screen_border": theme.dark,
    "other_screen_border": theme.dark,
}

def separator():
    return widget.Sep(**base_colors(theme.light, theme.dark), linewidth=0, padding=6)


def icon(fg=None, bg=None, fontsize=16, text="."):
    return widget.TextBox(
        **base_colors(fg, bg),
        fontsize=fontsize,
        text=text,
        padding=3
    )

volume_emojis = ["", "", "", ""]

screens = [
    Screen(top=bar.Bar([
        widget.Spacer(**base_colors(theme.light, theme.dark), length=40),
        widget.GroupBox(visible_groups=_items, **groups_configs),
        separator(),
        widget.CurrentLayoutIcon(**base_colors(theme.text, theme.color2), scale=0.65),
        widget.CurrentLayout(**base_colors(theme.text, theme.color2), padding=5),
        separator(),
        widget.WindowName(**base_colors(theme.focus, theme.dark), fontsize=14, padding=5),
        widget.Spacer(**base_colors(theme.light, theme.dark)),
        separator(),
        # widget.Volume(update_interval=0.5, get_volume_command=),
        # separator(),
        widget.Systray(background=theme.dark, padding=5),
        separator(),
        widget.Clock(**base_colors(theme.light, theme.dark), fontsize=15, format='%Y-%m-%d - %H:%M '),
        separator(),
        widget.Spacer(**base_colors(theme.light, theme.dark), length=40)
       ], 
       size=30,
       margin=10,
       rounded=True))
   ]
lazy.group.setlayout("monadtall")


# Startup Once
@hook.subscribe.startup_once
def autostart():
    start_autostart()
