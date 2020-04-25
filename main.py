import random
import pygame
import params
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

    # call fish forth unto thy destiny
    for fishy in fish_map.fish:
        fishy.act(fishy)

    # updates entire display
    pygame.display.flip()

