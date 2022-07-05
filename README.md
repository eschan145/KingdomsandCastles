# Armies
An advanced battlefield simulator.

In this game, you command an army of soldiers. They can be of the following types:

1. Light infantry         — Regular ordinary foot soldiers
2. Heavy infantry         — Heavily armored but slower foot soldiers
3. Archers                — Soldier specialized in use with a bow

Your job is to battle an enemy army. Your army is split up into multiple units; each one you can command at your will. You can assign commands to inidividual units. Units can contain smaller units with them, culminating into one huge army. This simulation is designed to be as realistic as possible, so soldiers will take longer to move up hills, bodies are not removed, units somewhat dissolve when commander is killed, etc.

A soldier is armed with a sword and a bow. Their damage is based on their strength and range. For example, an arrow would inflict more damage at close range than far range. They start out with twenty-four arrows (fifty for archers) and their health is set to 100. Soldiers attack individually if commanded to. If enemies are too far for swords, they use arrows. As a commander, you can also tell them to retreat into lines if near defeat. Until Arcade releases a optimization update, the maximum number of soldiers on each side is fewer than 1,000.

### Formations
Formations are in a three-dimensional list.
- 1 signifies light infantry
- 2 signifies heavy infantry
- 3 signifies archer
- 4 signifies unit commander

## Development information
### Source files
#### Geometry
This file contains geometric functions to be used in Armies.

`Point`

`cube(value)`

`square(value)`

`are_polygons_intersecting(a, b)`

`check_collision(a, b)`

`convert_one_to_four_quadrants(x, y, width, height)`

`get_closest(object, list)`

`get_distance(a, b)`

`is_point_in_polygon(x, y, points)`

`set_hitbox(object)`

`set_polygon(object)`

`_check_collision(a, b)`

### GUI Documentation
Source code: https://github.com/eschan145/Armies/blob/main/widgets.py

The GUI interface is completely created by Ethan Chan. It includes several different types of interactive widgets, and more are to be added. All events are supported. All states can be accessed with `.hover`, `.press`, and `.disable` properties. Many widgets have components, which are basically other widgets added within it. For example, the toggle widget has three components: label (for the text), image (for the bar), and image (for the knob). Its main component is the bar, which takes the hover event and hitbox. I worked really hard on the docs and code so please enjoy it.

To start a GUI interface, use the `Container` class. Initialize this once in your `__init__` function. To start adding widgets, create widgets with their parameters and properties. Add them to the container. In the `on_draw` function, call the container's `draw` function. To end the container and terminate its events, call its `exit` function. If you want to draw each of the widgets's hitboxes, call its `draw_bbox(width, padding)`.

