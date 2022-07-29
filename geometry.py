"""Define some geometric functions for Armies."""

from arcade import Sprite, SpriteList, get_window, schedule, unschedule
from cmath import cos, sin
from math import atan2, degrees, hypot, pow, radians, sqrt
from operator import pos, neg
from random import randrange
from typing import Tuple, cast, List
from struct import unpack

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
    """A named 2D Point. This is used in almost every x and y coordinate in
    Armies. Note that this does not have to be used for points, it can be used
    as vectors for gravity, velocity, and more. This was inspired by
    pymunk.vec2d.Vec2d.
    
    A Point supports operations, so you can perform many computations with
    Points. Take a look at the below example.
    
    >>> a = Point(5, 3)
    >>> b = Point(5, 3)
    >>> a + b
    10, 6
    
    It supports:
        - Addition
        - Subtraction
        - Multiplication
        - Division
        - Floor division
    """

    def __init__(self, x, y, name=False):
        """Initialize a named object-oriented Point.

        >>> point = Point(100, 100)
        >>> point.x, point.y
        100, 100
        >>> point["name"]
        1

        x - x coordinate of Point
        y - y coordinate of Point
        name - unique name of Point (identifier). This is automatically
               generated with the number of Points created if not specified
               by this parameter.

        parameters: int, int, str

        properties:
            x - x coordinate of Point
            y - y coordinate of Point
            vx - horizontal velocity of Point
            vy - vertical velocity of Point
            name - unique keyname of Point
            data - map of properties
        
        methods:
            __getitem__ - Return a value from key item of data
            __iter__ - Return a list of the x and y coordinates
            __del__ - Delete point and remove it from scheduling
            __add__ - Add a Point or tuple to x and y coordinates
            __sub__ - Subtract a Point or tuple to x and y coordinates
            __mul__ - Multiply a number with x and y coordinates
            __truediv__ - Divide a number with x and y coordinates
            __floordiv__ - Floor divide a number with x and y coordinates

            get_distance - Get the distance between another Point
            is_in_polygon - Check if exists inside a polygon
            get_closest - Get the closest Point given a list
            get_length - Get the length of the Point
            get_squared_length - Get the squared length of the Point
        """

        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

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

        schedule(self.update, 1 / 60)

    def __call__(self, *args, **kwds):
        """Return a tuplized version of the Point.
        
        >>> a = Point(5, 3)
        >>> a()
        5, 3

        returns: tuple (x and y coordinates)
        """

        return (self.x, self.y)
        
    def __getitem__(self, item):
        """Return a value from key item of data.

        >>> Point(5, 3)["x"]
        5
        
        item - key to find value
        
        parameters: str
        returns: str
        """

        self.data["x"] = self.x
        self.data["y"] = self.y
        self.data["name"] = self.name

        return self.data.get(item, False)
    
    def __iter__(self):
        """Return a list of the x and y coordinates.
        
        >>> iter(Point(5, 3))
        5, 3

        returns: list (x, y)
        """

        return [self.x, self.y]
    
    def __del__(self):
        """Delete Point and remove it from event scheduling.
        
        >>> a = Point(5, 3)
        >>> del a
        """

        try: unschedule(self.update)
        except AttributeError: pass # No scheduling... pretty mysterious

    ### MATHEMATICAL FUNCTIONS ###

    def __add__(self, point):
        """Add a Point or tuple to x and y coordinates.

        >>> Point(5, 3) + (6, 9)
        11, 12
        
        point - point to add coordinates
        
        parameters: Point or tuple
        returns: tuple
        """

        if isinstance(point, Tuple):
            self.x += point[0]
            self.y += point[1]

            return
        
        self.x += point.x
        self.y += point.y

        return self.x, self.y
    
    def __sub__(self, point):
        """Subtract a Point or tuple from x and y coordinates.

        >>> Point(5, 3) - Point(2, 1)
        3, 2
        
        point - point to subtract coordinates
        
        parameters: Point or tuple
        returns: tuple
        """

        if isinstance(point, Tuple):
            self.x -= point[0]
            self.y -= point[1]

            return
        
        self.x -= point.x
        self.y -= point.y

        return self.x, self.y
    
    def __mul__(self, value):
        """Multiply a float by x and y coordinates.

        >>> Point(5, 3) * 2.5
        12.5, 7
        
        value - value to multiply coordinates
        
        parameters: float
        returns: tuple
        """

        self.x *= value
        self.y *= value

        return self.x, self.y
    
    def __truediv__(self, value):
        """Divide x and y coordinates by value.

        >>> Point(5, 3) / 2
        2.5, 1.5
        
        value - value to divide coordinates
        
        parameters: float
        returns: tuple
        """

        self.x /= value
        self.y /= value

        return self.x, self.y
    
    def __floordiv__(self, value):
        """Floor divide x and y coordinates by value (integer division).
        
        >>> Point(5, 3) // 2
        2, 1
        
        value - value to floor divide coordinates
        returns: tuple
        """

        self.x //= value
        self.y //= value

        return self.x, self.y

    def __radd__(self, point):
        """Add a Point or tuple to x and y coordinates. This is a reversed
        addition.

        >>> (5, 3) + Point(5, 3)
        10, 6
        
        point - point to add coordinates
        
        parameters: Point or tuple
        returns: tuple
        """

        return self.__add__(point)

    def __rsub__(self, point):
        """Subtract a Point or tuple from x and y coordinates. This is a 
        reversed subtraction.

        >>> (10, 3) - Point(5, 3)
        5, 0
        
        point - point to add coordinates
        
        parameters: Point or tuple
        returns: tuple
        """

        self.x = point.x - self.x
        self.y = point.y - self.y

        return self.x, self.y
    
    def __rmul__(self, value):
        """Multiply a float by x and y coordinates. This is a reversed
        multiplication.

        >>> 2 * Point(5, 3)
        10, 6
        
        value - value to multiply coordinates
        
        parameters: float
        returns: tuple
        """

        return self.__mul__(value)
    
    def __pos__(self):
        """Return the unary position (converting to positive).
        
        >>> + Point(-5, 3)
        5, 3

        returns: tuple
        """

        self.x = pos(self.x)
        self.y = pos(self.y)

        return self.x, self.y
    
    def __neg__(self):
        """Return the negatated position (converting to negative).
        
        >>> - Point(-5, 3)
        5, -3
        
        returns: tuple
        """

        self.x = neg(self.x)
        self.y = neg(self.y)

        return self.x, self.y

    def get_distance(self, point):
        """Get the distance between another Point. See get_distance for more
        information.
        
        point - Point to get distance
        
        parameters: Point
        returns: int - (distance between two points)
        """

        return get_distance(self, point)
    
    def is_in_polygon(self, polygon):
        """Check if the x and y coordinates exist in a polygon.
    
        polygon - polygon to check if x and y coordinates exist in

        parameters: int, int
        returns: bool (True or False if Point exists in polygon)
        """

        return is_point_in_polygon(self, polygon)
    
    def get_closest(self, list):
        """Get the closest Point from a list. See get_closest for more
        information.
        
        list - list to get closest object
        
        parameters: List (list of Points)
        returns: tuple ((closest, distance))
        """

        return get_closest(self, points)
    
    def get_squared_length(self):
        """Return the squared length of the vector.
        
        returns: int
        """

        return self.x ** 2 + self.y ** 2
    
    def get_length(self):
        """Return the length of the vector.

        returns. int
        """

        return sqrt(self.x ** 2 + self.y ** 2)
    
    def update(self, delta):
        self.x += self.vx
        self.y += self.vy    


