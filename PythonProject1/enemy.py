import pygame   # импорт библиотек
import random
import math

class Enemy:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 25
        self.color = (200, 50, 50)  # красный цвет
        self.x = random.randint(self.radius, screen_width - self.radius)
        self.y = random.randint(self.radius, screen_height - self.radius)
        self.speed = 3
        self.direction = random.uniform(0, 2 * math.pi)  # случайный начальный угол
        self.change_direction_counter = 0
        self.spikes = 8  # количество шипов

    def move(self):
        # движение в текущем направлении
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed

        # отскок от границ экрана
        if self.x <= self.radius or self.x >= self.screen_width - self.radius:
            self.direction = math.pi - self.direction
        if self.y <= self.radius or self.y >= self.screen_height - self.radius:
            self.direction = -self.direction

        # случайное изменение направления
        self.change_direction_counter += 1
        if self.change_direction_counter > 60:  # меняем направление каждые ~60 кадров
            self.direction += random.uniform(-0.5, 0.5)
            self.change_direction_counter = 0

    def draw(self, screen):
        # рисуем основное тело врага
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # рисуем шипы
        for i in range(self.spikes):
            angle = 2 * math.pi * i / self.spikes
            spike_length = self.radius * 1.5
            end_x = self.x + math.cos(angle) * spike_length
            end_y = self.y + math.sin(angle) * spike_length
            pygame.draw.line(screen, (150, 0, 0), 
                           (self.x + math.cos(angle) * self.radius, 
                            self.y + math.sin(angle) * self.radius),
                           (end_x, end_y), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)