![image](https://user-images.githubusercontent.com/103769713/177225082-cb70e196-5159-4a6a-b134-fada8fb977d0.png)

Source code: (NOTE: none additional commands, properties, or events were used to save space)
```
class MyWindow(Window):
    def __init__(self, title, width, height):
        Window.__init__(
            width, height, title
        )

        self.container = Container()

        self.label = Label(
            "Label",
            10,
            60,
            multiline=True,
            width=500)

        self.button = Button(
            "Click me!",
            250,
            250,
            command=None)

        self.toggle = Toggle(
            "Show fps",
            250,
            350)
        
        self.slider = Slider(
            None,
            250,
            300)

        self.entry = Entry(
            250,
            160)
        
        self.container.append(self.label)
        self.container.append(self.button)
        self.container.append(self.toggle)
        self.container.append(self.slider)
        self.container.append(self.entry)

    def on_draw(self):
        self.clear()
        
        self.container.draw()
```

#### Labels
A label is a great and easy way to draw text. Labels are used as components in many widgets, including buttons and sliders. They are fast, but as the number of them approaches the dozens, the FPS drastically slows down. About 100 labels drop the FPS from 60 to 8.

|Parameter||Details|
|-|-|-|
|text|`str` or `None`, HTML|text of label|
|x|`int`|x coordinate of label|
|y|`int`|y coordinate of label|
|colors|`list`, `[normal, (hover, press, disable)]`. Has default|colors of label in RGB|
|font|`list`, `[family, size]`. Defaults to `["Montserrat", 12]`|font of label|
|title|`bool`. Defaults to `False`|label displayed as title?|
|justify|`str`, (`LEFT`, `CENTER`, or `RIGHT`). Defaults to `LEFT`|justification of label|
|width|`int`. Defaults to 0|maximum width of the label (used with `multiline`)|
|multiline|`bool`. Defaults to `False`|label with multiple lines?|
|command|`callable`. Defaults to `None`|command called when pressed|

All properties, including others like `.alpha`, `document` (pyglet HTML document), `length` (length of text), and `height` can be accessed.

#### Buttons
A button is the simplest interactive widget. It can be given a command as a function when clicked.

|Parameter||Details|
|-|-|-|
|text|`str`, HTML|text of button|
|x|`int`|x coordinate of button|
|y|`int`|y coordinate of button|
|command|`callable`. Defaults to `None`|command called when pressed|
|parameters|`list`. Defaults to `[]`|parameters of command
|colors|`list`, `[button, text]`. Has default|colors of button in `str` and RGB|
|font|`list`, `[family, size]`. Defaults to `["Montserrat", 12]`|font of button|
|callback|`str`, (`SINGLE`, `DOUBLE`, or `MULTIPLE`). Defaults to `SINGLE`|frequency of invoking command|

Components:
- Image (self.image)
- Label (self.label)

A button can be invoked by using the `invoke()` function. This sets the state of the button to a false press and calls its command. This is ignored if the button has no command or is disabled. A button can be assigned keys, which invoke the button, using the `keys` property or `bind(*keys)`. Multiple keys can be binded this way. To unbind keys, change the property or use the `unbind(*keys)` function. Images can be changed, with the properties `normal_image`, `hover_image`, `press_image`, and `disable_image`. These are Arcade textures. A button is used when it has focus with <kbd>Space</kbd>.

#### Toggles
A toggle is a switch widget. It switches between true and false states.

|Parameter||Details|
|-|-|-|
|text|`str`, HTML|text of toggle|
|x|`int`|x coordinate of toggle|
|y|`int`|y coordinate of toggle|
|colors|`tuple`. Defaults to `BLACK`|color of text in RGB|
|font|`list`, `[family, size]`. Defaults to `[Montserrat, 12]`|font of text|
|default|`bool`. Defaults to `True`|default value of toggle|
|padding|`int`. Defaults to 160|horizontal padding between text and bar|

Components:
- Image (self.bar)
- Image (self.knob)
- Label (self.label)

A toggle can be moved by setting its property `.switch` to `True`. This has no effect when disabled. Its state can be accessed using `.value` and its position `.on_left` and `.on_right`. Changing `.value` has no effect, but modifying `.on_left` and `.on_right` will cause the toggle to glitch out and bug. As like the button, the toggle's images can be changed with the `.true_image`, `.false_image`, `.hover_true_image`, and the `hover_false_image`. It can be used when it has focus with <kbd>Space</kbd> and <kbd>Enter</kbd>

#### Sliders
A slider is a numerical widget, designed to show values with a slider.

|Parameter||Details|
|-|-|-|
|text|`str`, HTML|text of slider before change|
|x|`int`|x coordinate of slider|
|y|`int`|y coordinate of slider|
|colors|`tuple`. Defaults to `BLACK`|color of text in RGB|
|font|`list`, `[family, size]`. Defaults to `["Montserrat", 12]`|font of text|
|size|`int`. Defaults to 10|number of numerical values|
|length|`int`. Defaults to 200|length of bar|
|padding|`int`. Defaults to 50|horizontal padding between text and bar|

Components:
- Image (self.bar)
- Image (self.knob)
- Label (self.label)

A slider's value can be taken with its property `.value`. Pressing the <kbd>←</kbd> or <kbd>→</kbd> moves the slider by its numerical amount. Also, scrolling the slider can change its value.

### Contact the maintainer
esamuelchan@gmail.com

This game is still heavily in development. If you encounter any issues, please post them in the Issues page. It was created using the Arcade library (https://api.arcade.academy/), which is based off on pyglet. This game was inspired by Masendor (https://github.com/remance/Masendor).

### TODO
- [x] Display armies
- [x] Have soldiers decide between melee and range attacks
- [x] Give soldiers basic properties (health, strength)
- [x] Soldiers take damage when hit
- [ ] Command soldiers
- [ ] Debug `Entry` glitches
- [ ] Complete documentation
