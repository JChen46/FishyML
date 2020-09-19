from fish import Fish
import params
import random
import csv
import copy

def initialize_random(map_input):
    # initialize fish_map fish_list
    for _ in range(params.NUM_FISHES):
        map_input.add_fish(None)
        # print(map_input.fish_list[i])
    
    # initialize fish_map food_list
    for _ in range(params.NUM_FOOD):
        map_input.add_food(None)

# wrong way to split in half, fix this later
def initialize_import(old_fish_map_input, map_input):
    old_fish_map = copy.deepcopy(old_fish_map_input)
    old_dead_list = old_fish_map.dead_list
    old_dead_list.sort(key=lambda fish: fish['fitness'])
    for i, fish in enumerate(old_dead_list):
        if i < len(old_dead_list)/2:
            traits = {}
            for trait in params.TRAIT_LIST:
                traits[trait] = fish['traits'][trait] + params.VARIATION*random.uniform(-1, 1)
            map_input.add_fish(Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 200, traits))
        else:
            map_input.add_fish(None)