import pygame

class Ground:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.position = 0
        
    def update(self, speed, gameOver):
        if not gameOver:
            self.position -= speed # Di chuyển đất
            if abs(self.position) > 30: # Check
                self.position = 0
      
    def draw(self, screen):
        screen.blit(self.image, (self.position, 540)) # Vẽ đất