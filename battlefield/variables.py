"""Contains variables used throughout the battlefield (Pun not intended)"""

import os
import sys
from math import atan2, cos, sin
from random import choice, randint

from arcade import load_texture
from pymunk import ShapeFilter

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

sys.path.append(parent)

from color import RED
from constants import (ARROW_ACCURACY, ARROW_MAXIMUM_ARCHER_SPEED,
                       ARROW_MAXIMUM_SPEED, ARROW_MINIMUM_SPEED, ENEMY, MELEE,
                       MELEE_RANGE, MELEE_RANGE_CHANCE, PLAYER, RANGE,
                       SOLDIER_MELEE_REACH)
from file import projectile, soldier
from geometry import Point, chance, get_closest
from sprite import PhysicsObject


class Arrow(PhysicsObject):

    def __init__(self, shooter, target):

        """Initiate arrows.

        Arrows start with a speed of zero, then speed up as they make their way to
        their target. They evantually slow down as a result of drag.
        """

        PhysicsObject.__init__(
            self, projectile["arrow"], 0.8, mass=0.13, type=2)

        self.x = shooter.x
        self.y = shooter.y

        self.rot_speed = 2**32

        self.shooter = shooter
        self.target = target

        self.accuracy = 0
        self.speed = randint(ARROW_MINIMUM_SPEED, ARROW_MAXIMUM_SPEED)

        self.shooter.arrows -= 1

        self.collision_type = 2

        self.accuracy_x = randint(-ARROW_ACCURACY, ARROW_ACCURACY)
        self.accuracy_y = randint(-ARROW_ACCURACY, ARROW_ACCURACY)

        if self.shooter.archer:
            self.speed = ARROW_MAXIMUM_ARCHER_SPEED

            self.accuracy_x = randint(
                int(-ARROW_ACCURACY / 2), int(ARROW_ACCURACY / 2))
            self.accuracy_y = randint(
                int(-ARROW_ACCURACY / 2), int(ARROW_ACCURACY / 2))

        self.point = Point(self.target.x + self.accuracy_x,
                           self.target.y + self.accuracy_y)

        if self.shooter.allegiance == PLAYER:
            self.shape.filter = ShapeFilter(categories=0b0010, mask=0b1101)

        if self.shooter.allegiance == ENEMY:
           self.shape.filter = ShapeFilter(categories=0b0001, mask=0b1110)

        self.destination_point = self.point.x, self.point.y

        self.window.projectile_list.append(self)

    def update(self):
        PhysicsObject.update(self)

        if self.speed > 5:
            self.speed -= 5

        dest_x = self.point.x
        dest_y = self.point.y

        x_diff = dest_x - self.shooter.x
        y_diff = dest_y - self.shooter.y
        angle = atan2(y_diff, x_diff)

        force = [cos(angle), sin(angle)]

        # Taking into account the angle, calculate our force.
        force[0] *= self.speed
        force[1] *= self.speed

        self.force = force

        # arrow_player_collision = check_for_collision_with_list(self, self.window.player_list)
        # arrow_enemy_collision = check_for_collision_with_list(self, self.window.enemy_list)

        # for soldier in self.collisions:
        #     if self.shooter.allegiance == ENEMY:
        #         damage = abs(max(self.force)) / ARROW_DAMAGE_LOSS
        #         if not damage:
        #             damage = 1 # Even slow arrows cause damage

        #         soldier.wound(damage * ARROW_DAMAGE)

        #         if soldier.health:
        #             arrow = PhysicsObject(
        #                 projectile["arrow"],
        #                 0.7
        #             )

        #             arrow.x, arrow.y = self.x, self.y
        #             arrow.angle = self.angle

        #             self.remove()

        # for soldier in arrow_enemy_collision:
        #     if self.shooter.allegiance == PLAYER:
        #         damage = abs(max(self.force))
        #         if not damage:
        #             damage = 1 # Even slow arrows cause damage

        #         soldier.wound(damage * ARROW_DAMAGE)

        #         # print(damage, ARROW_DAMAGE)

        #         # print(self.force)
        #         if soldier.health:
        #             arrow = PhysicsObject(
        #                 projectile["arrow"],
        #                 0.7
        #             )

        #             arrow.x, arrow.y = self.x, self.y
        #             arrow.angle = self.angle

        #             self.remove()

        if self.bottom > self.window.height or \
            self.top < 0 or \
            self.left > self.window.width or \
            self.right < 0:
            self.remove()


class Soldier(PhysicsObject):
    _health = 100

    def __init__(self, allegiance, rivals,
                 light_infantry=False, heavy_infantry=False, archer=False):

        """Initiate soldiers.
        
        **Soldiers have allegiance to either the player or the enemy. A rivals
        parameter specifies its enemy side, referenced in a SpriteList.
        They can be of multiple types:
            * Light infantry        - Ordinary foot soldiers
            * Heavy infantry        - Heavily armored but slower foot soldiers
            * Archer                - Soldiers that can fire arrows at enemy

        allegiance - allegiance of the soldier
        rivals - rivals of the soldier
        light_infantry - soldier is light infantry
        heavy_infantry - soldier is heavy infantry
        archer - soldier is an archer
        """

        if allegiance == PLAYER:
            image = soldier["player_light_infantry"]
        else:
            image = soldier["enemy_light_infantry"]

        PhysicsObject.__init__(self, image, 0.5, mass=145, type=1)

        self.allegiance = allegiance
        self.rivals = rivals

        self.light_infantry = light_infantry
        self.heavy_infantry = heavy_infantry
        self.archer = archer

        self.hands = (None, "bow")

        self.arrows = 24
        self.strength = randint(70, 100)

        self.target = None
        self.health = 100

        self.mass = 10

        self.moving_up = False
        self.moving_down = False

        self.angle = 90

        if self.archer:
            self.arrows = 50

        self.weapon = RANGE

        self.collision_type = 1

        if self.allegiance == PLAYER:
            self.shape.filter = ShapeFilter(categories=0b1000, mask=0b1101)
            self.append_texture(load_texture(
                soldier["player_light_infantry_dead"]))

        else:
            self.shape.filter = ShapeFilter(categories=0b0100, mask=0b1110)
            self.append_texture(load_texture(
                soldier["enemy_light_infantry_dead"]))

    def wound(self, amount):
        self.color = RED
        self.health -= amount

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
                distance[0].wound(self.strength / 10)

        else:
            self.weapon = RANGE

            if self.arrows:
                arrow = Arrow(self, choice(self.rivals))

    def on_melee(self):
        distance = 2**32

        if not self.target:
            self.target, distance = get_closest(self, self.rivals)

        # Thrust with sword
        if distance < SOLDIER_MELEE_REACH:
            self.target.wound(5)

    def update(self):
        PhysicsObject.update(self)

        # if self.color != (255, 255, 255):
        #     try:
        #         self.color[1] += 1
        #     except ValueError:
        #         pass

        if self.health <= 0:
            self.set_texture(1)
            self.health = 0

            self.remove()
            self.window.dead_list.append(self)

            return

        if self.moving_up:
            self.force = (
                0,  # cos(self.radians) * self.strength / 10,
                sin(self.radians) * self.strength / 10
            )
        elif self.moving_down:
            self.force = (
                cos(self.radians) * self.strength / 10,
                sin(self.radians) * -self.strength / 10
            )

        if chance(1000):
            self.health += 1

        if self.target:
            if get_closest(self, self.rivals)[1] < MELEE_RANGE:
                self.follow(self.target, rate=5, speed=1.5)
