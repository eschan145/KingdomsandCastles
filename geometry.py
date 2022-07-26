"""Define some geometric functions for Armies."""

from cmath import cos, sin
from random import randrange
from arcade import Sprite, SpriteList
from math import atan2, degrees, hypot, radians
from typing import cast, List

points = 0 # Number of points to create unique keysets
pi = 3.14159265358979

__all__ = [
           "Point",
           "square",
           "cube",
           "chance",
           "are_polygons_intersecting",
           "is_point_in_polygon",
           "check_collision",
           "get_distance",
           "get_closest",
           "rotate_point",
           "get_angle_degrees",
           "get_angle_radians",
           "degrees_to_radians",
           "convert_xywh_to_points",
           "points",
           "pi",
           "_check_collision"
          ]


class Point:
    """Initialize a named Point. This is used in almost every x and y
    coordinate in Armies."""
    
    def __init__(self, x, y, name=False):
        """Initialize a named Point.
        
        x - x coordinate of Point
        y - y coordinate of Point
        name - unique name of Point (identifier). This is automatically
               generated with the number of Points created if not specified
               by this parameter.

        parameters: int, int, str

        properties:
            x - x coordinate of Point
            y - y coordinate of Point
            name - unique keyname of Point
            data - map of properties
        
        methods:
            __getitem__ - Return a value from key item of data
        """

        self.x = x
        self.y = y

        if not name:
            # Generate a unique keyset name for this point
            global points
            points += 1

            self.name = str(points)
            
        self.data = {
            "x" : self.x,
            "y" : self.y,
            "name" : self.name
        }

    def __getitem__(self, item):
        """Return a value from key item of data.
        
        item - key to find value
        
        parameters: str
        returns: str
        """

        return self.data.get(item, False)
        

def square(value):
    """Calculate the squared value of a number.
    
    value - value to take to the power of two
    
    parameters: int
    returns: int
    """

    return pow(value, 2)

def cube(value):
    """Calculate the cubed value of a number.
    
    value - value to take to the power of three

    parameters: int
    returns: int
    """

    return pow(value, 3)

def chance(value):
    """Return True or False in a 1-in-value chance.
    
    value - chance of returning True
    
    parameters: int
    returns: bool
    """

    if randrange(1, value + 1) == 2:
        return True
    else:
        return False

def are_polygons_intersecting(a, b):
    """Check if two polygons are intersecting.
    
    a - first polygon bounding box of intersection check
    b - second polygon bounding box of intersection check

    parameters: int, int
    returns: bool (True or False if polygons intersecting)
    """

    for polygon in (a, b):
        for i1 in range(len(polygon)):
            i2 = (i1 + 1) % len(polygon)
            projection_1 = polygon[i1]
            projection_2 = polygon[i2]

            normal = (projection_2[1] - projection_1[1],
                      projection_1[0] - projection_2[0])

            min_a, max_a, min_b, max_b = (None,) * 4

            for _polygon in a:
                projected = normal[0] * _polygon[0] + normal[1] * _polygon[1]

                if min_a is None or projected < min_a:
                    min_a = projected
                if max_a is None or projected > max_a:
                    max_a = projected

            for _polygon in b:
                projected = normal[0] * _polygon[0] + normal[1] * _polygon[1]

                if min_b is None or projected < min_b:
                    min_b = projected
                if max_b is None or projected > max_b:
                    max_b = projected

            if cast(float, max_a) <= cast(float, min_b) \
                or cast(float, max_b) <= cast(float, min_a):
                return False

    return True

