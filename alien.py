import pygame, random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        # Load the alien image based on its type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        # Set the alien's position based on the given coordinates
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        # Move the alien horizontally based on the direction (-1 for left, 1 for right)
        self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        # Load the mystery ship image
        self.image = pygame.image.load("Graphics/mystery.png")

        # Randomly choose the starting position: left or right of the screen
        x = random.choice([self.offset / 2, self.screen_width + self.offset - self.image.get_width()])
        
        # Set speed based on starting position: move right if starting on the left, or left if starting on the right
        if x == self.offset / 2:
            self.speed = 3
        else:
            self.speed = -3

        # Set the mystery ship's position at the chosen starting point
        self.rect = self.image.get_rect(topleft=(x, 90))

    def update(self):
        # Update the mystery ship's position based on its speed
        self.rect.x += self.speed
        # Remove the mystery ship if it moves off-screen
        if self.rect.right > self.screen_width + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()
