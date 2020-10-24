import random
from fish_map import Fish_map
import pygame
import params
from write_fish import write_fish
from initialize import initialize_random, initialize_import
from copy import deepcopy
import time

pygame.init()

screen = pygame.display.set_mode((params.WINDOW_WIDTH, params.WINDOW_HEIGHT))

clock = pygame.time.Clock()
food_clock = 0
current_food_spawn_rate = params.FOOD_SPAWN_RATE
generation = 1

# # initalize all fish/food entities
# print(params.NUM_FISHES)
# params.NUM_FISHES = 123
# initialize.testprint()

# pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75) # args(surface instance, (R,G,B), )

MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.NUM_FOOD, params.NUM_FISHES)
initialize_random(MAP)
font = pygame.font.SysFont(None, 18)
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (800,600))

while params.APP_RUNNING:
    dt = clock.tick(30) * 0.03
    # check if user closes out of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            params.APP_RUNNING = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            MAP.add_food([pos[0], pos[1], 10, 0]) #add 1 energy food at mouse location

    # screen.fill((28, 46, 153))
    screen.blit(background, background.get_rect())

    # check if no more fish, then finish generation
    if(len(MAP.fish_list) <= 1):
        if(params.ENABLE_GRAPHICS):
            time.sleep(5)
        # kill the last fish
        MAP.move_fish(MAP.fish_list[0])
        write_fish(MAP, generation) # writes fish stats to file
        old_map = deepcopy(MAP)
        MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.NUM_FOOD, params.NUM_FISHES)
        initialize_import(old_map, MAP)
        generation += 1
        clock = pygame.time.Clock()
        current_food_spawn_rate = params.FOOD_SPAWN_RATE
    
    # render the visible dead
    for fishy in MAP.dead_list:
        screen.blit(fishy.sprite.fish_image, fishy.sprite.rect)

    # Spawn food
    if(params.FOOD_SPAWN):
        food_clock += dt
        if(food_clock >= current_food_spawn_rate):
            MAP.add_food(None)
            current_food_spawn_rate += 5
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

