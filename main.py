import random
from fish_map import Fish_map
import pygame
import params
from write_fish import write_fish
from initialize import initialize_random, initialize_import
import copy

pygame.init()

screen = pygame.display.set_mode((params.WINDOW_WIDTH, params.WINDOW_HEIGHT))

clock = pygame.time.Clock()
food_clock = 0
generation = 1

# # initalize all fish/food entities
# print(params.NUM_FISHES)
# params.NUM_FISHES = 123
# initialize.testprint()

# pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75) # args(surface instance, (R,G,B), )

MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.NUM_FOOD, params.NUM_FISHES)
initialize_random(MAP)
font = pygame.font.SysFont(None, 18)

while params.APP_RUNNING:
    dt = clock.tick(30) * 0.05
    #print(dt)
    # check if user closes out of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            params.APP_RUNNING = False

    screen.fill((28, 46, 153))

    # check if no more fish, then finish generation
    if(len(MAP.fish_list) <= 1):
        old_map = copy.deepcopy(MAP)
        write_fish(old_map, generation) # writes fish stats to file
        MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.NUM_FOOD, params.NUM_FISHES)
        initialize_import(old_map, MAP)
        generation += 1

    # render the visible dead
    for fishy in MAP.dead_list:
        screen.blit(fishy.sprite.fish_image, fishy.sprite.rect)

    # Spawn food
    food_clock += dt
    if(food_clock >= params.FOOD_SPAWN_RATE):
        MAP.add_food(None)
        params.FOOD_SPAWN_RATE += 10
        food_clock = 0 + random.uniform(-params.FOOD_SPAWN_VARIANCE, params.FOOD_SPAWN_VARIANCE) # added variability to food spawn

    # call fish forth unto thy destiny
    for fishy in MAP.fish_list:
        fishy.act(MAP, dt)
        fish_energy_num = font.render('{:.0f}'.format(fishy.energy), True, (0, 0, 0))
        screen.blit(fishy.sprite.fish_image, fishy.sprite.rect)
        text_rect = fish_energy_num.get_rect(center=fishy.sprite.rect.center)
        screen.blit(fish_energy_num, text_rect)

    for food in MAP.food_list:
        food.sprite.draw(screen, MAP, food)

    # DEBUGGING TEXT
    img = font.render('Generation: {}'.format(generation), True, (255, 255, 255))
    screen.blit(img, (20, 20))

    # updates entire display
    pygame.display.flip()