def is_point_in_polygon(point, polygon):
    """See if the given Point exists in a polygon.
    
    point - Point to check if in polygon
    polygon - polygon to recieve test

    parameters: int, int
    returns: bool (True or False if Point exists in polygon)
    """

    length = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    
    if not length:
        return False
    
    for i in range(length + 1):
        p2x, p2y = points[i % length]
        if point.y > min(p1y, p2y):
            if point.y <= max(p1y, p2y):
                if point.x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (point.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    # noinspection PyUnboundLocalVariable
                    if p1x == p2x or point.x <= xints:
                        inside = not inside
                        
        p1x, p1y = p2x, p2y

    return inside

def _check_collision(a, b):
    """Internal function for checking collision of two objects. Used by
    check_collision.
    
    a - first object to check collision
    b - second object to check collision
    
    NOTE: you should never need to call this directly.
    NOTE: you must use an Object or a PhysicsObject. If you want to check
          collisions with other objects, use are_polygons_interecting with
          each object's hitbox. Note there are exceptions to these conditions.
    
    parameters:
        a - Object or PhysicsObject
        b - Object or PhysicsObject
    returns: list (list of collisions)
    """

    collision_radius = a.collision_radius + b.collision_radius

    diff_x = a.position[0] - b.position[0]
    diff_x2 = square(diff_x)

    if diff_x2 > collision_radius * collision_radius:
        return False

    diff_y = a.position[1] - b.position[1]
    diff_y2 = square(diff_y)
    if diff_y2 > square(collision_radius):
        return False

    distance = diff_x2 + diff_y2
    if distance > square(collision_radius):
        return False

    try:
        intersection = are_polygons_intersecting(a.get_adjusted_hit_box(),
                                                 b.get_adjusted_hit_box())
    except ValueError:
        intersection = []
        
    return intersection

def check_collision(a, b):
    """Check for collisions between two things. Multiple datatypes are
    supported. You may use a Object or PhysicsObject, a SpriteList, or a List as parameters and it will calculate the collisions for you.
    
    a - first item to check collision with
    b - second item to check collision with
    
    parameters: 
        a - Object or PhysicsObject,
        b - PhysicsObject or SpriteList or List
    returns: list (list of collisions)
    """
    
    if isinstance(b, Sprite):
        return _check_collision(a, b)

    elif isinstance(b, SpriteList):
        return [
            sprite
            for sprite in b
            if a is not b and _check_collision(a, sprite)
        ]

    elif isinstance(b, List):
        sprites = []
        
        for spritelist in b:
            for sprite in spritelist:
                if a is not sprite and _check_collision(a, sprite):
                    sprites.append(sprite)

        return sprites

def get_distance(a, b):
    """Get the distance between two Points.
    
    a - first point to get distance
    b - second point to get distance
    
    parameters: Point, Point
    returns: int - (distance between two points
    """

    return hypot(a.x - b.x, a.y - b.y)

def get_closest(object, list):
    """Get the closest object from a list to another object.
    
    object - object to get distance
    list - list to get closest object
    
    parameters:
        object - Object or PhysicsObject
        list - List or SpriteList
    returns: tuple ((closest, distance))
    """

    if not list:
        return [object, 0]

    position = 0
    distance = get_distance(object, list[position])
    
    for i in range(1, len(list)):
        _distance = get_distance(object, list[i])

        if _distance < distance:
            position = i
            distance = _distance

    return list[position], distance

def rotate_point(point, center, degrees):
    """Rotate a Point a certain degrees around a center.
    
    point - Point to rotate around center
    center - center the Point rotates around
    degrees - angle to rotate
    
    parameters: Point, Point, int
    returns: Point
    """

    temp_x = point.x - center.x
    temp_y = point.y - center.y

    # now apply rotation
    radians_ = radians(degrees)
    cos_angle = cos(radians_)
    sin_angle = sin(radians_)
    rotated_x = temp_x * cos_angle - temp_y * sin_angle
    rotated_y = temp_x * sin_angle + temp_y * cos_angle

    # translate back
    rounding_precision = 2
    x = round(rotated_x + center.x, rounding_precision)
    y = round(rotated_y + center.y, rounding_precision)

    return Point(x, y)

def get_angle_degrees(a, b):
    """Get angle degrees between two Points.
    
    a - first Point to get angle degrees
    b - second Point to get angle degrees
    
    parameters: Point, Point
    returns: int
    """

    x_diff = b.x - a.x
    y_diff = b.y - a.y
    
    angle = degrees(atan2(x_diff, y_diff))

    return angle


def get_angle_radians(a, b):
    """Get angle radians between two Points.
    
    a - first Point to get angle radians
    b - second Point to get angle radians

    parameters: Point, Point
    returns: int
    """

    x_diff = b.x - a.x
    y_diff = b.y - a.y
    angle = atan2(x_diff, y_diff)
    return angle

def degrees_to_radians(degrees, digits=2):
    """Convert degrees to radians.
    
    degrees - degrees to be converted to radians
    digits - number of digits of the π value
    
    parameters: int
    returns: int
    """

    return degrees * round(pi, digits) / 180

def convert_xywh_to_points(point, width, height):
    """Convert an rectangle with center points and dimensions to only points.
    
    point - center Point of rectangle
    width - width of rectangle
    height - height of rectangle
    
    parameters: Point, int, int
    returns: tuple (x1, y1, x2, y2)
    """

    # Note this does not return two Points
    return (
        point.x - width / 2,
        point.y + height / 2,
        point.x + width / 2,
        point.y - height / 2
    )

### DECEPRATED FUNCTIONS ###

def set_hitbox(object):
    height = object.height
    
    if not object.height:
        height = 1
        
    x1, y1 = -object.width / 2, -height / 2
    x2, y2 = +object.width / 2, -height / 2
    x3, y3 = +object.width / 2, +height / 2
    x4, y4 = -object.width / 2, +height / 2

    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

def set_position(object):
    height = object.height
    
    if not object.height:
        height = 1
        
    object.right = object.x - object.width
    object.left = object.x + object.width
    object.top = object.y + height
    object.bottom = object.y - height

    object.hit_box = set_hitbox(object)
    
def convert_four_to_one_quadrants(x, y, width, height):
    x = width / 2 + x
    y = height / 2 + y

    return x, y
