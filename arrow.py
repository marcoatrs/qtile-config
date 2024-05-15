from libqtile.widget.textbox import TextBox

_fontsize = 30

def left_arrow(fg, bg):
    return TextBox(
            text="",
            padding=0,
            fontsize=_fontsize,
            foreground=fg,
            background=bg,
            )


def right_arrow(fg, bg):
    return TextBox(
            text="",
            padding=0,
            fontsize=_fontsize,
            foreground=fg,
            background=bg,
            )

 
