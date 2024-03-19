import pygame
from pygame.locals import *
import random
from ai import gen_path, next_states, build_path
pygame.init()

clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("Bauhaus 93", 60)
white = (0, 0, 255)

# Setup screen
screen_width = 960
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy bird')

#variables
pass_pipe = False
score = 0
ground_sroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 120
pipe_frequency = 1300
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Load and scale images bg
width_bg = screen_width
height_bg = screen_height - 100;
bg = pygame.image.load('./img/bg.jpg')
bg = pygame.transform.scale(bg, (width_bg, height_bg))
# load image ground
ground = pygame.image.load('./img/ground.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img = pygame.image.load(f'./img/bird_blue{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 0
        self.clicked = False
    
        
    def update(self):
        if flying:
            self.vel += 0.3
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 540:   
                self.rect.y += (self.vel)
            #jumb
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -6
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # handle the animation
            self.counter += 1
            flap_cooldown = 4
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load('./img/pipe.png')
        self.rect = self.image.get_rect()
        
        #position 1 is from the top, -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(300, int(screen_height/2))
bird_group.add(flappy)

def sinhTrangthai():
    pass

run = True
while run:
    clock.tick(fps)
    
    #draw background
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    screen.blit(ground, (ground_sroll, 540))
    
    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score = score + 1
                pass_pipe = False
                
    draw_text(str(score), font, white, int(screen_width - 100), int(screen_height - 70)) 
    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        
    
    # check if bird has hit the ground
    if flappy.rect.bottom >= 529:
        flying = False
        game_over = True
        
    if game_over == False:
        
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency and flying==True:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        
        #draw and scroll the ground
        ground_sroll -= scroll_speed
        pipe_group.update()

        if abs(ground_sroll) > 30:
            ground_sroll = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
            
    pygame.display.update()

pygame.quit()
