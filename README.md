# Armies
An advanced battlefield simulator.

In this game, you command an army of soldiers. They can be of the following types:

1. Light infantry         — Regular ordinary foot soldiers
2. Heavy infantry         — Heavily armored but slower foot soldiers
3. Archers                — Soldier specialized in use with a bow

Your job is to battle an enemy army. Your army is split up into multiple units; each one you can command at your will. You can assign commands to inidividual units. Units can contain smaller units with them, culminating into one huge army. This simulation is designed to be as realistic as possible, so soldiers will take longer to move up hills, bodies are not removed, units somewhat dissolve when commander is killed, etc.

A soldier is armed with a sword and a bow. Their damage is based on their strength and range. For example, an arrow would inflict more damage at close range than far range. They start out with twenty-four arrows (fifty for archers) and their health is set to 100. Soldiers attack individually if commanded to. If enemies are too far for swords, they use arrows. As a commander, you can also tell them to retreat into lines if near defeat. One problem is the current random mumber generator is deadly slow, which keeps the game at 15 fps with only a few hundred soldiers.

An arrow is fired every 10,000 frames for light infantry, 7,000 frames for heavy infantry, and 15,000 frames for archers. An arrow's damage is calculated by multiplying its velocity in px/s by 15.

### Commands
Commands help you lead your army and attack.

|Command|Key|Details|
|-|-|-|
|Volley|<kbd>Q</kbd>|has all <u>archers</u> fire arrows simultaneously at selected targets. Note that this uses up arrows|
|Split|<kbd>W</kbd>|split unit into individual soldiers to attack. Loses defenses of ranks and volleys|
|Switch projectile|<kbd>E</kbd>|switch between arrows, fire arrows, spears, ...|
|Move forward|<kbd>↑</kbd>|move your army forwards|
|Move backward|<kbd>↓</kbd>|move your army backwards|
|Move left|<kbd>←</kbd>|move your army left|
|Move right|<kbd>→</kbd>|move your army right|

