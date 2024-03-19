import pygame
from pygame.locals import *

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Tải ảnh cho các nút menu và giảm kích thước chúng xuống 2 lần
        self.start_img = pygame.image.load('./img/entergame.png')
        self.music_img = pygame.image.load('./img/music.png')
        self.exit_img = pygame.image.load('./img/thoatgame.png')
        # Lưu trữ các ảnh trong một list
        self.menu_images = [self.start_img, self.music_img, self.exit_img]
        self.selected_item = 0
        self.scale_factor = 1.1  # Tỷ lệ để tăng kích thước ảnh được chọn
        # Font và văn bản
        self.font = pygame.font.SysFont('Roboto', 24)
        self.start_text = "Click mui ten len xuong va enter"
        
    def draw(self, screen):
        text_surface = self.font.render(self.start_text, True, (0, 0, 255))
        # Vẽ văn bản trên nút start, ở vị trí 1/3 chiều cao màn hình
        screen.blit(text_surface, (200, 200))
        for i, img in enumerate(self.menu_images):
            img_rect = img.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + i * 70))
            if i == self.selected_item:
                # Tăng kích thước ảnh được chọn
                scaled_img = pygame.transform.scale(img, (int(img_rect.width * self.scale_factor), int(img_rect.height * self.scale_factor)))
                scaled_img_rect = scaled_img.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + i * 70))
                screen.blit(scaled_img, scaled_img_rect)
            else:
                screen.blit(img, img_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_images)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_images)
            elif event.key == pygame.K_RETURN:
                if self.selected_item == 0:  # Start
                    return "start"
                elif self.selected_item == 1:  # Music
                    return "music"
                elif self.selected_item == 2:  # Exit
                    return "exit"
        return None
