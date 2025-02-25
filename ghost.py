import pygame
import random
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED


class Ghost(pygame.sprite.Sprite):
    """Класс призраков"""

    def __init__(self, row, col, color):
        super().__init__()
        self.abs_x = row * CHAR_SIZE
        self.abs_y = col * CHAR_SIZE
        self.rect = pygame.Rect(self.abs_x, self.abs_y, CHAR_SIZE, CHAR_SIZE)
        self.move_speed = GHOST_SPEED
        self.color = pygame.Color(color)
        self.move_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.direction = (0, 0)

        self.img_path = f'assets/ghosts/{color}.png'
        self.image = pygame.image.load(self.img_path)
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)

        # Направления движения
        self.directions = {'left': (-self.move_speed, 0), 'right': (self.move_speed, 0),
                           'up': (0, -self.move_speed), 'down': (0, self.move_speed)}
        self.keys = list(self.directions.keys())

    def move_to_start_pos(self):
        """Метод, обрабатывающий движение на стартовую позицию"""
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y

    def is_collide(self, x, y, walls_collide_list):
        """Метод обработки столкновений"""
        return self.rect.move(x, y).collidelist(walls_collide_list) != -1

    def update(self, walls_collide_list):
        """Метод, обрабатывающий движение призрака"""
        available_moves = [key for key in self.keys if not self.is_collide(*self.directions[key], walls_collide_list)]

        if available_moves:
            if len(available_moves) > 2 or self.direction == (0, 0) or random.random() < 0.6:
                self.direction = self.directions[random.choice(available_moves)]

        if not self.is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)

        # Телепорт при выходе за экран
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0
