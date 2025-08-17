import pygame   # импорт библиотек
import random


class BaseCoin: # базовый класс (шаблон), имеющий все необходимые функции для наследников
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(20, screen_width - 20)
        self.y = random.randint(20, screen_height - 20)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def respawn(self, screen_width, screen_height): # функция, которая отвечает за появление монеток на экране
        self.x = random.randint(20, screen_width - 20)
        self.y = random.randint(20, screen_height - 20)


class StandardCoin(BaseCoin):   # наследник класса BaseCoin, со своими значениями
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.radius = 10
        self.color = (255, 215, 0)  # золотой
        self.value = 10


class BigCoin(BaseCoin):   # наследник класса BaseCoin, со своими значениями
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.radius = 15
        self.color = (24, 143, 0)  # зелёный
        self.value = 30


class MegaCoin(BaseCoin):   # наследник класса BaseCoin, со своими значениями
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.radius = 20
        self.color = (192, 5, 248)  # фиолетовый
        self.value = 50


class BadCoin(BaseCoin):   # наследник класса BaseCoin, со своими значениями
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.radius = 10
        self.color = (255, 0, 0)  # красный
        self.value = -20