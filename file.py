# Set up variables and filepaths

import getpass
import sys
import os

username = getpass.getuser() # Get username [DEPRECATED]

# Get directory paths
directory = sys.path[0]
directory = os.path.dirname(os.path.realpath(__file__))

path = f"{directory}/".replace("\\", "/").replace("/battlefield", "")

image_path = f"{path}images/"
gui_image_path = f"{image_path}gui/"


# To be put into settings

blank1 = f"{image_path}application/blank1.png"
blank2 = f"{image_path}application/blank2.png"

widgets = {}
colors = ["blue", "green", "silver", "red", "yellow"]

for color in colors:
    widgets[f"{color}_button_normal"] = f"{gui_image_path}{color}_button_normal.png"
    widgets[f"{color}_button_hover"] = f"{gui_image_path}{color}_button_hover.png"
    widgets[f"{color}_button_press"] = f"{gui_image_path}{color}_button_press.png"
    widgets[f"{color}_button_disable"] = f"{gui_image_path}{color}_button_disable.png"
    widgets[f"{color}_button_square_normal"] = f"{gui_image_path}{color}_button_square_normal.png"
    widgets[f"{color}_button_square_hover"] = f"{gui_image_path}{color}_button_square_hover.png"
    widgets[f"{color}_button_square_press"] = f"{gui_image_path}{color}_button_square_press.png"

# TODO: add all of the filepaths into entry map, toggle map, etc.
entry_normal = f"{gui_image_path}entry_normal.png"
entry_hover = f"{gui_image_path}entry_hover.png"
entry_focus = f"{gui_image_path}entry_focus.png"

toggle_true = f"{gui_image_path}toggle_true.png"
toggle_false = f"{gui_image_path}toggle_false.png"
toggle_true_hover = f"{gui_image_path}toggle_true_hover.png"
toggle_false_hover = f"{gui_image_path}toggle_false_hover.png"

slider_horizontal = f"{gui_image_path}slider_horizontal.png"

combobox_top_normal = f"{gui_image_path}combobox_top_normal.png"
combobox_top_hover = f"{gui_image_path}combobox_top_hover.png"
combobox_middle_normal = f"{gui_image_path}combobox_middle_normal.png"
combobox_middle_hover = f"{gui_image_path}combobox_middle_hover.png"
combobox_bottom_normal = f"{gui_image_path}combobox_bottom_normal.png"
combobox_bottom_hover = f"{gui_image_path}combobox_bottom_hover.png"


knob = f"{gui_image_path}knob.png"

colorchooser = f"{gui_image_path}colorchooser.png"

none = f"{image_path}application/none.png"

arrow_trail = f"{image_path}objects/projectiles/arrow_trail.png"

soldier = {
    "player_light_infantry" : f"{image_path}/objects/soldiers/player_light_infantry.png",
    "enemy_light_infantry" : f"{image_path}/objects/soldiers/enemy_light_infantry.png",
    "player_light_infantry_dead" : f"{image_path}/objects/soldiers/player_light_infantry_dead.png",
    "enemy_light_infantry_dead" : f"{image_path}/objects/soldiers/enemy_light_infantry_dead.png",
}

projectile = {
    "arrow" : f"{image_path}/objects/projectiles/arrow.png"
}
