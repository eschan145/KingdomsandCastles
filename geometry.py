from arcade import Sprite, SpriteList
from math import hypot
from typing import cast, List

class Point:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.data = {}

    def __getitem__(self, data):
        return self.data.get(data, False)
        
def square(value):
    return pow(value, 2)

def cube(value):
    return pow(value, 3)

def are_polygons_intersecting(a, b):
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

def is_point_in_polygon(x, y, points):
    length = len(points)
    inside = False
    p1x, p1y = points[0]
    
    if not length:
        return False
    
    for i in range(length + 1):
        p2x, p2y = points[i % length]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    # noinspection PyUnboundLocalVariable
                    if p1x == p2x or x <= xints:
                        inside = not inside
                        
        p1x, p1y = p2x, p2y

    return inside

def _check_collision(a, b):
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
    return hypot(a.x - b.x, a.y - b.y)

def get_closest(object, list):
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
    
