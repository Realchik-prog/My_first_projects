import sqlite3
from pathlib import Path

class LibraryManagerApp:
    def __init__(self):
        # Устанавливаем файл с таблицей
        self.FILE: Path = Path(__file__).parent / 'library.db'
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT
                )
            """)
            
    def add_book(self) -> None:
        # Ввод данных о книге
        author = input('Введите автора: ').strip()
        title = input('Введите название: ').strip()
        # Проверка, что книга ещё не добавлена
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT title, author FROM books")
            for book in cursor.fetchall():
                if (title.lower(), author.lower()) == (book[0].lower(), book[1].lower()):
                    print()
                    print("Данная книга уже существует")
                    return None
        # Продолжение ввода данных
        try:
            year = int(input('Введите год издания: '))
        except ValueError:
            year = 'год не указан'
        genre = input('Введите жанр: ').strip().title()
        if genre.lower() == 'нет' or genre == '0' or genre == '':
            genre = 'Жанр не указан'
            
                
        # Запись книги в базу данных
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)",
                (title, author, year, genre)
            )
            cursor.execute("SELECT id FROM books WHERE title = ? AND author = ?",
                           (title, author))
            print(f'\nКнига добавлена! (ID: {cursor.fetchone()[0]})')
        
    def view_books(self) -> None:
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            # Проверка, есть ли книги
            cursor.execute("SELECT id, title, author, year, genre FROM books")
            if cursor.fetchall() != []:
                # Вывод книг
                print("Список всех книг:")
                cursor.execute("SELECT id, title, author, year, genre FROM books")
                author_books = (book for book in cursor.fetchall())
                for book in author_books:
                    print(f'{book[0]}) {book[2]} "{book[1]}", {book[4]}, {book[3]}')
            else:
                print('Нет ни одной книги')
                
    def search_books(self):
        # Проверка, есть ли книги
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM books")
            all_id = cursor.fetchall()
        if all_id == []:
            print("Нет ни одной книги")
            return None
        # Выбор режима поиска
        while True:
            print("""Как вы хотите найти книги?
1. По названию
2. По автору
3. По году издания
4. По жанру\n""")
            mode = input("> ").strip()
            print()
            if mode in ['1', '2', '3', '4']:
                break
            print('Команда не опознана')
            print()
        mode = int(mode)
        if mode==1:
            element = input('Введите название: ').strip().lower()
        elif mode==2:
            element = input('Введите автора: ').strip().lower()
        elif mode==3:
            element = input('Введите год издания: ').strip().lower()
        elif mode==4:
            element = input('Введите жанр: ').strip().lower()
        else:
            raise ValueError
        
        print()
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            # Вывод книг
            cursor.execute("SELECT id, title, author, year, genre FROM books")
            all_books = (book for book in cursor.fetchall() if element in str(book[mode]).lower())
            books_found = False
            for book in all_books:
                if not books_found:
                    print("Найдены:")
                print(f'{book[0]}) {book[2]} "{book[1]}", {book[4]}, {book[3]}')
                books_found = True
            if not books_found:
                print('Ничего не нашлось')
    def update_year(self) -> None:
        # Берём id, если книги есть
        id = self.input_id()
        if id is False:
            return None
    
        # Ввод нового года издания
        while True:
            try:
                year = int(input("Введите новый год издания: "))
                break
            except ValueError:
                print('Неправильный ввод')
                
        # Обновление года издания
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE books SET year = ? WHERE id = ?",
                           (year, id))
        print()
        print("Год издания обновлён")
        
    def delete_book(self):
        # Берём id, если книги есть
        id = self.input_id()
        if id is False:
            return None
        
        # Удаление книги
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        print()
        print('Книга удалена')
        
    def input_id(self) -> int | bool:
        self.view_books()
        print()
        # Берём существующие номера книг
        with sqlite3.connect(self.FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM books")
            all_id = cursor.fetchall()
        # Проверка, есть ли книги
        if all_id != []:
            # Ввод номера книги
            while True:
                try:
                    id = int(input('Введите номер книги: '))
                    if (id,) not in all_id:
                        raise IndexError
                    break
                except ValueError:
                    print('Неправильный ввод')
                except IndexError:
                    print('Книги с таким номером не существует')
            return id
        print("Нет ни одной книги")
        return False
    
    def setup(self) -> None:
        # Главное меню
        while True:
            print('''\nМеню:
1. Добавить книгу
2. Показать все книги
3. Найти книги по ...
4. Обновить год издания книги
5. Удалить книгу
0. Выход\n''')
            command = input('> ').strip()
            print()
            if command=='1':
                self.add_book()
            elif command=='2':
                self.view_books()
            elif command=='3':
                self.search_books()
            elif command=='4':
                self.update_year()
            elif command=='5':
                self.delete_book()
            elif command=='0':
                break
            else:
                print('Команда не опознана')
if __name__ == "__main__":
    # Запуск программы
    print("\nДобро пожаловать в менеджер книг!")
    app = LibraryManagerApp()
    app.setup()
