import pygame

class ResetMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_button_image = pygame.image.load('./img/thoatmenu.png')
        self.continue_button_image = pygame.image.load('./img/tieptuc.png')
        # Tính toán vị trí của nút Menu và Tiếp tục để chúng nằm giữa màn hình
        menu_button_rect = self.menu_button_image.get_rect(center=(screen_width // 2, screen_height // 2))
        continue_button_rect = self.continue_button_image.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        
        # Tạo mảng chứa thông tin về các item trong menu
        self.menu_items = [
            {"image": self.menu_button_image, "rect": menu_button_rect, "event": "menu"},
            {"image": self.continue_button_image, "rect": continue_button_rect, "event": "tieptuc"}
        ]
        
        self.selected_item = 0  # Khởi tạo selected_item với giá trị 0
        
    def draw(self, screen):
        # Vẽ các button
        for item in self.menu_items:
            screen.blit(item["image"], item["rect"])
        
        # Scale item được chọn lên 1.1 nếu có
        if self.selected_item is not None:
            selected_item = self.menu_items[self.selected_item]
            scaled_image = pygame.transform.scale(selected_item["image"], (int(selected_item["rect"].width * 1.1), int(selected_item["rect"].height * 1.1)))
            scaled_rect = scaled_image.get_rect(center=selected_item["rect"].center)
            screen.blit(scaled_image, scaled_rect)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Xử lý khi nhấn phím mũi tên lên
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                # Xử lý khi nhấn phím mũi tên xuống
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                # Xác nhận item được chọn và trả về sự kiện tương ứng
                return self.menu_items[self.selected_item]["event"]
        return None
