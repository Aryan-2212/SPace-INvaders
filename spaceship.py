import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()
        # Screen dimensions and offset for boundary constraints
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load spaceship image and set its initial position
        self.image = pygame.image.load("Graphics/spaceship.png")
        self.rect = self.image.get_rect(midbottom=((self.screen_width + self.offset) / 2, self.screen_height))

        # Spaceship movement and shooting attributes
        self.speed = 6  # Movement speed
        self.lasers_group = pygame.sprite.Group()  # Group to hold lasers fired by the spaceship
        self.laser_ready = True  # Whether the spaceship can fire a laser
        self.laser_time = 0  # Time when the last laser was fired
        self.laser_delay = 300  # Time delay (in milliseconds) between consecutive laser shots

        # Load laser sound effect
        self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")

    def get_user_input(self):
        """Handles user input for spaceship movement and laser firing."""
        keys = pygame.key.get_pressed()  # Get the current state of all keys

        # Move right if the RIGHT arrow key is pressed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Move left if the LEFT arrow key is pressed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Fire a laser if the SPACE key is pressed and the laser is ready
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False  # Disable laser firing until recharged
            laser = Laser(self.rect.center, 5, self.screen_height)  # Create a laser object
            self.lasers_group.add(laser)  # Add laser to the group
            self.laser_time = pygame.time.get_ticks()  # Record the time of firing
            self.laser_sound.play()  # Play laser firing sound

    def update(self):
        """Updates the spaceship's position, constraints, lasers, and laser recharge."""
        self.get_user_input()  # Handle player input
        self.constrain_movement()  # Keep spaceship within screen boundaries
        self.lasers_group.update()  # Update the positions of lasers
        self.recharge_laser()  # Check if laser can be recharged

    def constrain_movement(self):
        """Restricts the spaceship's movement within the screen boundaries."""
        if self.rect.right > self.screen_width:  # Prevent moving past the right edge
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:  # Prevent moving past the left edge
            self.rect.left = self.offset

    def recharge_laser(self):
        """Recharges the laser after a delay."""
        if not self.laser_ready:  # If laser is not ready
            current_time = pygame.time.get_ticks()  # Get the current time
            if current_time - self.laser_time >= self.laser_delay:  # Check if delay has passed
                self.laser_ready = True  # Recharge the laser

    def reset(self):
        """Resets the spaceship's position and clears its lasers."""
        self.rect = self.image.get_rect(midbottom=((self.screen_width + self.offset) / 2, self.screen_height))  # Reset position
        self.lasers_group.empty()  # Remove all lasers from the group
