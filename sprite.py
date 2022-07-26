from arcade import Sprite, get_window
from math import atan2, cos, degrees, pi, radians, sin
from random import choice, randint, randrange, uniform

from pyglet.event import EventDispatcher
from pymunk import Body, Poly, Vec2d

from geometry import get_angle_degrees
from file import *
from constants import *
from color import *


##### Sprite (arcade.Sprite) #####
# .alive = True
# When .remove_from_sprite_lists(), alive = False


class Object(Sprite):
    def __init__(self, image, scaling=1.0):
        Sprite.__init__(self, filename=image, scale=scaling)

        # Destination point is where we are going
        self._destination_point = None

        # Max speed we can rotate
        self.rot_speed = 3

        self.alive = True
        self.fading = False
        self.ranks = False

        self.moved = False
        self.move_angle = 0

        self.frames = 0

        self.window = get_window()

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

    def remove(self):
        self.remove_from_sprite_lists()
    
    @property
    def destination_point(self):
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        self._destination_point = destination_point
    
    def forward(self, speed):
        self.change_x = cos(self.radians) * speed
        self.change_y = sin(self.radians) * speed

    def rotate_to_point(self, point):
        angle = get_angle_degrees(self.x, self.y, point.x, point.y)

        self.angle = -angle
    
    def follow(self, object, rate=65, speed=2):
        self.x += self.change_x
        self.y += self.change_y

        if not rate and not self.moved:
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
            self.move_angle = atan2(y_diff, x_diff)

            self.moved = True

        if not rate:
            self.change_x = cos(self.move_angle) * speed
            self.change_y = sin(self.move_angle) * speed

            return

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
        
        self.frames += 1

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


class PhysicsObject(Sprite):

    def __init__(self, image, scaling=1.0, mass=1):
        Sprite.__init__(self, filename=image, scale=scaling)

        self.body = Body()
        self.shape = Poly(self.body, self.hit_box)

        self.x = 0
        self.y = 0

        self.stopped = False

        # Destination point is where we are going
        self._destination_point = None

        # Max speed we can rotate
        self.rot_speed = 3

        self.moved = False
        self.move_angle = 0

        self.frames = 0
        self.window = get_window()

        self.window.space.add(self.body, self.shape)

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

    def remove(self):
        self.remove_from_sprite_lists()
    
    @property
    def destination_point(self):
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        self._destination_point = destination_point
    
    def forward(self, speed):
        self.change_x = cos(self.radians) * speed
        self.change_y = sin(self.radians) * speed

    def rotate_to_point(self, point):
        angle = get_angle_degrees(self.x, self.y, point.x, point.y)

        self.angle = -angle
    
    def follow(self, object, rate=65, speed=2):
        self.x += self.change_x
        self.y += self.change_y

        if not rate and not self.moved:
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
            self.move_angle = atan2(y_diff, x_diff)

            self.moved = True

        if not rate:
            self.change_x = cos(self.move_angle) * speed
            self.change_y = sin(self.move_angle) * speed

            return

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
    
    def update(self):
        self.body.position = self.x, self.y
        self.shape.position = self.x, self.y
        
        if self.stopped:
            self.force = 0
            self.body.force = (0, 0)
            self.stop()
            
            return
        self.body.force = self.force
        self.body.angle = self.angle
        self.shape.angle = self.angle
       

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
