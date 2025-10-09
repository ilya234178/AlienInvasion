import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Игра запускается в активном состоянии
        self.game_active = True



    def run_game(self):
        """Запускает основной цикл игры"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
        """Обрабатывает нажатие клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # elif event.key == pygame.KMOD_SHIFT:  #для боковой стрельбы
        #     self._fire_bullet()


    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """Создает новый снаряд и добавляет в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        self.bullets.update()
        #  удаление снарядов вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        # проверка попаданий в пришельцев; при обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()


    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана, с последующим обновлением
        позиций всех ппришельцев во флоте.
        """
        self._check_fleet_edges()
        self.aliens.update()
        # проверка коллизий пришелец-корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # проверить не сталкиваются ли пришельцы с нижним краем экрана
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

        # self._check_bottom_and_respawn()
    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #уменьшение ships_left
            self.stats.ships_left -= 1

            #удаление пришельцев и пуль
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(1)
        else:
            self.game_active = False


    def _create_fleet(self):
        """Создает флот пришельцев."""
        # интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y  = alien_width, alien_height
        while current_y < (self.settings.screen_height - 7 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # конец ряда: сбрасываем значение х и инкрементируем значение у
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        # создание пришельца и вычисление пришельцев в ряду.
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # def _check_bottom_and_respawn(self):
    #     """Если нижний ряд дошёл до края, удалить его и создать новый сверху."""
    #     screen_bottom = self.settings.screen_height
    #
    #     # Находим нижнюю координату самого нижнего пришельца
    #     lowest_y = max(alien.rect.bottom for alien in self.aliens.sprites())
    #
    #     if lowest_y >= screen_bottom:
    #         self._remove_bottom_row()
    #         self._create_top_row()

    # def _remove_bottom_row(self):
    #     """Удаляет нижний ряд пришельцев."""
    #     if not self.aliens:
    #         return
    #
    #     # Определяем нижний ряд (у кого rect.bottom максимально)
    #     max_bottom = max(alien.rect.bottom for alien in self.aliens.sprites())
    #
    #     # Удаляем всех пришельцев из нижнего ряда
    #     for alien in list(self.aliens):
    #         if abs(alien.rect.bottom - max_bottom) < alien.rect.height // 2:
    #             self.aliens.remove(alien)
    #
    # def _create_top_row(self):
    #     """Создаёт один новый ряд пришельцев сверху."""
    #     alien = Alien(self)
    #     alien_width, alien_height = alien.rect.size
    #
    #     # координата y для нового ряда — чуть выше экрана
    #     y_position = alien_height
    #
    #     current_x = alien_width
    #     while current_x < (self.settings.screen_width - 2 * alien_width):
    #         self._create_alien(current_x, y_position)
    #         current_x += 2 * alien_width


    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
