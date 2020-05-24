import random
from fish_map import MAP
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
pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

while params.APP_RUNNING:
    dt = clock.tick(30) * 0.01

    # check if user closes out of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            params.APP_RUNNING = False

    # check if no more fish, then finish generation
    dead_count = 0
    for fish in MAP.fish_list:
        if(fish.state == 'dead'):
            dead_count += 1
    if(dead_count) > 0:
        write_fish(MAP.fish_list) # writes fish stats to file
        

    # call fish forth unto thy destiny
    for fishy in MAP.fish_list:
        fishy.act(fishy)

    # updates entire display
    pygame.display.flip()

