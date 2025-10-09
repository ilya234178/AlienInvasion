import pygame


class Ship:
    """Класс для управления корабля"""
    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/rocket_small.png')
        self.rect = self.image.get_rect()

        #Каждый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        #сохранение вещественной координаты центра корабля

        #флаги перемещения: начинаем с неподвижного корабля
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Обновляет позицию корабля с учетом флага."""
        #обновляется атрибут х, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
            # движение вверх
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.ship_speed
            # движение вниз
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed



    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней части экрана"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
        