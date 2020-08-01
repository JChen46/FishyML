import params
import fish
import random

class Fish_map:
    def __init__(self, size_x, size_y, food_spawn_rate, num_fishes):
        self._size_x = size_x
        self._size_y = size_y
        self._fish_list = []
        self._dead_list = []
        self.food_list = []
        self.food_spawn_rate = food_spawn_rate
    
    @property
    def size_x(self):
        return self._size_x

    @property
    def size_y(self):
        return self._size_y

    @property
    def fish_list(self):
        return self._fish_list

    @property
    def dead_list(self):
        return self._dead_list

    @size_x.setter
    def size_x(self, value):
        self._size_x = value

    @size_y.setter
    def size_y(self, value):
        self._size_y = value

    def add_fish(self, fish):
        self._fish_list.append(fish)

    def move_fish(self, fish): # moves a dead fish from fish_list to dead_list
        self._dead_list.append(fish)
        print('REMOVING FISH ', fish)
        self._fish_list.remove(fish)

    def add_food(self, food):
        self.food_list.append(food)

    def get_fish(self):
        for fish in self.fish_list:
            yield fish

    def get_food(self):
        for food in self.food_list:
            yield food

    # For clearing lists when new generation starts. Might be moved/refactored to ga.py
    def clear_lists(self):
        self._fish_list.clear()
        self.food_list.clear()

MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.FOOD_SPAWN_RATE, params.NUM_FISHES)
def reset_fish_map():
    global MAP
    MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.FOOD_SPAWN_RATE, params.NUM_FISHES)