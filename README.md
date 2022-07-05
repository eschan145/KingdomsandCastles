## Armies
An advanced battlefield simulator.

In this game, you command an army of soldiers. They can be of the following types:

1. Light infantry         — Regular ordinary foot soldiers
2. Heavy infantry         — Heavily armored but slower foot soldiers
3. Archers                — Soldier specialized in use with a bow

Your job is to battle an enemy army with several commands. Your army is split up into multiple units; each one you can command at your will. You can assign commands to inidividual units. Units can contain smaller units with them, culminating into one huge army.

A soldier is armed with a sword and a bow. Their damage is based on their strength and range. For example, an arrow would inflict more damage at close range than far range. They start out with twenty-four arrows (fifty for archers) and their health is set to 100. Soldiers attack individually if commanded to. If enemies are too far for swords, they use arrows. As a commander, you can also tell them to retreat into lines if near defeat. Until Arcade releases a optimization update, the maximum number of soldiers on each side is fewer than 1,000.

### Formations
Formations are in a three-dimensional list.
- 1 signifies light infantry
- 2 signifies heavy infantry
- 3 signifies archer
- 4 signifies unit commander

### GUI
The GUI interface is completely created by Ethan Chan. It includes several different types of interactive widgets, and more are to be added. All events are supported. All states can be accessed with `.hover`, `.press`, and `.disable` properties. Many widgets have components, which are basically other widgets added within it. For example, the toggle widget has three components: label (for the text), image (for the bar), and image (for the knob). Its main component is the bar, which takes the hover event and hitbox.

![image](https://user-images.githubusercontent.com/103769713/177225082-cb70e196-5159-4a6a-b134-fada8fb977d0.png)

#### Labels
A label is a great and easy way to draw text. Labels are used as components in many widgets, including buttons and sliders. They are fast, but as the number of them approaches the dozens, the FPS drastically slows down. About 100 labels drop the FPS from 60 to 8.

|Parameter||Details|
|-|-|-|
|text|`str` or `None`, HTML|text of label|
|x|`int`|x coordinate of label|
|y|`int`|y coordinate of label|
|colors|`list`, `[normal, (hover, press, disable)]`. Has default|colors of label in RGB|
|font|`list`, `[family, size]`. Defaults to `[Montserrat, 12]`|font of label|
|title|`bool`. Defaults to `False`|label displayed as title?|
|justify|`str`, `LEFT`, `CENTER`, or `RIGHT`. Defaults to `LEFT`|justification of label|
|width|`int`. Defaults to 0|maximum width of the label (used with `multiline`)|
|multiline|`bool`. Defaults to `False`|label with multiple lines?|

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
|callback|`str`, `SINGLE`, `DOUBLE`, `MULTIPLE`|frequency of invoking command|

Components:
- Image
- Label

A button can be invoked by using the `invoke()` function. This sets the state of the button to a false press and calls its command. This is ignored if the button has no command or is disabled. A button can be assigned keys, which invoke the button, using the `keys` property or `bind(*keys)`. Multiple keys can be binded this way. To unbind keys, change the property or use the `unbind(*keys)` function. Images can be changed, with the properties `normal_image`, `hover_image`, `press_image`, and `disable_image`. These are Arcade textures. A button is used when it has focus with <kbd>Space</kbd>.

#### Toggles
A toggle is a switch widget. It switches between true and false states.

|Parameter||Details|
|-|-|-|
|text|`str`, HTML|text of toggle|
|x|`int`|x coordinate of toggle|
|y|`int`|y coordinate of toggle|

### Contact the maintainer
esamuelchan@gmail.com

This game is still heavily in development. If you encounter any issues, please post them in the Issues page. It was created using the Arcade library (https://api.arcade.academy/), which is based off on pyglet. This game was inspired by Masendor (https://github.com/remance/Masendor).

### TODO
- [ ] Display armies
- [x] Have soldiers decide between melee and range attacks
- [x] Give soldiers basic properties (health, strength)
- [ ] Command soldiers
