import pygame
from settings import CHAR_SIZE, PLAYER_SPEED
from animation import import_sprite


class Pac(pygame.sprite.Sprite):
    """Класс Пэк-мана (героя игры)"""
    def __init__(self, row, col):
        super().__init__()
        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)
        self.image = import_sprite("assets/pac/pacman_o.png")
        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pac_speed = PLAYER_SPEED
        self.immune_time = 0
        self.immune = False
        self.directions = {
            'left': (-PLAYER_SPEED, 0),
            'right': (PLAYER_SPEED, 0),
            'up': (0, -PLAYER_SPEED),
            'down': (0, PLAYER_SPEED)
        }
        self.keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
        self.direction = (0, 0)
        # статус
        self.status = "idle"
        self.life = 3
        self.pac_score = 0

    def _is_collide(self, x, y):
        """Метод обработки столкновений"""
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(self.walls_collide_list) == -1:
            return False
        return True

    def move_to_start_pos(self):
        """Метод, обрабатывающий движение на стартовую позицию"""
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y

    def animate(self, pressed_key, walls_collide_list):
        """Метод, обрабатывающий движение персонажа"""
        self.walls_collide_list = walls_collide_list

        for key, key_value in self.keys.items():
            if pressed_key[key_value] and not self._is_collide(*self.directions[key]):
                self.direction = self.directions[key]
                self.status = key if not self.immune else "power_up"
                break
        if not self._is_collide(*self.direction):
            self.rect.move_ip(self.direction)
            self.status = self.status if not self.immune else "power_up"
        if self._is_collide(*self.direction):
            self.status = "idle" if not self.immune else "power_up"

    def update(self):
        """Таймер"""
        self.immune = True if self.immune_time > 0 else False
        self.immune_time -= 1 if self.immune_time > 0 else 0
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
