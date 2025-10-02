class Settings:
    """Класс для хранения всех настроек игры "Инопланетное вторжение"."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_heigth = 800
        self.bg_color = (0, 0, 255)

        self.ship_speed = 5