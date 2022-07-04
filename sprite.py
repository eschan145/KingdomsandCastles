from arcade import Sprite
from math import atan2, cos, degrees, pi, radians, sin
from random import choice, randint, randrange, uniform

from geometry import get_closest, get_distance
from file import *
from constants import *
from color import *


##### Sprite (arcade.Sprite) #####
# .alive = True
# When .remove_from_sprite_lists(), alive = False


class Object(Sprite):
    def __init__(self, image, scaling=1.0):
        super().__init__(filename=image, scale=scaling)

        # Destination point is where we are going
        self._destination_point = None

        # Max speed we can rotate
        self.rot_speed = 3

        self.alive = True
        self.fading = False
        self.ranks = False

    def _get_x(self):
        return self._position[0]

    def _set_x(self, new_value):
        if new_value != self._position[0]:
            self.clear_spatial_hashes()
            self._point_list_cache = None
            self._position = (new_value, self._position[1])
            self.add_spatial_hashes()

            for sprite_list in self.sprite_lists:
                sprite_list.update_location(self)

    def _get_y(self):
        return self._position[1]

    def _set_y(self, new_value):
        if new_value != self._position[1]:
            self.clear_spatial_hashes()
            self._point_list_cache = None
            self._position = (self._position[0], new_value)
            self.add_spatial_hashes()

            for sprite_list in self.sprite_lists:
                sprite_list.update_location(self)

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    
    @property
    def destination_point(self):
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        self._destination_point = destination_point
    
    def follow(self, object, rate=65, speed=2):
        self.x += self.change_x
        self.y += self.change_y

        # Random 1 in rate chance that we'll change from our old direction and
        # then re-aim toward the player
        if not randrange(rate):
            start_x = self.x
            start_y = self.y

            # Get the destination location for the bullet
            dest_x = object.x
            dest_y = object.y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = cos(angle) * speed
            self.change_y = sin(angle) * speed

    def direction(self, sprite, position):
        right = False
        left = False
        top = False
        bottom = False
        
        if sprite.x > self.x:
            right = True
        elif sprite.x < self.x:
            left = True

        if sprite.y > self.y:
            top = True
        elif sprite.y < self.y:
            bottom = True

        if position == "top" and top:
            return True
        elif position == "bottom" and bottom:
            return True
        elif position == "right" and right:
            return True
        elif position == "left" and left:
            return True
        else:
            return False
        
    def update(self):
        # Update the player

        if self.fading:
            try:
                self.alpha -= self.fading
            except ValueError:
                self.remove_from_sprite_lists()
                
        # If we have no destination, don't go anywhere.
        if not self._destination_point:
            self.change_x = 0
            self.change_y = 0
            return

        # Position the start at our current location
        start_x = self.x
        start_y = self.y

        # Get the destination location
        dest_x = self._destination_point[0]
        dest_y = self._destination_point[1]

        # Do math to calculate how to get the sprite to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the player will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        target_angle_radians = atan2(y_diff, x_diff)
        if target_angle_radians < 0:
            target_angle_radians += 2 * pi

        # What angle are we at now in radians?
        actual_angle_radians = radians(self.angle - 270)

        # How fast can we rotate?
        rot_speed_radians = radians(self.rot_speed)

        # What is the difference between what we want, and where we are?
        angle_diff_radians = target_angle_radians - actual_angle_radians

        # Figure out if we rotate clockwise or counter-clockwise
        if abs(angle_diff_radians) <= rot_speed_radians:
            # Close enough, let's set our angle to the target
            actual_angle_radians = target_angle_radians
            clockwise = None
        elif angle_diff_radians > 0 and abs(angle_diff_radians) < pi:
            clockwise = False
        elif angle_diff_radians > 0 and abs(angle_diff_radians) >= pi:
            clockwise = True
        elif angle_diff_radians < 0 and abs(angle_diff_radians) < pi:
            clockwise = True
        else:
            clockwise = False

        # Rotate the proper direction if needed
        if actual_angle_radians != target_angle_radians and clockwise:
            actual_angle_radians -= rot_speed_radians
        elif actual_angle_radians != target_angle_radians:
            actual_angle_radians += rot_speed_radians

        # Keep in a range of 0 to 2pi
        if actual_angle_radians > 2 * pi:
            actual_angle_radians -= 2 * pi
        elif actual_angle_radians < 0:
            actual_angle_radians += 2 * pi

        # Convert back to degrees
        if not self.ranks:
            self.angle = degrees(actual_angle_radians) + 270

        self.x += self.change_x
        self.y += self.change_y


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Arrow(Object):
    
    def __init__(self, shooter, target):

        """Initiate arrows.
        
        Arrows start with a speed of zero, then speed up as they make their way to
        their target. They evantually slow down as a result of drag.
        
        """

        Object.__init__(self, projectile["arrow"])

        self.shooter = shooter
        self.target = target

        self.accuracy = 0 # TODO: add misses
        self.speed = 0

        self.point = Point(self.target.x, self.target.y)
    
    def update(self):
        if self.speed < ARROW_MAXIMUM_SPEED:
            self.speed += ARROW_ACCELERATION
        else:
            self.speed -= ARROW_ACCELERATION
        self.follow(self.point, speed=self.speed)

        
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

        Object.__init__(self, image)

        self.allegiance = allegiance
        self.rivals = rivals

        self.light_infantry = light_infantry
        self.heavy_infantry = heavy_infantry
        self.archer = archer

        self.health = 100
        self.arrows = 24
        self.strength = 10
    
        self.weapon = RANGE

    def on_attack(self):
        distance = get_closest(self, self.rivals)

        if distance[1] < randint(MELEE_RANGE - MELEE_RANGE_CHANCE,
                              MELEE_RANGE + MELEE_RANGE_CHANCE):
            self.weapon = MELEE

            # TODO: have soldier inflict damage
        
        else:
            self.weapon = RANGE

            arrow = Arrow(PLAYER, self, distance[0])
            self.fire_projectile(arrow)
            
    def update(self):
        for enemy in self.rivals:
            if enemy.health > 0: # Enemy dead
                self.on_attack() # TODO: add interval of attack
                
                break


class Explosion(Object):
    def __init__(self, textures):
        Object.__init__(self, None)

        # Start at the first frame
        self.current_texture = 0
        self.textures = textures

        self.angle = randint(1, 360)
        self.scale = uniform(1, 1.2)
        
    def update(self):
        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 5
        
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            if self.alpha > 30:
                self.alpha -= 30
            else:
                self.remove_from_sprite_lists()
