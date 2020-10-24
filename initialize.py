from fish import Fish
import params
import random
import csv
import copy

def initialize_random(map_input):
    print('Initializing random fish...')
    # initialize fish_map fish_list
    for _ in range(params.NUM_FISHES):
        map_input.add_fish(None)
        # print(map_input.fish_list[i])
    
    # initialize fish_map food_list
    for _ in range(params.NUM_FOOD):
        map_input.add_food(None)

def ga_half_same_half_random(fish_list, fish_map):
    fish_list.sort(key=lambda fish: fish.fitness)
    for i, fish in enumerate(fish_list):
        if i < len(fish_list)/2:
            traits = {}
            for trait in params.TRAIT_LIST:
                traits[trait] = fish.traits[trait] + params.VARIATION*random.uniform(-1, 1)
            fish_map.add_fish(Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 200, traits))
        else:
            fish_map.add_fish(None)

def ga_offspring_based_on_fitness(fish_list, fish_map):
    fish_list.sort(key=lambda fish: fish.fitness)
    for i, fish in enumerate(fish_list):
        # this loops a certain number of times resulting in first half reproducing
        # based on their fitness scores. higher fitness means more offspring
        for _ in range(round(-8/len(fish_list)*(i - len(fish_list)/2 + 0.5))):
            traits = {}
            for trait in params.TRAIT_LIST:
                traits[trait] = fish.traits[trait] + params.VARIATION*random.uniform(-1, 1)
            fish_map.add_fish(Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 200, traits))

# wrong way to split in half, fix this later
def initialize_import(old_fish_map, map_input):
    print('Initializing imported fish')
    old_dead_list = old_fish_map.dead_list
    #ga_half_same_half_random(old_dead_list, map_input)
    ga_offspring_based_on_fitness(old_dead_list, map_input)