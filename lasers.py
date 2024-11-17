import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,screen_width,screen_height,speed):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/enhanced_pixel_ar1t.png")           #loads image png from directory
        self.rect = self.image.get_rect(midbottom=(self.screen_width/2,self.screen_height))
        self.rect.center=[screen_width,screen_height]
        self.speed=speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()
