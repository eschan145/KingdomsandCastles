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
The GUI interface is completely created by Ethan Chan. It includes several different types of interactive widgets, and more are to be added. All events are supported.

![image](https://user-images.githubusercontent.com/103769713/177225082-cb70e196-5159-4a6a-b134-fada8fb977d0.png)

#### Labels
A label is a great and easy way to draw text. Labels are used as components in many widgets, including buttons and sliders.

|Parameter|Function|
|-|-|-|
|text|`str`, HTML|text to be displayed|
|x||`int`|x coordinate of widget|
|y||`int`|y coordinate of widget|
|colors|`list`, `[normal, (hover, press, disable)]`. Defaults to `[BLACK, (COOL_BLACK, DARK_SLATE_GRAY, DARK_GRAY)]|colors to be displayed in RGB|
|font|`list`, `[family, size]`. Defaults to `[Montserrat, 12]`|font to be displayed|
|title|`bool`. Defaults to `False`|label displayed as title|
|justify|`str`, `LEFT`, `CENTER`, or `RIGHT`. Defaults to `LEFT`


This game is still heavily in development. If you encounter any issues, please post them in the Issues page. It was created using the Arcade library (https://api.arcade.academy/), which is based off on pyglet. This game was inspired by Masendor (https://github.com/remance/Masendor).

### Contact the maintainer
esamuelchan@gmail.com

### TODO
- [ ] Display armies
- [x] Have soldiers decide between melee and range attacks
- [x] Give soldiers basic properties (health, strength)
- [ ] Command soldiers
