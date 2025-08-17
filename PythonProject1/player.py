import pygame   # импорт библиотек
import time

class Player:   # класс игрока и его конструктор класса __init__
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.x = 400
        self.y = 300
        self.speed = 5
        self.color = (0, 0, 0)
        self.radius = 20
        self.max_health = 3
        self.health = self.max_health
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 1.5  # 1.5 секунды неуязвимости

    def draw(self, screen):
        # рисуем игрока (мерцает при неуязвимости)
        if not self.invincible or time.time() % 0.2 < 0.1:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # рисуем шкалу здоровья
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 40
        bar_height = 8
        x = self.x - bar_width // 2
        y = self.y - self.radius - 10

        # Фон шкалы
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))

        # Здоровье
        health_width = (bar_width / self.max_health) * self.health
        health_color = (0, 255, 0) if self.health > 1 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (x, y, health_width, bar_height))

    def move(self, dx, dy, screen_width, screen_height):  # функция отвечающая за движение игрока
        self.x = max(self.radius, min(screen_width - self.radius, self.x + dx * self.speed))
        self.y = max(self.radius, min(screen_height - self.radius, self.y + dy * self.speed))

    def update_score(self, points): # функция, которая обновляет счет
        self.score += points

    def take_damage(self):
        if self.invincible:
            return False

        self.health -= 1
        self.invincible = True
        self.invincible_start_time = time.time()
        return self.health <= 0

    def update_invincibility(self):
        if self.invincible and time.time() - self.invincible_start_time > self.invincible_duration:
            self.invincible = False

    def get_rect(self): # функция рисующая прямоугольник
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)
