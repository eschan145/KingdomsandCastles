from arcade import draw_rectangle_outline, get_window
from pyglet.event import EventDispatcher
from random import choice, random

import os
import sys # Use full imports: may have three path variables

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from color import RED
from constants import *
from key import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, Keys
from variables import Arrow, Soldier


class Unit(EventDispatcher):
    
    def __init__(self, formation, allegiance, x, y):
        self.formation = []
        
        self.x = x
        self.y = y

        self.allegiance = allegiance

        self.soldiers = []

        self.window = get_window()

        if allegiance == PLAYER:
            self.rivals = self.window.enemy_list
        else:
            self.rivals = self.window.player_list
        
        self.width = (len(formation[1]) + 1) * SOLDIER_SPACING# Soldier width
        self.height = (len(formation) + 1) * SOLDIER_SPACING
        
        self._x = self.x
        self._y = self.y

        self._x -= self.width / 2
        self._y += self.height / 2

        row = 0
        col = 0

        for rank in formation:
            row += SOLDIER_SPACING
            col = 0
            for soldier in rank:
                col += SOLDIER_SPACING

                if soldier == 1:
                    soldier = Soldier(self.allegiance, self.rivals, light_infantry=True)

                if soldier == 2:
                    soldier = Soldier(self.allegiance, self.rivals, heavy_infantry=True)

                if soldier == 3:
                    soldier = Soldier(self.allegiance, self.rivals, archer=True)

                soldier.x = col + self._x
                soldier.y = self._y - row

                if self.allegiance == PLAYER: self.window.player_list.append(soldier)
                else: self.window.enemy_list.append(soldier)

                self.soldiers.append(soldier)
        
        self.keys = Keys()

        self.window.push_handlers(self)
        self.window.units.append(self)

    def on_volley(self):
        for soldier in self.soldiers:
            if soldier.health > 0 and soldier.archer and soldier.arrows:
                arrow = Arrow(soldier, choice(soldier.rivals))
                arrow = Arrow(soldier, choice(soldier.rivals))
    
    def on_split(self):
        for soldier in self.soldiers:
            soldier.target = choice(soldier.rivals)

    def check_collision(self, x, y):
        return (0 < x - self.x < self.width and
                0 < y - self.y < self.height)
    
    def draw(self):
        if self.window.current_unit == self:
            draw_rectangle_outline(
                self.window.current_unit.x,
                self.window.current_unit.y,
                self.window.current_unit.width,
                self.window.current_unit.height,
                RED
            )
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_collision(x, y):
            if self.allegiance == PLAYER:
                self.window.current_unit = self
    
    def on_update(self, delta):
        for soldier in self.soldiers:
            if not soldier.health:
                self.soldiers.remove(soldier)

        fire = False

        for enemy in self.rivals:
            if enemy.health > 0: # Enemy still alive
                fire = True
                break

        if fire and self.soldiers:
            soldier = choice(self.soldiers)
            if soldier.archer: rate = 2000 / len(self.soldiers)
            if soldier.light_infantry: rate = 3000 / len(self.soldiers)

            if len(self.window.projectile_list) < 50: # Fewer than twenty arrows
                if random() < 1 / rate:     #
                    soldier.on_attack() # Fire

        if not self.window.current_unit == self:
            return