def square(value):
    """Calculate the squared value of a number. This forms a quadratic function,
    which is x².

    value - value to take to the power of two
    
    parameters: int
    returns: int
    """

    return pow(value, 2)

def cube(value):
    """Calculate the cubed value of a number. This forms a cubic function, which
    is x³.

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
    """Check if the given Point exists in a polygon.
    
    point - Point to check if in polygon
    polygon - polygon to check if Point coordinates exist in

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

def get_nearby_sprites(object, list):
    """Internal function used by GPU collision check.
    
    object - object to get nearby objects
    list - list of nearby objects
    
    parameters: Object, PhysicsObject
    returns: list (list of objects selected by the transformation)
    """

    count = len(list)
    if count == 0:
        return []

    # Update the position and size to check
    ctx = get_window().ctx
    list._write_sprite_buffers_to_gpu()

    ctx.collision_detection_program["check_pos"] = object.x, object.y
    ctx.collision_detection_program["check_size"] = object.width, object.height

    # Ensure the result buffer can fit all the sprites (worst case)
    buffer = ctx.collision_buffer
    if buffer.size < count * 4:
        buffer.orphan(size=count * 4)

    # Run the transform shader emitting sprites close to the configured position and size.
    # This runs in a query so we can measure the number of sprites emitted.
    with ctx.collision_query:
        list._geometry.transform(  # type: ignore
            ctx.collision_detection_program,
            buffer,
            vertices=count,
        )

    # Store the number of sprites emitted
    emit_count = ctx.collision_query.primitives_generated

    # If no sprites emitted we can just return an empty list
    if emit_count == 0:
        return []

    # .. otherwise build and return a list of the sprites selected by the transform
    return [
        list[i]
        for i in unpack(f'{emit_count}i', buffer.read(size=emit_count * 4))
    ]

