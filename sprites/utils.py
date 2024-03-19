import pygame

class DrawText:
    def __init__(self, font_name, font_size, text, color, x, y):
        """
        Khởi tạo đối tượng DrawText.

        Args:
            font_name (str): Tên font hoặc đường dẫn đến file font.
            font_size (int): Kích thước font.
            text (str): Nội dung văn bản cần vẽ.
            color (tuple): Màu sắc của văn bản (R, G, B).
            x (int): Vị trí x trên màn hình để vẽ văn bản.
            y (int): Vị trí y trên màn hình để vẽ văn bản.
        """
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.color = color
        self.position = (x, y)

    def draw(self, screen):
        """
        Vẽ văn bản lên màn hình.

        Args:
            screen: Đối tượng màn hình được tạo từ pygame.display.set_mode()
        """
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.position)
