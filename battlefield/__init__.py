from arcade import SpriteList, Window, draw_point
from arcade import run

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from sprite import Soldier, Arrow
from constants import *
from color import RED, WHITE

from units import Unit
from variables import enemy_list, player_list


class Battlefield(Window):

    def __init__(self):
        Window.__init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        global player_list, enemy_list
        
        self.player_list = player_list
        self.enemy_list = enemy_list
        
        self.unit = Unit(player_formation, player_list, 100, 50)
        

        self.background_color = WHITE
    
    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.enemy_list.draw()

        self.player_list = player_list
        self.enemy_list = enemy_list

    def on_update(self, delta_time):
        self.player_list.update()
        self.enemy_list.update()

if __name__ == "__main__":
    battlefield = Battlefield()

    run()