def check_collision(a, b, type=None, method=0):
    """Check for collisions between two things. Multiple datatypes are
    supported. You may use a Object or PhysicsObject, a SpriteList, or a List as
    parameters and it will calculate the collisions for you. Optionally, you can
    specify the collision type with the third type parameter. This can be used
    for optimization.

    Spatial hash is a new method developed by Python arcade for detecting
    collisions. This will speed up collisions with motionless objects, but will
    result with buggy moving with active, moving objects.

    Arcade divides the screen up into a grid. We can track which grid location
    each object overlaps, and put them in a hash map. For each grid location, we
    can quickly pull the object in that grid in a fast O* operation. When
    looking for object that collide with our target object, we only look at
    objects in sharing its grid location. This can reduce checks from 50,000 to
    just 3 or 4. If the object moves, we have to recalculate and re-hash its
    location, which reduces speed.

    The method parameter specifies the type of checking collisions:
        0: automatic select:
            - Spatial if avaliable
            - GPU if 1,500+ objects
            - Simple
        1: Spatial hashing if avaliable
        2: GPU based (recommended with 1,500+ objects)
        3: Simple-check

    a - first item to check collision with
    b - second item to check collision with
    type - optional type of collsions
    
    parameters: 
        a - Object or PhysicsObject,
        b - PhysicsObject or SpriteList or List
    returns: list (list of collisions)


    """
    
    single = False
    double = False
    triple = False

    if type:
        if type == Sprite: single = True
        elif type == SpriteList: double = True
        elif type == List: triple = True
    
    else:
        if isinstance(b, Sprite): single = True
        elif isinstance(b, SpriteList): double = True
        elif isinstance(b, List): triple = True
    
    if single:
        return _check_collision(a, b)

    elif double:
        if b.spatial_hash and (method == 1 or method == 0):
        # Spatial
            b_ = b.spatial_hash.get_objects_for_box(a)
        elif method == 3 or (method == 0 and len(b) <= 1500):
            b_ = b  # type: ignore
        else:
            # GPU transform
            b_ = get_nearby_sprites(a, b)  # type: ignore

        return [
            sprite
            for sprite in b_
            if a is not b and _check_collision(a, sprite)
        ]

    elif triple:
        list = []
        
        for b in b:
            for object in b:
                if a is not object and _check_collision(a, object):
                    list.append(object)

        return list

def get_distance(a, b):
    """Get the distance between two objects. Note that other data types may be
    used, as long as they have x and y properties.
    
    a - first object to get distance
    b - second object to get distance
    
    parameters: Point, Point
    returns: int - (distance between two points
    """

    return hypot(a.x - b.x, a.y - b.y)

def get_distance_(a, b):
    """Get the distance between two objects. Note that other data types may be
    used, as long as they have x and y properties. This uses a different
    method:

    d = √(x₁ — x₂)²＋(y₁ — y₂)²

    NOTE: this method is less efficient than get_distance, as it uses more
          steps. But, they both yield the same result.
    
    >>> a = Point(5, 5)
    >>> b = Point(5, 3)
    >>> get_distance(a, b) == get_distance_(a, b)
    True
    
    a - first object to get distance
    b - second object to get distance
    
    parameters: Point, Point
    returns: int - (distance between two points
    """

    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def get_closest(object, list):
    """Get the closest object from a list to another object. Note that other
    data types can be used, as long as they work with get_distance (meaning
    they have x and y properties).
    
    object - object to get distance
    list - list to get closest object
    
    parameters:
        object - Point
        list - List (list of Points)
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

    point.x = x
    point.y = y

    return x, y

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
        
    x1, y1 = -object.width / 2, - height / 2
    x2, y2 = +object.width / 2, - height / 2
    x3, y3 = +object.width / 2, + height / 2
    x4, y4 = -object.width / 2, + height / 2

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
