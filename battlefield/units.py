from arcade import Window
from sys import path

import sys # User full imports: may have three path variables
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from sprite import Soldier

from constants import *

def setup(_player_list, _enemy_list):
    global player_list, enemy_list

    player_list = _player_list
    enemy_list = _enemy_list


class Unit:
    
    def __init__(self, formation, allegiance):
        global player_list, enemy_list

        self.formation = []

        if allegiance == player_list:
            self.rivals = enemy_list
        else:
            self.rivals = player_list

        for rank in formation:
            for soldier in rank:
                if soldier == 1:
                    soldier = Soldier(PLAYER, self.rivals, light_infantry=True)

                    if self.rivals == enemy_list: player_list.append(soldier)
                    else: enemy_list.append(soldier)