### Installation
To install this, you must download the Python `arcade` library.
1. Open up the Command Prompt (Type "cmd" in the search bar and press <kbd>Enter</kbd>
2. Type in `py -m pip install arcade --user` or `python -m pip install arcade --user`
3. Press <kbd>Enter</kbd>

If the download is successful, download this respository and open it with your favorite code editor.

### Formations
Formations are in a three-dimensional list.
- 1 signifies light infantry
- 2 signifies heavy infantry
- 3 signifies archer
- 4 signifies unit commander

## Development information
### TODO
At this point, soldiers need to have more realistic melee attacks. They just swarm into the enemy, instead of pushing their way in. They also can flow through each other, and collision checks need to make them not run into each other.

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

The GUI interface is completely created by Ethan Chan. It includes several different types of interactive widgets, and more are to be added. API is provided to create your own widgets, which can subclass the `Widget` base class. All events are supported. All states can be accessed with `.hover`, `.press`, and `.disable` properties. Many widgets have components, which are basically other widgets added within it. For example, the toggle widget has three components: label (for the text), image (for the bar), and image (for the knob). Its main component is the bar, which takes the hover event and hitbox. I worked really hard on the docs and code so please enjoy it.

To start a GUI interface, use the `Container` class. Initialize this once in your `__init__` function. To start adding widgets, create widgets with their parameters and properties. Add them to the container. In the `on_draw` function, call the container's `draw` function. To end the container and terminate its events, call its `exit` function. If you want to draw each of the widgets's hitboxes, call its `draw_bbox(width, padding)`. Calling `destroy()` on a widget disconnects it from the event framework and removes it from the container. `check_collision(x, y)` sees if the `x` and `y` point is colliding with the widget. If that fails, use `_check_collision(x, y)`.

List of widget events:
|Event|Parameters|Details|
|-|-|-|
|`on_key`|`keys`, `modifiers`|a key is pressed|
|`on_lift`|`keys`, `modifiers`|a key is released|
|`on_hover`|`x`, `y`, `dx`, `dy`|the widget is hovered|
|`on_press`|`x`, `y`, `buttons`, `modifiers`|the widget is pressed|
|`on_release`|`x`, `y`, `buttons`, `modifiers`|the widget is released|
|`on_drag`|`x`, `y`, `dx`, `dy`, `buttons`, `modifiers`|the widget is dragged (only for sliders)|
|`on_scroll`|`x`, `y`, `mouse`, `direction`|the widget is scrolled (only for sliders)|
|`on_focus`||the widget has focus|
|`on_text_select`|`motion`|the widget has text selected (only for `Entry` widgets)|
|`draw`||draw the widget|
|`update`||update the widget|

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
|font|`tuple`, `(family, size)`. Defaults to `("Montserrat", 12)`|font of label|
|title|`bool`. Defaults to `False`|label displayed as title?|
|justify|`str`, (`LEFT`, `CENTER`, or `RIGHT`). Defaults to `LEFT`|justification of label|
|width|`int`. Defaults to 0|maximum width of the label (used with `multiline`)|
|multiline|`bool`. Defaults to `False`|label with multiple lines?|
|command|`callable`. Defaults to `None`|command called when pressed|
|parameters|`list`. Defaults to []|parameters used in command|
|outline|`tuple`, `(color, padding, width)`. Defaults to `None`|create outline surrounding label|

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

### Shapes Documentation
The shapes toolkit is part of the GUI toolkit. Though not completed, it contains several different shapes:
- Rectangle
- Circle
- Ellipse
- Sector
- Line
- Triangle
- Star
- Polygon
- Arc

More customizations are to be added in the future.

- Setting radius for polygons, triangles, and rectangles
- Gradients
- Effects
    - Shadow
    - Glow

![image](https://user-images.githubusercontent.com/103769713/178084276-8d075be6-5dd6-488a-9fa5-a6a87f4164b3.png)

#### Rectangle
A rectangle is the only shape that supports an implemented border. For other shapes, you must draw a copy of it underneath the main shape.

![image](https://user-images.githubusercontent.com/103769713/178083183-97668775-7a60-4ac7-9d32-619fe16f0808.png)![image](https://user-images.githubusercontent.com/103769713/178083412-6da41c0d-a39d-4a8d-a875-ed3bd39c7979.png)

**Left**: `Rectangle(x=200, y=150, width=100, height=100)`

**Right**: `Rectangle(x=200, y=150, width=100, height=100, border=30, colors=(RED, ORANGE_PEEL))` — Shows full border effect

|Parameter||Details|
|-|-|-|
|x|`int`|x coordinate of rectangle|
|y|`int`|y coordinate of rectangle|
|width|`int`|width of rectangle|
|height|`int`|height of rectangle|
|border|`int`. Defaults to 1|border size of rectangle|
|colors|`tuple`, `(fill, border)`. Defaults to `(WHITE, BLACK)`|colors of rectangle in RGB|
|label|`str`. Defaults to `None`|label to add to center of rectangle|

#### Circle
A circle can become a regular n-sided polygon by changing its segments to the number of sides. It can be created by setting an ellipse's a and b to the same value.

![image](https://user-images.githubusercontent.com/103769713/178083664-4d63b232-887f-4255-9307-a308bb449929.png)![image](https://user-images.githubusercontent.com/103769713/178083624-e61bf949-2496-4c58-8762-9cc6989f8857.png)

**Left**: `Circle(x=250, y=200, radius=50, color=BLUE_YONDER)`

**Right**: `Circle(x=250, y=200, radius=50, segments=7, color=BLUE_BELL)`

|Parameter||Details|
|-|-|-|
|x|`int`|x coordinate of circle|
|y|`int`|y coordinate of circle|
|radius|`int`|radius of circle|
|segments|`int`. Defaults to `None`|number of distinct segments. Calculated with `max(14, int(radius / 1.25))`|
|color|`tuple`. Defaults to `BLACK`|color of circle in RGB|

#### Ellipse
An ellipse can also be called an oval.

|Parameter||Details|
|-|-|-|
|x|`int`|x coordinate of ellipse|
|y|`int`|y coordinate of ellipse|
|a|`int`|semi-major axes of the ellipse|
|b|`int`|semi-minor axes of the ellipse|
|color|`tuple`. Defaults to `BLACK`|color of ellipse in RGB|

#### Sector
A sector is a slice of a circle. It is the most complex of the shapes.

|Parameter||Details|
|-|-|-|
|x|`int`|x coordinate of sector|
|y|`int`|y coordinate of sector|
|radius|`int`|radius of sector|
|segments|`int`. Defaults to `None`|number of distinct segments. Calculated with `max(14, int(radius / 1.25))`|
|angle|`int`. Defaults to `math.tau`|angle of sector in radians|
|start|`int`. Defaults to 0|start angle of sector in radians|
|color|`tuple`. Defaults to `BLACK`|color of sector in RGB|

#### Line
|Parameter||Details|
|-|-|-|
|x1|`int`|x1 coordinate of line|
|y1|`int`|y1 coordinate of line|
|x2|`int`|x2 coordinate of line|
|y2|`int`|y2 coordinate of line|
|width|`int`|width of line|
|color|`tuple`. Defaults to `BLACK`|color of line in RGB|

#### Triangle
|Parameter||Details|
|-|-|-|
|x1|`int`|x1 coordinate of triangle|
|y1|`int`|y1 coordinate of triangle|
|x2|`int`|x2 coordinate of triangle|
|y2|`int`|y2 coordinate of triangle|
|x3|`int`|x3 coordinate of triangle|
|y3|`int`|y3 coordinate of triangle|
|color|`tuple`. Defaults to `BLACK`|color of triangle in RGB|

#### Star
NOTE: setting excessive amounts of spikes will cause glitches in drawing, as shown on the right. Two spikes will draw a diamond, while one spike will do nothing.

![image](https://user-images.githubusercontent.com/103769713/178081441-3154878f-910a-48ea-9ecf-bef74d46f7fe.png)![image](https://user-images.githubusercontent.com/103769713/178081289-0bc5d8df-0ad3-4840-9ff0-dcba2179360b.png)

**Left**: `Star(x=250, y=200, outer=40, inner=100, spikes=5, color=YELLOW_ORANGE)`

**Right**: `Star(x=250, y=200, outer=30, inner=100, spikes=1000)`

|Parameter||Details|
|-|-|-|
|x|`int`|x coordinate of star|
|y|`int`|y coordinate of star|
|outer|`int`|outer radius of star|
|inner|`int`|inner radius of star|
|spikes|`int`|number of spikes|
|rotation|`int`|rotation of star in degrees|
|color|`tuple`. Defaults to `BLACK`|color of star in RGB|

#### Create your own widgets
It is super easy to create your own widgets. All you need is to subclass the `Widget` class, which will provide all of the events. You need to specify its parameters.
```
class MyWidget(Widget):
    
    def __init__(self, size, text):
        self.image = Image("file.png")
        
        Widget.__init__(self)
        
        self.size = size
        self.text = text
        
        self.activated = False
```

Let's look at the above code. In line 1—3 we set up the actual subclassing of the widget class. In line 4, we create our component for the widget. Note that not all widgets need to have components, just they are required for more complex widgets. We then initialize the parent `Widget` class by calling its `__init__` function. A widget starting off takes several parameters: image (if none provided a blank one is used), scale (scaling of widget), and frame, which can be specified in the widget's parameters if you want to use it. On line 11 we create an `activated` property, which is required for a widget or a `ValueError` will be raised when calculating its hitbox.

```
    def func(self):
        pass
```

If you are going to create any public functions, create them right after the `__init__` method and before the events. (Internal functions like `__del__` are to be added even before those public functions). After that, you create the events. Any one of the event types can be used. Just make sure to specify the correct amount of parameters. The `draw` function always goes first, and the `update` function last.

```
    def draw(self):
        self.image.draw()
        
        self.component = self.image
        self.activated = True
        
    def on_press(self, x, y, buttons, modifiers):
        """Called when the widget is pressed"""
        
        if not self.activated or self.disable:
            return
```

The `draw` function is only supposed to hold drawing commands, not defining variables, checking widget states, or stuff like that. Those are to be done in the `update` function. You must set the widget's component during the draw function. Also, set `self.activated` to True at the end. Make sure you check if the widget is activated or not disabled before every event. If those are true, then return and stop the function. If you want to register events, then you can do something like this.

`self.dispatch_event("on_color_pick", color)`

This wouold be used fpr a color picker. The name of the event is the first parameter, and then its parameters follow. You can have any number of parameters. Then, in a subclass of a widget, the event using `push_handlers()`. For more information about events, go to the [pyglet event documentation](https://pyglet.readthedocs.io/en/latest/programming_guide/events.html). I highly reccomend the pyglet website for extra help and information.

```
class ColorPicker2(ColorPicker):
    
    def __init__(self):
        ColorPicker.__init__(self)
        
        self.push_handlers(self.on_color_pick)
       
    def on_color_pick(self, color):
        """A color is picked"""
```

After you ware done with the events, use `remove_handlers()`. You can remove specific events as parameters.
### Contact the maintainer
esamuelchan@gmail.com

This game is still heavily in development. If you encounter any issues, please post them in the Issues page. It was created using the Arcade library (https://api.arcade.academy/), which is based off on pyglet. This game was inspired by Masendor (https://github.com/remance/Masendor).

### TODO
- [x] Display armies
- [x] Have soldiers decide between melee and range attacks
- [x] Give soldiers basic properties (health, strength)
- [x] Soldiers take damage when hit
- [ ] Multiplayer
- [ ] Command soldiers
- [ ] Debug `Entry` glitches
- [ ] Complete documentation
