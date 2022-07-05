from arcade import Window
from sys import path

import sys # User full imports: may have three path variables
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from sprite import Soldier
from variables import enemy_list, player_list
from constants import *


class Unit:
    
    def __init__(self, formation, allegiance, x, y):
        global player_list, enemy_list

        self.formation = []
        
        self.x = x
        self.y = y

        if allegiance == player_list:
            self.rivals = enemy_list
        else:
            self.rivals = player_list

        row = x - SOLDIER_SPACING
        col = y

        for rank in formation:
            col = x
            row += SOLDIER_SPACING
            
            for soldier in rank:
                col -= SOLDIER_SPACING
                
                if soldier == 1:
                    soldier = Soldier(PLAYER, self.rivals, light_infantry=True)

                    soldier.left = col
                    soldier.top = row

                    if self.rivals == enemy_list: player_list.append(soldier)
                    else: enemy_list.append(soldier)
