from arcade import SpriteList, Window, close_window
from arcade import get_fps, run

import os
import sys

from pymunk import Space

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from color import GRASS
from constants import *
from key import Q, W
from widgets import Container, Frame, Label, create_image

from units import Unit


class Battlefield(Window):

    def __init__(self):
        Window.__init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

        self.player_list = SpriteList()
        self.enemy_list = SpriteList()
        self.projectile_list = SpriteList()
        self.dead_list = SpriteList()

        self.units = []
        self.images = []

        self.space = Space()
        
        self.player_unit = Unit(player_formation, PLAYER, self.width / 2, 200)
        self.enemy_unit = Unit(enemy_formation, ENEMY, self.width / 2, 500)

        self.current_unit = self.player_unit

        self.container = Container()

        self.fps = Label("", 50, 50, command=close_window)

        self.unit_frame = Frame(self.width - UNIT_FRAME_WIDTH / 2, self.height,
                                UNIT_FRAME_WIDTH, UNIT_FRAME_HEIGHT, TOP)
        self.unit_frame.top = 0
        
        self.unit_organize_volley = Label("Organize volley", 10, 40, self.unit_frame,
                                          command=self.command, parameters=["volley"])

        self.container.append(self.fps)
        self.container.append(self.unit_organize_volley)

        self.unit_organize_volley.bind(Q)

        self.background_color = GRASS

    def command(self, attack):
        if attack == "volley":
            self.current_unit.on_volley()

    def on_draw(self):
        self.clear()
        
        for image in self.images:
            create_image(*image)

        self.player_list.draw()
        self.enemy_list.draw()
        self.projectile_list.draw()
        self.dead_list.draw()

        self.fps.text = f"{int(get_fps())} fps"
        
        self.container.draw()

        for unit in self.units:
            unit.draw()
        
    def on_key_press(self, keys, modifiers):
        if keys == W:
            self.current_unit.on_split()

    def on_update(self, delta):
        self.player_list.update()
        self.enemy_list.update()
        self.projectile_list.update()

        self.space.step(1 / 60.0)


if __name__ == "__main__":
    battlefield = Battlefield()

    run()
