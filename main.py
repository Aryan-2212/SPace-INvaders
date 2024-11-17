import pygame, sys
from spaceship import Spaceship
from lasers import Laser

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
GREY = (29, 29, 27)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SPace INvaders") # Set screen size

clock = pygame.time.Clock() # to control frame rate of game

spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

# laser=Laser(),
laser_group= pygame.sprite.Group()
# laser_group.add(laser)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    spaceship_group.update()

    # drawing
    screen.fill(GREY)
    spaceship_group.draw(screen)
    spaceship_group.sprite.lasers_group.draw(screen)

    # Refresh rate
    pygame.display.update()
    clock.tick(60)
