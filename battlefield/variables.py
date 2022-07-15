"""Contains variables used throughout the battlefield (Pun not intended)"""
from random import choice, randint

import os
import sys

from arcade import load_texture
from math import atan2, cos, sin

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from constants import *
from file import soldier, projectile
from geometry import Point, chance, check_collision, get_closest
from sprite import Object


class Arrow(Object):
    
    def __init__(self, shooter, target):

        """Initiate arrows.
        
        Arrows start with a speed of zero, then speed up as they make their way to
        their target. They evantually slow down as a result of drag.
        
        """

        Object.__init__(self, projectile["arrow"], 0.8)

        self.x = shooter.x
        self.y = shooter.y

        self.rot_speed = 2**32

        self.shooter = shooter
        self.target = target

        self.accuracy = 0
        self.speed = 1

        self.shooter.arrows -= 1
        
        self.accuracy_x = randint(-ARROW_ACCURACY, ARROW_ACCURACY)
        self.accuracy_y = randint(-ARROW_ACCURACY, ARROW_ACCURACY)
        
        if self.shooter.archer:
            self.speed = 0.7

            self.accuracy_x = randint(int(-ARROW_ACCURACY / 2), int(ARROW_ACCURACY / 2))
            self.accuracy_y = randint(int(-ARROW_ACCURACY / 2), int(ARROW_ACCURACY / 2))
        
        self.point = Point(self.target.x + self.accuracy_x,
                           self.target.y + self.accuracy_y)
        
        dest_x = self.point.x
        dest_y = self.point.y

        x_diff = dest_x - self.shooter.x
        y_diff = dest_y - self.shooter.x
        angle = atan2(y_diff, x_diff)

        force = [cos(angle), sin(angle)]
        size = max(self.shooter.width, self.shooter.height) / 2

        self.center_x += size * force[0]
        self.center_y += size * force[1]

        self.window.projectile_list.append(self)
        self.window.physics.add_sprite(
                                       self,
                                       mass=0.1,
                                       damping=1,
                                       friction=0.6,
                                       collision_type="bullet",
                                       elasticity=0
        )

        # Taking into account the angle, calculate our force.
        force[0] *= -ARROW_MOVE_FORCE
        force[1] *= -ARROW_MOVE_FORCE
        
        self.window.physics.apply_force(self, force)

        def arrow_soldier_handler(sprite_a, sprite_b, arbiter, space, data):
            soldier = self.window.physics.get_sprite_for_shape(arbiter[0])

            if self.shooter.allegiance == PLAYER and \
                isinstance(soldier, Soldier) and \
                soldier.allegiance == ENEMY:
                soldier.health -= self.speed * ARROW_DAMAGE
                if soldier.health:
                    self.window.images.append(
                        (
                            self.x, self.y,
                            projectile["arrow"], 0.7,
                            self.angle,
                        )
                    )
                    self.remove()

        self.window.physics.add_collision_handler("arrow", "soldier", post_handler=arrow_soldier_handler)

    def update(self):
        Object.update(self)

        if self.speed < ARROW_MAXIMUM_SPEED:
            self.speed += ARROW_ACCELERATION
        else:
            self.speed -= ARROW_ACCELERATION
        
        # for object in check_collision(self, self.window.player_list):
        #     if self.shooter.allegiance == ENEMY and \
        #         isinstance(object, Soldier):
        #         object.health -= self.speed * ARROW_DAMAGE
        #         object.knockback(ARROW_KNOCKBACK)
        #         if object.health:
        #             self.window.images.append(
        #                 (
        #                     self.x, self.y,
        #                     projectile["arrow"], 0.7,
        #                     self.angle,
        #                 )
        #             )
        #             self.remove()
        
        # for object in check_collision(self, self.window.enemy_list):
        #     if self.shooter.allegiance == PLAYER and \
        #         isinstance(object, Soldier):
        #         object.health -= self.speed * ARROW_DAMAGE
        #         object.knockback(ARROW_KNOCKBACK)
        #         if object.health:
        #             self.window.images.append(
        #                 (
        #                     self.x, self.y,
        #                     projectile["arrow"], 0.7,
        #                     self.angle,
        #                 )
        #             )
        #             self.remove()
        
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

        Object.__init__(self, image, 0.5)

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

        if self.allegiance == PLAYER:
            self.append_texture(load_texture(soldier["player_light_infantry_dead"]))
        else:
            self.append_texture(load_texture(soldier["enemy_light_infantry_dead"]))

    def knockback(self, strength):
        self.reverse(strength)

        self.x += self.change_x
        self.y += self.change_y

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

            if self.arrows:
                arrow = Arrow(self, choice(self.rivals))

    def update(self):
        if self.health <= 0:
            self.set_texture(1)
            self.health = 0

            self.remove()
            self.window.dead_list.append(self)

            return

        if chance(1000):
            self.health += 1
        
        if self.target:
            if get_closest(self, self.rivals)[1] < MELEE_RANGE:
                self.follow(self.target, rate=5, speed=1.5)
