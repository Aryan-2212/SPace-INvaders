import pygame, sys, random
from game import Game 
from lasers import Laser
from lasers import Alien_Laser
pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET=50
alien_cooldown =1000
last_alien_shot = pygame.time.get_ticks()
GREY = (29, 29, 27)
YELLOW= (243,216,63)
font=pygame.font.Font("font/monogram.ttf",40)
level_surface= font.render("LEVEL 01",False,YELLOW)
game_over_surface= font.render("GAME OVER",False,YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH+OFFSET, SCREEN_HEIGHT+2*OFFSET))
pygame.display.set_caption("SPace INvaders") # Set screen size

background = pygame.image.load("Graphics/bg.png")

def draw_bg():
	screen.blit(background, (0, 0))

clock = pygame.time.Clock() # to control frame rate of game

game = Game(SCREEN_WIDTH,SCREEN_HEIGHT,OFFSET)

# #spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)
# #spaceship_group = pygame.sprite.GroupSingle()
##spaceship_group.add(spaceship)

##laser_group= pygame.sprite.Group()
alien_laser_group=pygame.sprite.Group()
MYSTERYSHIP=pygame.USEREVENT+1
SHOOT_LASER=pygame.USEREVENT
pygame.time.set_timer(MYSTERYSHIP,random.randint(4000,8000))

while True:
    draw_bg()
    time_now=pygame.time.get_ticks()
    if time_now-last_alien_shot >alien_cooldown and len(alien_laser_group) < 5 and len(game.aliens_group) > 0:
         attacking_alien = random.choice(game.aliens_group.sprites())
         alien_laser=Alien_Laser(attacking_alien.rect.centerx, attacking_alien.rect.bottom,SCREEN_HEIGHT )
         alien_laser_group.add(alien_laser)
         last_alien_shot= time_now 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MYSTERYSHIP and game.run:
             game.create_mystery_ship()
             pygame.time.set_timer(MYSTERYSHIP,random.randint(4000,8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run==False:
             game.reset()

    if game.run: 
           game.spaceship_group.update()
           game.move_aliens()
           alien_laser_group.update()
           game.mystery_ship_group.update()
           game.check_for_collisions()

    # game.alien_shoot_laser()
    # game.alien_lasers_group.update()
    # alien_laser_group.update()
    # #spaceship_group.update()

    # drawing
    pygame.draw.rect(screen,YELLOW,(10,10,780,780),2,0,60,60,60,60)
    pygame.draw.line(screen,YELLOW,(25,710),(775,710),3)
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    alien_laser_group.draw(screen)
    if game.run:
         screen.blit(level_surface,(570,740,50,50))
    else:
         screen.blit(game_over_surface,(570,740,50,50))
    x=50
    for life in range(game.lives):
         screen.blit(game.spaceship_group.sprite.image,(x,720))   
         x+=50  
    for obstacle in game.obstacles:
         obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen )

    # Refresh rate
    pygame.display.update()
    clock.tick(60)
