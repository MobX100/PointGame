import sqlite3  # импорт библиотек
from typing import List, Tuple


class Database: # класс, отвечающий за заполнение базы данных
    def __init__(self, db_name='game_scores.db'):   # конструктор
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self): # функция, создающая таблицу с id, именем, очками
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_score(self, name: str, score: int): # функция добавляющая очки
        cursor = self.conn.cursor()
        # проверяем существующий результат
        cursor.execute('SELECT score FROM scores WHERE name = ?', (name,))
        existing_score = cursor.fetchone()

        if existing_score:  # проверка результата с уже существующим
            if score > existing_score[0]:
                cursor.execute('UPDATE scores SET score = ?, date = CURRENT_TIMESTAMP WHERE name = ?',
                               (score, name))
        else:
            cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        self.conn.commit()

    def get_top_scores(self, limit: int = 5) -> List[Tuple[str, int]]:   # функция, выводящая топ игроков
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()