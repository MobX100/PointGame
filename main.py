import pygame   # импорт библиотек
import sys
import math
import random
from player import Player
from rules import RulesScreen
from coin import StandardCoin, BigCoin, MegaCoin, BadCoin
from inputScreen import InputScreen
from dataBase import Database
from enemy import Enemy


class Game: # основной класс, отвечающий за игру
    def __init__(self):
        pygame.init() # инициализация pygame
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # создаем экран
        pygame.display.set_caption("ALL In: 60 Seconds") # задаем название игре
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.enemies = [Enemy(self.screen_width, self.screen_height) for _ in range(5)]  # 2 врага
        self.game_over = False

        # игровые параметры
        self.game_time = 60    # время
        self.target_score = 1000    # необходимые для победы очки
        self.coins = []
        self.db = Database()

        # получаем имя игрока
        self.input_screen = InputScreen(self.screen_width, self.screen_height)
        player_name = self.input_screen.get_player_name()

        if not player_name:
            pygame.quit()
            sys.exit()

        rules_screen = RulesScreen(self.screen_width, self.screen_height) # задаем экран правил
        if not rules_screen.show_rules():
            pygame.quit()
            sys.exit()

        self.player = Player(player_name)    # получаем имя игрока из player.py
        self.spawn_coins(10)  # начальное количество монеток

        # таймер
        self.start_time = pygame.time.get_ticks()
        self.time_left = self.game_time
        self.game_active = True

    def spawn_coins(self, count):   # функция создает монетки с разными вероятностями появления
        coin_types = [StandardCoin, BigCoin, MegaCoin, BadCoin]
        # вероятности: 70%, 20%, 5%, 5%
        weights = [0.70, 0.20, 0.05, 0.05]

        for _ in range(count):
            coin_class = random.choices(coin_types, weights=weights)[0]
            self.coins.append(coin_class(self.screen_width, self.screen_height))

    def check_collisions(self): # функция обрабатывает столкновения с монетками
        player_rect = self.player.get_rect()
        for coin in self.coins[:]:
            if player_rect.colliderect(coin.get_rect()):
                self.player.update_score(coin.value)
                self.coins.remove(coin)
                self.spawn_coins(1)

    def update_timer(self): # функция обновляет игровой таймер
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        self.time_left = max(0, self.game_time - elapsed)
        return self.time_left > 0

    def show_game_info(self):   # функция отображает полупрозрачную панель с информацией
        # создаем поверхность с прозрачностью
        info_panel = pygame.Surface((300, 130), pygame.SRCALPHA)
        pygame.draw.rect(info_panel, (240, 240, 250, 200), (0, 0, 300, 130), 0, 10)
        pygame.draw.rect(info_panel, (200, 200, 200, 220), (0, 0, 300, 130), 2, 10)
        self.screen.blit(info_panel, (10, 10))

        # текст информации
        texts = [
            f"Игрок: {self.player.name}",
            f"Счет: {self.player.score}",
            f"Время: {self.time_left} сек",
            f"Цель: {self.target_score}"
        ]

        for i, text in enumerate(texts):
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, 20 + i * 30))

    def show_game_over(self, won):  # функция отображает экран завершения игры
        # полупрозрачный фон
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((240, 240, 250, 220))
        self.screen.blit(overlay, (0, 0))

        # заголовок
        title_font = pygame.font.Font(None, 72)
        if won:
            title = title_font.render("Победа!", True, (0, 150, 0))
        else:
            title = title_font.render("Конец игры", True, (200, 0, 0))

        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80))

        # счет игрока
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Ваш счет: {self.player.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 170))

        # топ игроков
        top_panel = pygame.Surface((400, 270), pygame.SRCALPHA)
        pygame.draw.rect(top_panel, (240, 240, 250, 200), (0, 0, 400, 270), 0, 10)
        pygame.draw.rect(top_panel, (200, 200, 200, 220), (0, 0, 400, 270), 2, 10)
        self.screen.blit(top_panel, (self.screen_width//2 - 200, 230))

        top_title = score_font.render("Лучшие игроки:", True, (0, 0, 0))
        self.screen.blit(top_title, (self.screen_width//2 - top_title.get_width()//2, 240))

        top_scores = self.db.get_top_scores()   # цвета для окраски первого, второго, третьего и т.д. мест
        colors = [
            (255, 215, 0),  # золотой
            (192, 192, 192),  # серебряный
            (205, 127, 50),  # бронзовый
            (50, 50, 50),  # черный
            (50, 50, 50)  # черный
        ]

        for i, (name, score) in enumerate(top_scores):
            color = colors[i] if i < len(colors) else (50, 50, 50)
            score_text = self.font.render(f"{i + 1}. {name}: {score}", True, color)
            self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 310 + i * 40))

        # инструкция
        hint_font = pygame.font.Font(None, 36)
        hint_text = hint_font.render("Нажмите R для рестарта или Q для выхода", True, (100, 100, 100))
        self.screen.blit(hint_text, (self.screen_width // 2 - hint_text.get_width() // 2, 540))

        pygame.display.flip()   # обновляем экран

        waiting = True
        while waiting:
            for event in pygame.event.get():    # отработка ивентов (событий)
                if event.type == pygame.QUIT:   # выход
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:   # нажата клавиша
                    if event.key == pygame.K_r:   # нажата R
                        return True
                    elif event.key == pygame.K_q:   # нажата Q
                        pygame.quit()
                        sys.exit()
            self.clock.tick(60)  # ограничиваем FPS

        return False

    def run(self):
        running = True  # bool-переменная

        while running:
            for event in pygame.event.get():    # отработка ивентов (событий)
                if event.type == pygame.QUIT:   # выход
                    running = False

            if self.game_active and not self.game_over:
                # обновляем неуязвимость игрока
                self.player.update_invincibility()

                # движение врагов
                for enemy in self.enemies:
                    enemy.move()

                    # проверка столкновений (только если игрок не неуязвим)
                    if not self.player.invincible and self.player.get_rect().colliderect(enemy.get_rect()):
                        if self.player.take_damage():
                            self.game_over = True
                            self.game_active = False
                            # Показываем экран завершения игры
                            if self.show_game_over(False):
                                # Рестарт игры
                                return True
                            else:
                                return False

                        # отталкивание игрока
                        push_direction = math.atan2(self.player.y - enemy.y,
                                                    self.player.x - enemy.x)
                        self.player.x += math.cos(push_direction) * 30
                        self.player.y += math.sin(push_direction) * 30

                # управление
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_LEFT]: dx = -1
                if keys[pygame.K_RIGHT]: dx = 1
                if keys[pygame.K_UP]: dy = -1
                if keys[pygame.K_DOWN]: dy = 1

                self.player.move(dx, dy, self.screen_width, self.screen_height)
                self.check_collisions()

                # обновляем таймер
                self.game_active = self.update_timer()

                # проверяем условие победы/поражения
                if not self.game_active:
                    icon = pygame.image.load('assetStore/icon.png')
                    pygame.display.set_icon(icon)
                    pygame.display.set_caption("ALL In: 60 Seconds - Результаты")
                    won = self.player.score >= self.target_score
                    if won:
                        self.db.add_score(self.player.name, self.player.score)

                    if self.show_game_over(won):
                        # рестарт игры
                        return True
                    else:
                        return False

            # отрисовка
            pygame.display.set_caption("ALL In: 60 Seconds")
            icon = pygame.image.load('assetStore/icon.png')
            pygame.display.set_icon(icon)
            self.screen.fill((66, 170, 255))

            # рисуем монетки
            for coin in self.coins:
                coin.draw(self.screen)

            # рисуем врагов
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # рисуем игрока
            self.player.draw(self.screen)

            # отображаем информацию
            self.show_game_info()

            pygame.display.flip()
            self.clock.tick(60) # количество кадров/с

        pygame.quit()   # выход


if __name__ == "__main__":
    while True:
        game = Game()
        should_restart = game.run()
        if not should_restart:
            break