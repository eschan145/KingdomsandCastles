"""Contains constants used for Armies"""

# Sides

LEFT = "left"
CENTER = "center"
RIGHT = "right"

TOP = "top"
BOTTOM = "bottom"

# Callbacks
SINGLE = "single"
MULTIPLE = "multiple"

DISABLE_ALPHA = 160 # Alpha of disabled widget
FOCUS_SIZE = 1.05 # [DEPRECATED]

X = 0
Y = 0

ENTRY_BLINK_INTERVAL = 0.5 # Interval in seconds the caret blinks in an entry

TOGGLE_VELOCITY = 2 # How fast the knob moves in a toggle
TOGGLE_FADE = 17 # How fast the toggle fades during transitions

SLIDER_VELOCITY = 10 # How fast does the slider glide

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

DEFAULT_FONT_FAMILY = "Montserrat"
DEFAULT_FONT_SIZE = 12

DEFAULT_FONT = ["Montserrat", 12]

UNIT_FRAME_WIDTH = 700
UNIT_FRAME_HEIGHT = 200

red_filter = (0b100, 0b110)
blue_filter = (0b010, 0b110)
arrow_filter = (0b001, 0b001)

PLAYER = "player"
ENEMY = "enemy"
SOLDIER = "soldier"

SQUAD = 12
SWORD = "sword"

MELEE_RANGE = 20
MELEE_RANGE_CHANCE = 10

RANGE = "range"
MELEE = "melee"

ARROW = "arrow"
ARROW_ACCURACY = 10
ARROW_MAXIMUM_SPEED = 1000
ARROW_MAXIMUM_ARCHER_SPEED = 1200
ARROW_SPEED_LOSS = 20
ARROW_DAMAGE = 20
ARROW_KNOCKBACK = 3
ARROW_MOVE_FORCE = 25000

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Armies"

SOLDIER_SPACING = 10

player_formation = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

    
]

enemy_formation = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

fps_list = [

]
