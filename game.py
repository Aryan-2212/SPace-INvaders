import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle, grid
from alien import Alien, MysteryShip
from laser import Laser

class Game:
    """Represents the core game logic and structure."""
    def __init__(self, screen_width, screen_height, offset):
        # Screen dimensions and offset for UI
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        # Spaceship setup
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))

        # Obstacles and aliens setup
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1

        # Alien lasers and mystery ship setup
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()

        # Game state
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0

        # Add level tracking
        self.level = 1

        # Load sounds and high score
        self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
        self.load_highscore()
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)  # Loop background music

    def create_obstacles(self):
        """Creates obstacles based on a predefined grid."""
        obstacle_width = len(grid[0]) * 3  # Calculate obstacle width from grid
        gap = (self.screen_width + self.offset - (4 * obstacle_width)) / 5  # Calculate spacing between obstacles
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        """Spawns aliens in rows with specific types based on their position."""
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55

                # Set alien type by row (affects score value)
                alien_type = 3 if row == 0 else (2 if row in (1, 2) else 1)

                alien = Alien(alien_type, x + self.offset / 2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        """Moves aliens horizontally and down if they hit the screen edges."""
        self.aliens_group.update(self.aliens_direction)
        for alien in self.aliens_group:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        """Moves aliens downward by a specified distance."""
        for alien in self.aliens_group:
            alien.rect.y += distance

    def alien_shoot_laser(self):
        """Allows a random alien to shoot a laser."""
        if self.aliens_group:
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        """Spawns a mystery ship."""
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_for_collisions(self):
        """Handles all collision detections in the game."""
        # Check spaceship lasers
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                # Laser hits alien
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()

                # Laser hits mystery ship
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()

                # Laser hits obstacle
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Check alien lasers
        for laser_sprite in self.alien_lasers_group:
            # Alien laser hits spaceship
            if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                laser_sprite.kill()
                self.lives -= 1
                if self.lives == 0:
                    self.game_over()

            # Alien laser hits obstacle
            for obstacle in self.obstacles:
                if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                    laser_sprite.kill()

        # Check aliens colliding with obstacles or spaceship
        for alien in self.aliens_group:
            for obstacle in self.obstacles:
                pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

            if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                self.game_over()
                
        # Check if all aliens are destroyed        
        if not self.aliens_group:
            self.level_up()

    def level_up(self):
        """Handles level progression."""
        self.level += 1
        self.create_aliens()  # Create a new wave of aliens
        self.aliens_direction = 1  # Reset alien movement direction
        self.obstacles = self.create_obstacles()  # Reset obstacles

    def game_over(self):
        """Ends the game."""
        self.run = False

    def reset(self):
        """Resets the game to its initial state."""
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()  # You should implement reset in the Spaceship class or reset manually
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        """Checks and updates the high score."""
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        """Loads the high score from a file."""
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

