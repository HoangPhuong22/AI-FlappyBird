import pygame
from pygame.locals import *
import random
from sprites.bird import Bird
from sprites.pipe import Pipe
from sprites.ground import Ground
from sprites.background import Background
from sprites.utils import DrawText
from menu import Menu
from game_option import GameOptions
from ai import gen_path

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Flappy Bird')
        # Set up screen
        self.screen_width = 960
        self.screen_height = 640
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #
        # utils
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.flying = False
        self.gameOver = False
        self.speed = 5
        self.score = 0
        #
        # Font chữ và màu
        self.font = "Verdana"
        self.font_size = 50
        self.color = (0, 0, 255)  
        #
        # bird
        self.bird_group = pygame.sprite.Group()
        self.bird = None
        #
        # background
        self.background = Background('./img/bg.jpg', self.screen_width, self.screen_height - 100)
        #
        # ground
        self.ground = Ground('./img/ground.png')
        #
        # pipe
        self.pipe_group = pygame.sprite.Group()
        self.time_now = pygame.time.get_ticks()
        self.pipe_time = 1500
        self.pipe_last_time = self.time_now - self.pipe_time
        self.pass_pipe = False
        #
        # Menu
        self.menu = Menu(self.screen_width, self.screen_height)
        self.menu_active = True
        self.menu_selection = None
        #
        # Game options
        self.game_options = GameOptions(self.screen_width, self.screen_height)
        self.options_active = False  # Kiểm soát việc hiển thị cửa sổ options
        #
        # AI
        self.find_next_pipe = True
        self.mode = 1
        
    def get_next_pipe(self):
        for pipe in self.pipe_group:
            if self.bird.rect.topright[0] < pipe.rect.left:
                return pipe
        return None
    
    
    def draw(self):
        self.background.draw(self.screen)
        self.pipe_group.draw(self.screen)
        self.ground.draw(self.screen)
        if self.menu_active:
            self.menu.draw(self.screen)
        elif self.options_active:
            self.game_options.draw(self.screen)
        else:
            self.bird_group.draw(self.screen)
            self.draw_score()
            
            
    def handle_event(self, event):
        if self.menu_active:
            self.menu_selection = self.menu.handle_event(event)
            if self.menu_selection == "start":
                self.menu_active = False
                self.options_active = True  # Kích hoạt màn hình chọn options
            elif self.menu_selection == "exit":
                self.running = False
        elif self.options_active:
            selection, mode, bird_game = self.game_options.handle_event(event)
            if selection:
                if selection == "Back":
                    self.options_active = False
                    self.menu_active = True
                else:
                    # Xử lý lựa chọn mức độ khó và bắt đầu trò chơi
                    self.options_active = False
                    self.bird = (Bird(100, int(self.screen_height / 2), bird_game))
                    self.bird_group.add(self.bird)
                    self.mode = mode
                    if(self.mode == 2): self.flying = True
                    # Set difficulty here based on selection
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and self.flying == False and self.gameOver == False:
                self.flying = True
    
    def randomPipe(self):
        #Vẽ Pipe
        gap = 120
        self.time_now = pygame.time.get_ticks()
        if self.time_now - self.pipe_last_time > self.pipe_time and self.flying == True:
            self.pipe_height = random.randint(-100, 100)
            pipe_bottom = Pipe(self.screen_width, int(self.screen_height/2) + self.pipe_height, -1, gap,self.speed)
            pipe_top = Pipe(self.screen_width, int(self.screen_height/2) + self.pipe_height, 1, gap, self.speed)
            self.pipe_group.add(pipe_top)
            self.pipe_group.add(pipe_bottom)
            self.pipe_last_time = self.time_now
        
    def update(self):
        self.ground.update(self.speed, self.gameOver)
        if(self.mode == 1): self.bird_group.update(self.flying, self.gameOver)
        elif self.mode == 2: self.bird.updateAI()
        
        if self.find_next_pipe and self.flying == True:
            next_pipe = self.get_next_pipe()
            if next_pipe:
                path = gen_path(self.bird, next_pipe, self.bird.gravity)
                print('Path: ',len(path))
                self.bird.path = path
                self.find_next_pipe = False
        self.pipe_group.update(self.gameOver)

    def collection(self):
        if self.flying:
            # Va chạm chim với chướng ngại vật và trần
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.bird.rect.top < 0:
                    self.gameOver = True
                    
            # Va chạm chim với đất
            if self.bird.rect.bottom >= 535:
                self.flying = False
                self.gameOver = True
    
    def draw_score(self):
        if len(self.pipe_group) > 0:
            if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left\
                and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right\
                and not self.pass_pipe:
                self.pass_pipe = True
            if self.pass_pipe:
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
                    self.score += 1
                    self.pass_pipe = False
                    self.find_next_pipe = True
            
        draw = DrawText(self.font,self.font_size, f'Score: {self.score}', self.color, self.screen_width - 400, self.screen_height - 80)
        draw.draw(self.screen)
        
        
    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.randomPipe() # Vẽ pipe
            self.update() # Cập nhật các thành phần
            self.draw()    # Vẽ các thành phần game
            self.collection()
            self.draw_score()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                # if event.type == pygame.MOUSEBUTTONDOWN and self.flying == False and self.gameOver == False:
                #     self.flying = True
                self.handle_event(event)
            pygame.display.update()  # Cập nhật toàn bộ nội dung cửa sổ
            
if __name__ == "__main__":
    game = Game()
    game.run()
