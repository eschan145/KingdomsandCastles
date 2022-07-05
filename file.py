# Set up variables and filepaths

import getpass
import sys

username = getpass.getuser() # Get username [DEPRECATED]

# Get directory paths
directory = sys.path[0]

path = f"{directory}/".replace("\\", "/").replace("/battlefield", "")

image_path = f"{path}images/"
gui_image_path = f"{image_path}gui/"


# To be put into settings
theme = "yellow"

button = {
    f"{theme}_button_normal" : f"{gui_image_path}{theme}_button_normal.png",
    f"{theme}_button_hover" : f"{gui_image_path}{theme}_button_hover.png",
    f"{theme}_button_press" : f"{gui_image_path}{theme}_button_press.png",
    f"{theme}_button_disable" : f"{gui_image_path}{theme}_button_disable.png"
}

# TODO: add all of the filepaths into entry map, toggle map, etc.
entry_normal = f"{gui_image_path}entry_normal.png"
entry_hover = f"{gui_image_path}entry_hover.png"
entry_focus = f"{gui_image_path}entry_focus.png"

toggle_true = f"{gui_image_path}toggle_true.png"
toggle_false = f"{gui_image_path}toggle_false.png"
toggle_true_hover = f"{gui_image_path}toggle_true_hover.png"
toggle_false_hover = f"{gui_image_path}toggle_false_hover.png"

slider_horizontal = f"{gui_image_path}slider_horizontal.png"

knob = f"{gui_image_path}knob.png"

none = f"{image_path}application/none.png"


soldier = {
    "player_light_infantry" : f"{image_path}/objects/soldiers/player_light_infantry.png"
}

projectile = {
    "arrow" : f"{image_path}/objects/projectiles/arrow.png"
}
