import pygame
from pygame.locals import *
from sprites.bird import Bird
class GameOptions:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Verdana", 40)
        self.options_items = ["Easy", "Medium", "Hard", "Back"]
        self.selected_item = 0
        self.options_color = (255, 255, 255)
        self.selected_color = (0, 255, 0)

        # Load images for buttons
        self.button_images = [pygame.image.load('./img/easy.png'),
                              pygame.image.load('./img/medium.png'),
                              pygame.image.load('./img/hard.png'),
                              pygame.image.load('./img/back.png')]

        # Mũi tên
        self.arrow_left_image = pygame.image.load('./img/arrow_left.png')
        self.arrow_right_image = pygame.image.load('./img/arrow_right.png')

        # Chế độ chơi
        self.play_modes = [1, 2]
        self.play_mode = 0
        self.play_mode_images = [pygame.image.load('./img/choi1minh.png'),
                                 pygame.image.load('./img/AItuchoi.png'),]
        
        # Chọn bird
        self.bird_types = ["bird_pink", "bird_green", "bird_yellow", "bird_super", "bird_blue"]  
        self.bird_objects = [Bird(0, 0, bird_type) for bird_type in self.bird_types]  # Tạo đối tượng Bird cho mỗi loại
        self.bird_index = 0

        self.font = pygame.font.SysFont('Roboto', 24)
        self.text1 = "Click mui ten len xuong de chon muc do, click 2 nut A và S chon chim"
        self.text2 = "click mui ten trai phai de chon cach choi, enter de vao game"
    def draw(self, screen):
        text_surface = self.font.render(self.text1, True, (0, 0, 255))
        screen.blit(text_surface, (50, 100))
        text_surface = self.font.render(self.text2, True, (0, 0, 255))
        screen.blit(text_surface, (50, 150))
        for i, image in enumerate(self.button_images):
            button_rect = image.get_rect(center=(self.screen_width // 4, 200 + i * 100))
            if i == self.selected_item:
                # Scale the image by 1.1
                scaled_image = pygame.transform.scale(image, (int(button_rect.width * 1.1), int(button_rect.height * 1.1)))
                scaled_rect = scaled_image.get_rect(center=(self.screen_width // 4, 200 + i * 100))
                screen.blit(scaled_image, scaled_rect)
            else:
                screen.blit(image, button_rect)

        # Draw play mode options with arrows
        play_mode_image = self.play_mode_images[self.play_mode]
        mode_rect = play_mode_image.get_rect(center=(3 * self.screen_width // 4, 2*self.screen_height // 3))
        screen.blit(play_mode_image, mode_rect)
        screen.blit(self.arrow_left_image, (mode_rect.left - 80, mode_rect.centery - self.arrow_left_image.get_height() // 2))
        screen.blit(self.arrow_right_image, (mode_rect.right + 20, mode_rect.centery - self.arrow_right_image.get_height() // 2))

        # Draw bird
        # Vẽ loại chim được chọn
        selected_bird = self.bird_objects[self.bird_index]
        selected_bird.fly()  # Cập nhật trạng thái vỗ cánh
        # Đặt lại vị trí để vẽ chim ở trung tâm mong muốn
        selected_bird.rect.center = (3 * self.screen_width // 4, 2 * self.screen_height // 3 - 100)
        # Vẽ chim lên màn hình tùy chọn
        selected_bird.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.options_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.options_items)
            elif event.key == pygame.K_LEFT:
                # Change play mode only
                self.play_mode = (self.play_mode - 1) % len(self.play_modes)
            elif event.key == pygame.K_RIGHT:
                # Change play mode only
                self.play_mode = (self.play_mode + 1) % len(self.play_modes)
            elif event.key == pygame.K_a:  # Sang trái
                self.bird_index = (self.bird_index - 1) % len(self.bird_types)
            elif event.key == pygame.K_s:  # Sang phải
                self.bird_index = (self.bird_index + 1) % len(self.bird_types)
            elif event.key == pygame.K_RETURN:
                # Might need to handle the selected option here
                return self.options_items[self.selected_item], self.play_modes[self.play_mode], self.bird_types[self.bird_index]
        return None, None, None
