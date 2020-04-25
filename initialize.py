import fish_map
import fish
import params
import random

# initialize fish_map fish_list
for i in range(params.NUM_FISHES):
    traits = {
        'search_radius' : random.uniform(params.SEARCH_RADIUS_MIN, params.SEARCH_RADIUS_MAX),
        'roaming_speed' : random.uniform(params.ROAMING_SPEED_MIN, params.ROAMING_SPEED_MAX),
        'seeking_speed' : random.uniform(params.SEEKING_SPEED_MIN, params.SEEKING_SPEED_MAX),
        'size' : random.uniform(params.FISH_SIZE_MIN, params.FISH_SIZE_MAX)
    }
    fish_map.fish_list[i] = Fish(random.uniform(0, params.WINDOW_WIDTH), random.uniform(0, params.WINDOW_HEIGHT), 200, traits)