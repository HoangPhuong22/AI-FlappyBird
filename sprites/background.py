# import pygame
# from pygame.locals import *

# class Background:
#     def __init__(self, image, width, height):
#         # Tải hình ảnh từ đường dẫn
#         self.image = pygame.image.load(image)
#         # Thay đổi kích thước hình ảnh
#         self.image = pygame.transform.scale(self.image, (width, height))
        
#     def draw(self, screen):
#         # Vẽ hình ảnh lên màn hình
#         screen.blit(self.image, (0, 0))
import pygame
from pygame.locals import *

class Background:
    def __init__(self, image, width, height, speed = 1):
        # Tải hình ảnh từ đường dẫn
        self.image = pygame.image.load(image)
        # Thay đổi kích thước hình ảnh
        self.image = pygame.transform.scale(self.image, (width, height))
        # Lưu lại tốc độ di chuyển của background
        self.speed = speed
        # Khởi tạo vị trí ban đầu của background
        self.x = 0
        
    def update(self, gameOver):
        if not gameOver:
            self.x -= self.speed
            # Kiểm tra nếu vị trí của background ra khỏi màn hình, thì reset vị trí về bên phải
            if self.x <= -self.image.get_width():
                self.x = 0
    
    def draw(self, screen):
        # Vẽ hình ảnh background lên màn hình tại vị trí x, y
        screen.blit(self.image, (self.x, 0))
        # Nếu background vẫn chưa vẽ hết trên màn hình, vẽ thêm một bức hình nữa để tạo hiệu ứng chuyển động liên tục
        if self.x < 0:
            screen.blit(self.image, (self.x + self.image.get_width(), 0))
