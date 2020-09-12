import params
from fish import Fish
import random
import math

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
        if not fish:
            size_mode = math.sqrt(params.FISH_SIZE_MAX * params.FISH_SIZE_MIN)
            traits = {
                'search_radius' : random.uniform(params.SEARCH_RADIUS_MIN, params.SEARCH_RADIUS_MAX),
                'roaming_speed' : math.exp(random.uniform(math.log(params.ROAMING_SPEED_MIN), math.log(params.ROAMING_SPEED_MAX))),
                'seeking_speed' : random.uniform(params.SEEKING_SPEED_MIN, params.SEEKING_SPEED_MAX),
                'size' : random.triangular(params.FISH_SIZE_MIN, params.FISH_SIZE_MAX, size_mode)
            }
            self._fish_list.append(Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 100, traits))
        else:
            self._fish_list.append(fish)

    def move_fish(self, fish): # moves a dead fish from fish_list to dead_list
        self._dead_list.append(fish)
        # print('REMOVING FISH ', fish)
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