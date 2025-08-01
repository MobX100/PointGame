import pygame   # импорт библиотек


class Player:   # класс игрока и его конструктор класса __init__
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.x = 400
        self.y = 300
        self.speed = 5
        self.color = (0, 0, 0)
        self.radius = 20

    def draw(self, screen): # отрисовка игрока на поле
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy, screen_width, screen_height):    # функция отвечающая за движение игрока
        self.x = max(self.radius, min(screen_width - self.radius, self.x + dx * self.speed))
        self.y = max(self.radius, min(screen_height - self.radius, self.y + dy * self.speed))

    def update_score(self, points): # функция, которая обновляет счет
        self.score += points

    def get_rect(self): # функция рисующая прямоугольник
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)