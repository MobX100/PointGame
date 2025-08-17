import pygame    # импрот библиотек
from dataBase import Database   # импортируем класс DataBase из dataBase.py


class InputScreen:  # класс, реализующий входной экран
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        icon = pygame.image.load('assetStore/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("ALL In: 60 Seconds - Введите имя")

        self.colors = { # словарь цветов
            'background': (240, 240, 250),
            'white': (255, 255, 255),
            'black': (50, 50, 50),
            'gray': (180, 180, 180),
            'light_blue': (200, 230, 255),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192),
            'bronze': (205, 127, 50),
            'red': (255, 100, 100)
        }

        self.fonts = {  # словарь шрифтов
            'title': pygame.font.Font(None, 64),
            'subtitle': pygame.font.Font(None, 48),
            'normal': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 28)
        }

        self.db = Database()

    def show_top_scores(self):  # функция, показывающая топ очков
        top_scores = self.db.get_top_scores()   # берем значения из базы данных
        title = self.fonts['subtitle'].render("Топ игроков:", True, self.colors['black'])
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 130))

        if not top_scores: # если база данных пустая
            no_scores = self.fonts['normal'].render("Пока нет результатов", True, self.colors['gray'])
            self.screen.blit(no_scores, (self.width // 2 - no_scores.get_width() // 2, 230))
        else:
            colors = [  # словарь цветов
                self.colors['gold'],
                self.colors['silver'],
                self.colors['bronze'],
                self.colors['black'],
                self.colors['black']
            ]

            for i, (name, score) in enumerate(top_scores):  # раскрашиваем лучших игроков разными цветами, соответствующие медалям
                if i < len(colors):
                    color = colors[i]
                else:
                    color = self.colors['black']

                score_text = self.fonts['normal'].render(f"{i + 1}. {name}: {score}", True, color)
                self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 180 + i * 40))

    def get_player_name(self):   # функция, получающая имя пользователя
        active = True
        user_text = ""
        input_rect = pygame.Rect(self.width // 2 - 200, 450, 400, 50)

        while active:
            self.screen.fill(self.colors['background'])     # раскрашиваем экран

            # заголовок
            title = self.fonts['title'].render("ALL In: 60 Seconds", True, self.colors['black'])
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

            # показываем топ игроков (выше поля ввода)
            self.show_top_scores()

            # инструкция
            instruction = self.fonts['normal'].render("Введите ваш никнейм:", True, self.colors['black'])
            self.screen.blit(instruction, (self.width // 2 - instruction.get_width() // 2, 400))

            # поле ввода
            pygame.draw.rect(self.screen, self.colors['light_blue'], input_rect, 0, 10)
            pygame.draw.rect(self.screen, self.colors['black'], input_rect, 2, 10)

            text_surface = self.fonts['normal'].render(user_text, True, self.colors['black'])
            self.screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 12))

            # подсказка
            hint = self.fonts['small'].render("Нажмите Enter для начала игры", True, self.colors['gray'])
            self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, 520))

            for event in pygame.event.get():    # отработка событий(ивентов)
                if event.type == pygame.QUIT:   # выход
                    pygame.quit()
                    return None

                if event.type == pygame.KEYDOWN:    # была нажата клавиша
                    if event.key == pygame.K_RETURN:    # enter
                        if user_text.strip():   # вывод
                            active = False
                    elif event.key == pygame.K_BACKSPACE:   # backspace
                        user_text = user_text[:-1]  # стираем последний символ
                    else:
                        if len(user_text) < 20: # отработка исключений (ограничиваем длинну имени пользователя 20-ю символами)
                            user_text += event.unicode  # добавляем символ к имени справва

            pygame.display.flip()   # обновляем экран (чтобы отображались изменения)

        return user_text.strip()    # возвращаем имя