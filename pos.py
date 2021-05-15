import math
import params

class Pos:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

def closest_to_zero(*args):
    return min(args, key=abs)

def get_displacement(a, b, c):
    if abs(a) < abs(b):
        if abs(a) < abs(c):
            return a
        return c
    if abs(b) < abs(c):
        return b
    return c

# returns closest (since map rolls over) (direction,distance) from obj1 to obj2
def get_dir_dist(obj1, obj2):
    x_vect = closest_to_zero(obj2.pos.x - obj1.pos.x, obj2.pos.x - obj1.pos.x - params.MAP_SIZE_X)
    y_vect = closest_to_zero(obj2.pos.y - obj1.pos.y, obj2.pos.y - obj1.pos.y - params.MAP_SIZE_Y)
    return math.atan2(y_vect, x_vect), math.sqrt(math.pow(x_vect, 2) + math.pow(y_vect, 2))

def get_smallest_displacement(obj1, obj2):
    x1, x2, map_x = obj1.pos.x, obj2.pos.x, params.MAP_SIZE_X
    y1, y2, map_y = obj1.pos.y, obj2.pos.y, params.MAP_SIZE_Y
    x_disp = get_displacement(x2 - x1, x2 - x1 - map_x, x2 - (x1 - map_x))
    y_disp = get_displacement(y2 - y1, y2 - y1 - map_y, y2 - (y1 - map_y))
    return x_disp, y_disp