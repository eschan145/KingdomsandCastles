from arcade import SpriteList, Window
from arcade import draw_point, enable_timings, get_fps, run

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from constants import *
from color import RED, WHITE
from widgets import Container, Label

from units import Unit
from variables import Arrow, Soldier

# enable_timings()

class Battlefield(Window):

    def __init__(self):
        Window.__init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_list = SpriteList()
        self.enemy_list = SpriteList()
        self.projectile_list = SpriteList()
        
        self.player_unit = Unit(player_formation, PLAYER, 200, 250)
        self.enemy_unit = Unit(enemy_formation, ENEMY, 400, 800)

        self.container = Container()
        self.label = Label("", 50, 50)

        self.container.append(self.label)

        self.background_color = WHITE
    
    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.enemy_list.draw()
        self.projectile_list.draw()

        self.label.text = f"{int(get_fps())} fps"

        self.container.draw()
        
    def on_update(self, delta_time):
        self.player_list.update()
        self.enemy_list.update()
        self.projectile_list.update()

        # import arcade.examples.performance_statistics


if __name__ == "__main__":
    battlefield = Battlefield()

    run()
