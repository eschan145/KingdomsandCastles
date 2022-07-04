from arcade import SpriteList, Window
from arcade import run

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from sprite import Soldier, Arrow
from constants import *

from units import Unit
from units import setup

player_list = SpriteList()
enemy_list = SpriteList()

setup(player_list, enemy_list)

class Battlefield(Window):

    def __init__(self):
        Window.__init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        global player_list, enemy_list
        
        self.player_list = SpriteList()
        self.enemy_list = SpriteList()
        
        self.unit = Unit(player_formation, self.player_list)
    
    def on_draw(self):
        self.player_list.draw()
        self.enemy_list.draw()

        self.player_list = player_list
        self.enemy_list = enemy_list

        print(list(player_list))


if __name__ == "__main__":
    battlefield = Battlefield()

    run()
