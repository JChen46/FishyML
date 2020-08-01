import random
from fish_map import MAP, reset_fish_map
import pygame
import params
from write_fish import write_fish
import initialize

pygame.init()

screen = pygame.display.set_mode((params.WINDOW_WIDTH, params.WINDOW_HEIGHT))

clock = pygame.time.Clock()
count = 0

# # initalize all fish/food entities
# print(params.NUM_FISHES)
# params.NUM_FISHES = 123
# initialize.testprint()

screen.fill((255, 255, 255))
pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75) # args(surface instance, (R,G,B), )

while params.APP_RUNNING:
    dt = clock.tick(30) * 0.01

    # check if user closes out of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            params.APP_RUNNING = False

    # check if no more fish, then finish generation
    if(len(MAP.fish_list) == 0):
        write_fish(MAP) # writes fish stats to file
        initialize_import(MAP)

    # call fish forth unto thy destiny
    for fishy in MAP.fish_list:
        fishy.act()

    # updates entire display
    pygame.display.flip()

