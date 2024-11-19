import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,screen_width,screen_height,speed):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/enhanced_pixel_ar1t.png")           #loads image png from directory
        self.rect = self.image.get_rect(midbottom=((self.screen_width/2),self.screen_height))
        self.rect.center=[screen_width,screen_height]
        self.speed=speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()

class Alien_Laser(pygame.sprite.Sprite):    
    def __init__(self, x, y,screen_height):
        super().__init__()  # Corrected the super() call syntax
        self.image = pygame.image.load("Graphics/Screenshot 2024-11-19 001152.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.screen_height=screen_height

    def update(self):
        self.rect.y += 1  # Move the bullet down the screen
        if self.rect.top > self.screen_height:  # Check if the bullet is off the screen
            self.kill()  # Remove the bullet if it's off screen

