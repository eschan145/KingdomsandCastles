import os
import sys

from arcade import SpriteList, Window, close_window, get_fps, run
from pymunk import Space

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

sys.path.append(parent)

from color import GRASS
from constants import *
from key import Q
from widgets import Container, Label

from units import Unit


class Battlefield(Window):

    def __init__(self):
        Window.__init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
                        resizable=True, style=Window.WINDOW_STYLE_DIALOG)

        self.player_list = SpriteList()
        self.enemy_list = SpriteList()
        self.projectile_list = SpriteList()
        self.dead_list = SpriteList(use_spatial_hash=True)

        self.units = []
        self.images = SpriteList(use_spatial_hash=True)

        self.space = Space()

        self.player_unit = Unit(player_formation, PLAYER, self.width / 2, 200)
        self.enemy_unit = Unit(enemy_formation, ENEMY, self.width / 2, 500)

        self.current_unit = self.player_unit

        self.container = Container()

        self.fps = Label("", 50, 50, command=close_window)

        # self.unit_frame = Frame(self.width - UNIT_FRAME_WIDTH / 2, self.height,
        #                         UNIT_FRAME_WIDTH, UNIT_FRAME_HEIGHT, TOP)
        # self.unit_frame.top = 0

        self.unit_organize_volley = Label("Organize volley", 10, 40,
                                          command=self.command, parameters=["volley"])

        self.container.append(self.fps)
        self.container.append(self.unit_organize_volley)

        self.arrow_soldier_collisions = self.space.add_collision_handler(1, 2)

        self.unit_organize_volley.bind(Q)
        self.background_color = GRASS
        self.frames = 0

    def command(self, attack):
        if attack == "volley":
            self.current_unit.on_volley()

    def on_arrow_soldier_collision(self, arbiter, space, data):
        # print(arbiter.shapes)
        # print(arbiter.shapes[1].object)

        soldier = arbiter.shapes[0].object
        arrow = arbiter.shapes[1].object

        if arrow.shooter.allegiance == PLAYER and \
                soldier.allegiance == ENEMY:

            damage = abs(max(arrow.force)) / ARROW_DAMAGE_LOSS
            if not damage:
                damage = 1  # Even slow arrows cause damage

            soldier.wound(damage * ARROW_DAMAGE)

            # if soldier.health:
            #     arrow = PhysicsObject(
            #         projectile["arrow"],
            #         0.7
            #     )

            #     arrow.x, arrow.y = self.x, self.y
            #     arrow.angle = self.angle

            arrow.remove()

        if arrow.shooter.allegiance == ENEMY and \
                soldier.allegiance == PLAYER:
            damage = abs(max(arrow.force)) / ARROW_DAMAGE_LOSS
            if not damage:
                damage = 1  # Even slow arrows cause damage

            soldier.wound(damage * ARROW_DAMAGE)

            arrow.remove()

        return True

    def on_draw(self):
        self.clear()

        self.arrow_soldier_collisions.pre_solve = self.on_arrow_soldier_collision

        # for image in self.images:
        #     create_image(*image)

        self.player_list.draw()
        self.enemy_list.draw()
        self.projectile_list.draw()
        self.dead_list.draw()
        # print(len(self.player_list) + len(self.enemy_list))
        self.fps.text = f"{int(get_fps())} fps"

        self.container.draw()

        for unit in self.units:
            unit.draw()

    def on_update(self, delta):
        self.player_list.update()
        self.enemy_list.update()
        self.projectile_list.update()

        self.space.step(1 / 60.0)

        # for sprite in self.player_list:
        #     check_for_collision_with_list(sprite, self.enemy_list)


if __name__ == "__main__":
    battlefield = Battlefield()

    from pyglet.app import run
    run(1/1200)
