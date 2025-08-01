import pygame   # импорт библиотек
from pygame import mixer


class RulesScreen:  # класс для создания экрана с правилами
    def __init__(self, width=800, height=600):  # конструктор класса
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Правила игры")

        # Цвета
        self.colors = {
            'background': (240, 240, 250),
            'panel': (255, 255, 255, 200),
            'border': (200, 200, 200, 220),
            'title': (50, 50, 50),
            'text': (30, 30, 30),
            'button': (100, 200, 100),
            'button_hover': (70, 180, 70)
        }

        # Шрифты
        self.fonts = {
            'title': pygame.font.Font(None, 52),
            'subtitle': pygame.font.Font(None, 44),
            'normal': pygame.font.Font(None, 32),
            'small': pygame.font.Font(None, 24)
        }

    def show_rules(self):   # отображает экран с правилами и возвращает True, если игрок нажал Продолжить
        running = True
        continue_game = False

        # кнопка Продолжить
        button_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)
        button_hover = False

        while running:
            mouse_pos = pygame.mouse.get_pos()  # получаем позицию мыши
            button_hover = button_rect.collidepoint(mouse_pos)  # добавляем ей коллайдер

            for event in pygame.event.get():    # прописываем ивенты
                if event.type == pygame.QUIT:   # выход
                    running = False
                    pygame.quit()
                    return False

                if event.type == pygame.MOUSEBUTTONDOWN:    # нажатие пкм
                    if button_rect.collidepoint(event.pos):
                        continue_game = True
                        running = False

            # Отрисовка
            self.screen.fill(self.colors['background'])

            # Полупрозрачная панель для правил
            rules_panel = pygame.Surface((700, 520), pygame.SRCALPHA)
            pygame.draw.rect(rules_panel, self.colors['panel'], (0, 0, 700, 520), 0, 15)    # rect рисует прямоугольник
            pygame.draw.rect(rules_panel, self.colors['border'], (0, 0, 700, 520), 2, 15)
            self.screen.blit(rules_panel, (self.width // 2 - 350, 50))  # blit выводит на экран

            # Заголовок
            title = self.fonts['title'].render("Правила игры", True, self.colors['title'])
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 70))

            # Текст правил
            rules = [
                "Цель игры: собрать как можно больше монет за 60 секунд!",
                "",
                "Виды монет:",
                "• Жёлтые: +10 очков (обычные)",
                "• Зелёные: +30 очков (редкие)",
                "• Фиолетовые: +50 очков (очень редкие)",
                "• Красные: -20 очков (опасные!)",
                "",
                "Управление: стрелки клавиатуры",
                "Для победы нужно набрать минимум 1000 очков!"
            ]

            for i, line in enumerate(rules):    # вывод правил разными шрифтами, перебирая элементы и их индексы
                if "•" in line:
                    text = self.fonts['small'].render(line, True, self.colors['text'])
                else:
                    text = self.fonts['normal'].render(line, True, self.colors['text'])
                self.screen.blit(text, (self.width // 2 - 330, 150 + i * 35))

            # Кнопка Продолжить
            button_color = self.colors['button_hover'] if button_hover else self.colors['button']
            pygame.draw.rect(self.screen, button_color, button_rect, 0, 10)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2, 10)

            button_text = self.fonts['normal'].render("Продолжить", True, (255, 255, 255))

            self.screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                           button_rect.centery - button_text.get_height() // 2))

            pygame.display.flip()

        return continue_game    # возвращаемся в main