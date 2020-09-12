import math
import fish_map

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

def closer_to_zero(a, b):
    if abs(a) < abs(b):
        return a
    else:
        return b

def get_dir_dist(obj1, obj2):
    x_vect = closer_to_zero(obj2.pos.x - obj1.pos.x, obj2.pos.x - obj1.pos.x - fish_map.MAP.size_x)
    y_vect = closer_to_zero(obj2.pos.y - obj1.pos.y, obj2.pos.y - obj1.pos.y - fish_map.MAP.size_y)
    return math.atan2(y_vect, x_vect), math.sqrt(math.pow(x_vect, 2) + math.pow(y_vect, 2))