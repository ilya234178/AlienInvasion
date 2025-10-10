class Settings:
    """Класс для хранения всех настроек игры "Инопланетное вторжение"."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 255)

        #Настройки корабля
        self.ship_speed = 5
        self.ship_limit = 3

        #параметры снаряда
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # настройки пришельцев
        self.alien_speed = 1
        self.fleet_drop_speed = 10

        #темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        # fleet_direction = 1 означает движение вправо;а -1 влево
        self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        """Инициализирует настройки изменяющиеся в ходе игры"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale