
APP_RUNNING = True
ENABLE_GRAPHICS = True
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

MAP_SIZE_X = 800
MAP_SIZE_Y = 600

NUM_FISHES = 10
NUM_FOOD = 2

SEARCH_RADIUS_MIN = 10     #default 10
SEARCH_RADIUS_MAX = 100    #default 100

ROAMING_SPEED_MIN = 1       #default 1
ROAMING_SPEED_MAX = 10      #default 10

SEEKING_SPEED_MIN = 1       #default 1
SEEKING_SPEED_MAX = 10      #default 10

FISH_SIZE_MIN = 0.3         #default 0.3
FISH_SIZE_MAX = 2           #default 2

FOOD_SPAWN = True
FOOD_SPAWN_RATE = 30        #default 30
FOOD_SPAWN_VARIANCE = 10    #default 10

# perhaps move the min and maxes into here too
# then we could apply the mins and maxes to the genetic trait values
TRAIT_LIST = [
    'search_radius',
    'roaming_speed',
    'seeking_speed',
    'size'
]
VARIATION = 0.01