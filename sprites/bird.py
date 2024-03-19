import pygame
from pygame.locals import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, bird, scale=False):
        super().__init__()  
        self.images = [] # Mảng lưu hình ảnh
        self.index = 0 # Chỉ số index trong mảng self.images
        self.counter = 0 # Đếm số khung hình 
        for num in range(1, 3):
            img = pygame.image.load(f'./img/{bird}{num}.png')
            self.images.append(img)
        
        # Gán image của pygame
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # Vị trí của chim ban đầu
        self.gravity = 0 # Trọng lực
        self.clicked = False # Biến kiểm tra chuột
        self.path = []
        
    def draw(self, screen):
        bird_group = pygame.sprite.Group()
        bird_group.add(self)
        bird_group.draw(screen)
    def fly(self):
        # Chuyển động chim
        self.counter += 1 # Biến đếm vỗ cánh của chim
        flap_cooldown = 4
        if self.counter > flap_cooldown: # 10 khung hình cập nhật 1 lần ảnh
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images): # Lớn hơn số ảnh thì về 0
                self.index = 0
        # Cập nhật lại image
        self.image = self.images[self.index]
    #Cập nhật
    def updateAI(self):
        if self.path:
            # Cập nhật vị trí của Bird dựa trên đường đi
            next_position = self.path.pop(0)
            # self.rect.y = next_position[1]
            self.gravity = next_position[4] 
            self.rect.y = next_position[1]
            self.fly()
            self.image = pygame.transform.rotate(self.images[self.index], self.gravity * -2)
        else:
            self.gravity += 0.3
            if self.gravity > 8: #Gán bằng 8 ránh trường hợp gravity quá lớn
                self.gravity = 8
            if self.rect.bottom < 540:
                # Chưa chạm đất thì rơi
                self.rect.y += (self.gravity)
                
    def update(self, flying, gameOver):
        #Cập nhật trọng lực của chim

        if flying:
            self.gravity += 0.3
            if self.gravity > 8: #Gán bằng 8 ránh trường hợp gravity quá lớn
                self.gravity = 8
            if self.rect.bottom < 540:
                # Chưa chạm đất thì rơi
                self.rect.y += (self.gravity)
        
        #Kiểm tra game over
        if not gameOver:
            # Nếu chuột trái được nhấn, và biến check chuột bằng False thì cho nhảy
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.gravity = -6
            
            # Chuột không được nhấn thì reset biến chuột về False
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.fly()
            # Xoay chim theo hướng nhảy
            self.image = pygame.transform.rotate(self.images[self.index], self.gravity * -2)
        else:
            # Chết -> chim tông đầu xuống đất
            self.image = pygame.transform.rotate(self.images[self.index], -90)