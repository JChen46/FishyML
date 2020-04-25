import params
import fish
import random

class Fish_map:
    def __init__(self, size_x, size_y, food_spawn_rate, num_fishes):
        self.size_x = size_x
        self.size_y = size_y
        self.fish_list = []
        self.food_list = []
        self.food_spawn_rate = food_spawn_rate
    
    @property
    def size_x(self):
        return self.size_x

    @property
    def size_y(self):
        return self.size_y

    def add_fish(self, fish):
        self.fish.append(fish)

    def add_food(self, food):
        self.food.append(food)

    def get_fish(self):
        for fish in self.fish:
            yield fish

    def get_food(self):
        for food in self.food:
            yield food

MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.FOOD_SPAWN_RATE, params.NUM_FISHES)
print('goo goo gaa gaa')