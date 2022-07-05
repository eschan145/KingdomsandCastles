"""Contains variables used throughout the battlefield"""

from cmath import cos, sin
from math import atan2, radians
import time
from arcade import SpriteList
from arcade import get_window

from pyglet.event import EventDispatcher

import os
import sys


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from sprite import Object

from geometry import Point, check_collision
from geometry import chance, get_closest

from random import choice, randint

from file import soldier, projectile

from constants import *


class Arrow(Object):
    
    def __init__(self, shooter, target):

        """Initiate arrows.
        
        Arrows start with a speed of zero, then speed up as they make their way to
        their target. They evantually slow down as a result of drag.
        
        """

        Object.__init__(self, projectile["arrow"])

        self.x = shooter.x
        self.y = shooter.y

        self.angle = shooter.angle

        self.destination_point = shooter.x, shooter.y
        self.rot_speed = 2**32

        self.shooter = shooter
        self.target = target

        self.accuracy = 0
        self.speed = 2

        self.shooter.arrows -= 1

        self.point = Point(self.target.x, self.target.y)

        self.window.projectile_list.append(self)

    def update(self):
        Object.update(self)

        if self.speed < ARROW_MAXIMUM_SPEED:
            self.speed += ARROW_ACCELERATION
        else:
            self.speed -= ARROW_ACCELERATION

        self.follow(self.point, rate=0, speed=self.speed)

        for object in check_collision(self, self.window.player_list):
            if self.shooter.allegiance == ENEMY and \
                isinstance(object, Soldier):
                object.health -= self.speed * ARROW_DAMAGE
                self.remove_from_sprite_lists()
        
        for object in check_collision(self, self.window.enemy_list):
            if self.shooter.allegiance == PLAYER and \
                isinstance(object, Soldier):
                object.health -= self.speed * ARROW_DAMAGE
                self.remove_from_sprite_lists()


class Soldier(Object):

    def __init__(self, allegiance, rivals,
                 light_infantry=False, heavy_infantry=False, archer=False):

        """Initiate soldiers.
        
        Soldiers have allegiance to either the player or the enemy. A rivals
        parameter specifies its enemy side, referenced in a SpriteList.

        They can be of multiple types:
            * Light infantry        - Ordinary foot soldiers
            * Heavy infantry        - Heavily armored but slower foot soldiers
            * Archer                - Soldiers that can fire arrows at enemy
        """

        if allegiance == PLAYER:
            image = soldier["player_light_infantry"]
        else:
            image = soldier["enemy_light_infantry"]

        Object.__init__(self, image)

        self.allegiance = allegiance
        self.rivals = rivals

        self.light_infantry = light_infantry
        self.heavy_infantry = heavy_infantry
        self.archer = archer

        self.health = 100
        self.arrows = 24
        self.strength = 10

        if self.archer: self.arrows = 50
    
        self.weapon = RANGE

    def on_attack(self):
        distance = get_closest(self, self.rivals)

        if distance[1] < randint(MELEE_RANGE - MELEE_RANGE_CHANCE,
                              MELEE_RANGE + MELEE_RANGE_CHANCE):
            self.weapon = MELEE

            # TODO: have soldier inflict damage
        
        else:
            self.weapon = RANGE

            if self.arrows > 0:
                arrow = Arrow(self, choice(self.rivals))

    def update(self):
        if self.health <= 0:
            self.remove_from_sprite_lists()

        for enemy in self.rivals:
            self.destination_point = get_closest(self, self.rivals)[0].position

            if enemy.health > 0: # Enemy dead
                if chance(5000) and len(self.window.projectile_list) < 20:
                    self.on_attack() # TODO: add interval of attack
                    