"""Contains variables used throughout the battlefield (Pun not intended)"""

from arcade import SpriteList, get_angle_degrees
from arcade import get_window

from pyglet.event import EventDispatcher

import os
import sys

from scipy import rand


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from sprite import Object

from geometry import Point, chance, check_collision, get_closest, get_angle_degrees

from random import choice, randint, uniform

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
        self.speed = 0.5

        self.shooter.arrows -= 1
        
        self.accuracy_x = randint(-ARROW_ACCURACY, ARROW_ACCURACY)
        self.accuracy_y = randint(-ARROW_ACCURACY, ARROW_ACCURACY)
        
        if self.shooter.archer:
            self.speed = 0.7

            self.accuracy_x = randint(int(-ARROW_ACCURACY / 2), int(ARROW_ACCURACY / 2))
            self.accuracy_y = randint(int(-ARROW_ACCURACY / 2), int(ARROW_ACCURACY / 2))

        
        self.point = Point(self.target.x + self.accuracy_x, self.target.y + self.accuracy_y)

        self.window.projectile_list.append(self)

    def remove(self):
        self.remove_from_sprite_lists()

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
                self.remove()
        
        for object in check_collision(self, self.window.enemy_list):
            if self.shooter.allegiance == PLAYER and \
                isinstance(object, Soldier):
                object.health -= self.speed * ARROW_DAMAGE
                self.remove()
        
        if self.bottom > self.window.height or \
            self.top < 0 or \
            self.left > self.window.width or \
            self.right < 0:
            self.remove()


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

        self.target = None

        if self.archer: self.arrows = 50
    
        self.weapon = RANGE

    def on_attack(self):
        distance = get_closest(self, self.rivals)

        if chance(5):
            self.strength -= 1

        if distance[1] < randint(MELEE_RANGE - MELEE_RANGE_CHANCE,
                              MELEE_RANGE + MELEE_RANGE_CHANCE):
            self.weapon = MELEE

            if distance[1] < MELEE_RANGE:
                distance[0].health -= self.strength * 3
        
        else:
            self.weapon = RANGE

            if self.arrows > 0:
                arrow = Arrow(self, choice(self.rivals))

    def update(self):
        if self.health <= 0:
            self.remove_from_sprite_lists()

        if chance(1000):
            self.health += 1
        
        if self.target:
            if get_closest(self, self.rivals)[1] < MELEE_RANGE:
                self.follow(self.target, rate=5, speed=1.5)

        for enemy in self.rivals:
            if enemy.health > 0: # Enemy dead
                if self.archer: rate = 10000
                else: rate = 15000
                if chance(rate) and len(self.window.projectile_list) < 20:
                    self.on_attack() # TODO: add interval of attack
        
        # if self.allegiance == PLAYER:
        #     list = self.window.player_list
        # else:
        #     list = self.window.enemy_list
        
        for enemy in check_collision(self, self.rivals):
            if chance(5) and self.change_x:
                enemy.y += 1
            

                    
