import pygame


class HealthSystem: # класс, отвечающий за систему HP персонажа
    @staticmethod
    def draw_health_bar(surface, x, y, health, max_health): # функция, отвечающая за отрисовку шкалы здоровья над игроком
        bar_length = 100
        bar_height = 20
        fill = (health / max_health) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)

        health_color = (0, 255, 0) if health > max_health / 2 else (    # цвет шкалы здоровья отличается в зависимости от количества текущего здоровья
            (255, 255, 0) if health > max_health / 4 else (255, 0, 0))

        pygame.draw.rect(surface, health_color, fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)