from fish_map import MAP, Fish_map
from fish import Fish
import params
import random
import csv
import copy

def initialize_random():
    # initialize fish_map fish_list
    for i in range(params.NUM_FISHES):
        traits = {
            'search_radius' : random.uniform(params.SEARCH_RADIUS_MIN, params.SEARCH_RADIUS_MAX),
            'roaming_speed' : random.uniform(params.ROAMING_SPEED_MIN, params.ROAMING_SPEED_MAX),
            'seeking_speed' : random.uniform(params.SEEKING_SPEED_MIN, params.SEEKING_SPEED_MAX),
            'size' : random.uniform(params.FISH_SIZE_MIN, params.FISH_SIZE_MAX)
        }
        MAP.add_fish(Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 200, traits))
        print(MAP.fish_list[i])

# wrong way to split in half, fix this later
def initialize_import(old_fish_map_input):
    old_fish_map = copy.deepcopy(old_fish_map_input)
    old_dead_list = old_fish_map.dead_list
    old_dead_list.sort(key=lambda fish: fish['fitness'])
    for i, fish in enumerate(old_dead_list):
        if i < len(old_dead_list)/2:
            traits = {}
            for trait in params.TRAIT_LIST:
                traits[trait] = fish['traits'][trait] + params.VARIATION*random.uniform(-1, 1)
            MAP.add_fish(Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 200, traits))
        else:
            MAP.add_fish()