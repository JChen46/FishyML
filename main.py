import random
from fish_map import Fish_map
import pygame
import params
from write_fish import write_fish
from initialize import initialize_random, initialize_import

pygame.init()

screen = pygame.display.set_mode((params.WINDOW_WIDTH, params.WINDOW_HEIGHT))

clock = pygame.time.Clock()
count = 0

# # initalize all fish/food entities
# print(params.NUM_FISHES)
# params.NUM_FISHES = 123
# initialize.testprint()

# pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75) # args(surface instance, (R,G,B), )

MAP = Fish_map(params.MAP_SIZE_X, params.MAP_SIZE_Y, params.NUM_FOOD, params.NUM_FISHES)

while params.APP_RUNNING:
    dt = clock.tick(30) * 0.01
    #print(dt)
    # check if user closes out of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            params.APP_RUNNING = False

    screen.fill((28, 46, 153))

    # check if no more fish, then finish generation
    if(len(MAP.fish_list) == 0):
        write_fish(MAP) # writes fish stats to file
        # initialize_import(MAP, MAP)
        initialize_random(MAP)

    # render the visible dead
    for fishy in MAP.dead_list:
        screen.blit(fishy.sprite.fish_image, fishy.sprite.rect)

    # call fish forth unto thy destiny
    for fishy in MAP.fish_list:
        fishy.act(MAP, dt)
        screen.blit(fishy.sprite.fish_image, fishy.sprite.rect)

    for food in MAP.food_list:
        food.sprite.draw(screen, MAP, food)

    # updates entire display
    pygame.display.flip()

