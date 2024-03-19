import pygame
from pygame.locals import *
import random 

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, gap, speed):
        super().__init__()
        self.image = pygame.image.load('./img/pipe.png')
        self.rect = self.image.get_rect()
        self.gap = gap
        self.speed = speed
        
        #position 1 thì lên top, -1 thì xuống dưới bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) # Lật ngược
            self.rect.bottomleft = [x, y - int(self.gap/2)] # Cách
        if position == -1:
            self.rect.topleft = [x, y + int(self.gap/2)] # Cách
        
    def update(self, gameOver):
        if not gameOver:
            self.rect.x -= self.speed # Cập nhật speed
            if self.rect.right < 0: # Quá tọa độ x < 0 thì xóa
                self.kill()