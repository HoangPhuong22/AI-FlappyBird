import pygame
from pygame.locals import *

class Background:
    def __init__(self, image, width, height):
        # Tải hình ảnh từ đường dẫn
        self.image = pygame.image.load(image)
        # Thay đổi kích thước hình ảnh
        self.image = pygame.transform.scale(self.image, (width, height))
        
    def draw(self, screen):
        # Vẽ hình ảnh lên màn hình
        screen.blit(self.image, (0, 0))
       