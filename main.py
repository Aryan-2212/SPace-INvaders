import pygame, sys, random
from game import Game

# Initialize Pygame
pygame.init()

# Screen dimensions and offsets
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

# Colors (RGB values)
GREY = (29, 29, 27)  # Background color
YELLOW = (243, 216, 63)  # UI elements color

# Load font and create text surfaces
font = pygame.font.Font("Font/monogram.ttf", 40)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Python Space Invaders")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Instantiate the Game class
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

# Define custom events
SHOOT_LASER = pygame.USEREVENT  # Event for aliens shooting lasers
pygame.time.set_timer(SHOOT_LASER, 300)  # Trigger every 300 milliseconds

MYSTERYSHIP = pygame.USEREVENT + 1  # Event for spawning a mystery ship
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))  # Random interval between 4-8 seconds

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Exit the game
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:  # Alien shoots laser
            game.alien_shoot_laser()
        if event.type == MYSTERYSHIP and game.run:  # Spawn mystery ship
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))  # Reset timer for next mystery ship

        # Check for player input (space to reset game)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.run:  # Restart game
            game.reset()

    # Game updates (only when the game is running)
    if game.run:
        game.spaceship_group.update()  # Update spaceship position
        game.move_aliens()  # Move alien group
        game.alien_lasers_group.update()  # Update alien lasers
        game.mystery_ship_group.update()  # Update mystery ship
        game.check_for_collisions()  # Check for collisions between entities
    
    # Update the level surface dynamically
    level_surface = font.render(f"LEVEL: {game.level} ", False, YELLOW)

    # Drawing on the screen
    screen.fill(GREY)  # Fill the screen with background color

    # UI elements
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)  # Outer border
    pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)  # Line separating UI and game area

    # Display level or game over text
    if game.run:
        screen.blit(level_surface, (570, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))

    # Display player lives as spaceship icons
    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += 50

    # Display current score
    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)  # Pad score with zeros
    score_surface = font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))

    # Display high score
    screen.blit(highscore_text_surface, (550, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)  # Pad high score with zeros
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (625, 40, 50, 50))

    # Draw all game objects
    game.spaceship_group.draw(screen)  # Draw spaceship
    game.spaceship_group.sprite.lasers_group.draw(screen)  # Draw spaceship lasers
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)  # Draw obstacles
    game.aliens_group.draw(screen)  # Draw alien group
    game.alien_lasers_group.draw(screen)  # Draw alien lasers
    game.mystery_ship_group.draw(screen)  # Draw mystery ship

    # Update the display
    pygame.display.update()
    clock.tick(60)  # Maintain 60 FPS
