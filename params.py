
APP_RUNNING = True
ENABLE_VISUALIZATION = True
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

MAP_SIZE_X = 800
MAP_SIZE_Y = 600

NUM_FISHES = 10
FOOD_SPAWN_RATE = 1

SEARCH_RADIUS_MIN = 10
SEARCH_RADIUS_MAX = 100

ROAMING_SPEED_MIN = 1
ROAMING_SPEED_MAX = 100

SEEKING_SPEED_MIN = 1
SEEKING_SPEED_MAX = 100

FISH_SIZE_MIN = 1
FISH_SIZE_MAX = 100

# perhaps move the min and maxes into here too
# then we could apply the mins and maxes to the genetic trait values
TRAIT_LIST = [
    'search_radius',
    'roaming_speed',
    'seeking_speed',
    'size'
]
VARIATION = 0.05