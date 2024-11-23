import pygame

class Laser(pygame.sprite.Sprite):
    """Represents a laser fired by the spaceship or alien."""
    def __init__(self, position, speed, screen_height):
        super().__init__()
        # Create a small rectangular surface for the laser
        self.image = pygame.Surface((4, 15))  # Laser dimensions: 4x15 pixels
        self.image.fill((243, 216, 63))  # Fill the laser with a yellow color
        # Position the laser at the given (x, y) coordinates
        self.rect = self.image.get_rect(center=position)
        
        # Laser attributes
        self.speed = speed  # Movement speed of the laser
        self.screen_height = screen_height  # Screen height to determine boundaries

    def update(self):
        """Moves the laser and removes it when out of bounds."""
        self.rect.y -= self.speed  # Move the laser upwards by its speed
        # Remove the laser if it goes off-screen
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()  # Remove the laser sprite from all groups
