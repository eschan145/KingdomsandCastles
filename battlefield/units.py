from arcade import Window, get_window
from sys import path

import sys # User full imports: may have three path variables
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from variables import Soldier
from constants import *


class Unit:
    
    def __init__(self, formation, allegiance, x, y):
        self.formation = []
        
        self.x = x
        self.y = y

        self.window = get_window()

        if allegiance == PLAYER:
            self.rivals = self.window.enemy_list
        else:
            self.rivals = self.window.player_list
        
        row = x - SOLDIER_SPACING
        col = y

        for rank in formation:
            col = x
            row += SOLDIER_SPACING
            
            for soldier in rank:
                col -= SOLDIER_SPACING

                if soldier == 1:
                    soldier = Soldier(allegiance, self.rivals, light_infantry=True)

                    soldier.left = col
                    soldier.top = row

                    if self.rivals == self.window.enemy_list: self.window.player_list.append(soldier)
                    else: self.window.enemy_list.append(soldier)
                
                if soldier == 3:
                    soldier = Soldier(allegiance, self.rivals, archer=True)

                    soldier.left = col
                    soldier.top = row

                    if self.rivals == self.window.enemy_list: self.window.player_list.append(soldier)
                    else: self.window.enemy_list.append(soldier)
