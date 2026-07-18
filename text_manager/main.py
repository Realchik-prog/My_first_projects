from pathlib import Path
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from typing import Literal
from exclude import EXCLUDED_WORDS
EXCLUDED_SYMBOLS = r" \n\r\t\v\f,.<>?/.,*!@\"#№;$%:^&()-=+|\\`~…–«»—"


class TextManagerApp:
    def __init__(self, history_file) -> None:
        self.HISTORY_FILE = history_file
        if not self.HISTORY_FILE.exists():
            with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        self.file = askopenfilename(title = "Выберите текстовый файл", 
                               filetypes=[("Текстовый файл", "*.txt"), ("Все файлы", "*.*")])
        Tk().withdraw()
        
        if self.file:
            print()
            print(f'Вы открыли файл "{Path(self.file).name}"')
            with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
            history.append(self.file)
            with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f)
        elif self.file is None:
            print('Файл не выбран')
            return
        
        while True:
            print("""\nДействия с файлом:
1. Количество слов
2. Количество символов
3. Самые встречаемые слова
4. Самые частые символы
5. Самые встречаемые слова с большой буквы
6. Самые частые словосочетания
7. Сколько времени займёт прочтение
0. Завершить действия с файлом\n
        """)

            command = input('> ').strip()
            print()
            
            if command=='0':
                break
            elif command=='1':
                print('Количество слов:', self.words_number())
            elif command=='2':
                print('Количество символов:', self.symbols_number())
            elif command=='3':
                self.frequently_used_words(None)
            elif command=='4':
                self.frequently_used_symbols()
            elif command=='5':
                self.frequently_used_words('capitalized')
            elif command=='6':
                self.frequently_used_phrases()
            elif command=='7':
                self.read_time()
            
    def words_number(self) -> int:
        if self.file is None:
            raise SystemError
        with open(self.file, 'r') as text:
            words = 0
            for line in text:
                line = [word for word in line.strip().split() if word!=' ']
                words += len(line)
        return words
    
    def symbols_number(self) -> int:
        if self.file is None:
            raise SystemError
        with open(self.file, 'r') as text:
            symbols = 0
            for line in text:
                line = line.strip()
                for s in list(line):
                    if s != ' ':
                        symbols += 1
        return symbols
        
    def read_time(self) -> None:
        words = self.words_number()
        print(f'Вдумчивое чтение (150 слов в минуту): {words/150:.0f} минут ({words/150/60:.1f} часов)')
        print(f'Обычное чтение (200 слов в минуту): {words/200:.0f} минут ({words/200/60:.1f} часов)')
        print(f'Быстрое чтение (300 слов в минуту): {words/300:.0f} минут ({words/300/60:.1f} часов)')
    
    def frequently_used_words(self, mode: Literal[None, "capitalized"]):
        if self.file is None:
            raise SystemError
        words_frequency_dict = {}
        places_number = self.get_places_number()
        
        with open(self.file, 'r') as text:
            # Считаем частоту повторения всех слов
            for line in text:
                if mode==None:
                    line = line.strip().lower().split()
                elif mode=='capitalized':
                    line = line.strip().split()
                for word in line:
                    if mode=='capitalized' and word != word.title():
                        continue
                    word = word.strip(EXCLUDED_SYMBOLS).strip()
                    if word.lower() not in EXCLUDED_WORDS and len(word) > 1 and not all([symbol in '1234567890' for symbol in word]):
                        if word in words_frequency_dict.keys():
                            words_frequency_dict[word] += 1
                        else:
                            words_frequency_dict[word] = 1
            try:
                # Отображаем слова по местам
                max_word = None
                for i in range(1, places_number + 1):
                    max_frequency = 0
                    for word, frequency in words_frequency_dict.items():
                        if frequency>max_frequency:
                            max_frequency = frequency
                            max_word = word
                    if max_word is not None:
                        del words_frequency_dict[max_word]
                        print(f"Место {i}. {max_word} - {max_frequency}")
                    else:
                        print('Слов нет')
            except KeyError:
                print('Слова закончились')
    def frequently_used_symbols(self):
        if self.file is None:
            raise SystemError
        places_number = self.get_places_number()
        split_character_by_case = input('Разделять символы по регистру?: ').lower() == 'да'
        print()
        symbols_frequency_dict = {}
        with open(self.file, 'r') as text:
            # Считаем частоту повторения всех символов
            for line in text:
                line = line.strip()
                for symbol in line:
                    if symbol != ' ':
                        if not split_character_by_case:
                            symbol = symbol.lower()
                        if symbol in symbols_frequency_dict.keys():
                            symbols_frequency_dict[symbol] += 1
                        else:
                            symbols_frequency_dict[symbol] = 1
            try:
                # Отображаем символы по местам
                max_symbol = None
                for i in range(1, places_number + 1):
                    max_frequency = 0
                    for symbol, frequency in symbols_frequency_dict.items():
                        if frequency>max_frequency:
                            max_frequency = frequency
                            max_symbol = symbol
                    if max_symbol is not None:
                        del symbols_frequency_dict[max_symbol]
                        print(f"Место {i}. {max_symbol} - {max_frequency} ({round(max_frequency * 100 / self.symbols_number(), 2)} %)")
                    else:
                        print('Символов нет')
            except KeyError:
                print('Символы закончились')
        
        
                        
    def frequently_used_phrases(self):
        if self.file is None:
            raise SystemError
        phrahes_frequency_dict = {}
        places_number = self.get_places_number()
        with open(self.file, 'r') as text:
            # Считаем частоту повторения всех словосочетаний
            for line in text:
                line = line.strip().strip(EXCLUDED_SYMBOLS).strip().lower().split()
                try:
                    for i in range(len(line)):
                        if line[i].strip(EXCLUDED_SYMBOLS).strip() in EXCLUDED_WORDS or line[i+1].strip(EXCLUDED_SYMBOLS).strip() in EXCLUDED_WORDS:
                            continue
                        if line[i].rstrip(EXCLUDED_SYMBOLS)==line[i] and line[i+1].lstrip(EXCLUDED_SYMBOLS)==line[i+1]:
                            phrahe = f'{line[i].strip().strip(EXCLUDED_SYMBOLS).strip()} {line[i+1].strip().strip(EXCLUDED_SYMBOLS).strip()}'
                            if phrahe in phrahes_frequency_dict.keys():
                                phrahes_frequency_dict[phrahe] += 1
                            else:
                                phrahes_frequency_dict[phrahe] = 1
                except IndexError:
                    pass
                
        try:
            # Отображаем словосочетания по местам
            max_phrahe = None
            for i in range(1, places_number + 1):
                max_frequency = 0
                for phrahe, frequency in phrahes_frequency_dict.items():
                    if frequency>max_frequency:
                        max_frequency = frequency
                        max_phrahe = phrahe
                if max_phrahe is not None:
                    del phrahes_frequency_dict[max_phrahe]
                    print(f"Место {i}. {max_phrahe} - {max_frequency}")
                else:
                    print('Словосочетаний нет')
        except KeyError:
            print('Словосочетания закончились')    
    
    def get_places_number(self) -> int:
        while True:
            try:
                places_number = int(input("Сколько мест показать?: "))
                if places_number <= 0:
                    print('Количество мест должно быть положительным')
                    continue
                break
            except ValueError:
                print('\nНеправильный ввод\n')
        print()
        return places_number
                  
                
        
                
                
                
        
        
class MainMenu:
    def __init__(self):
        self.HISTORY_FILE = Path(__file__).parent / 'history.json'
    def setup(self):
        while True:
            print("""\nГлавное меню:
1. Открыть файл
2. Посмотреть историю открытых файлов
0. Выход из программы\n
""")        
            command = input('> ').strip()
            print()
            if command=='1':
                TextManagerApp(self.HISTORY_FILE)
            elif command=='2':
                self.view_history()
            elif command=='0':
                break 
            else:
                print('Неправильная команда\n')
        
    def view_history(self):
        with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
            history_list = json.load(f)
            if history_list == []:
                print('История пуста')
                return
            memory = [None, 1]
            for file in history_list:
                if file != memory[0]:
                    if memory[0] is not None:
                        print(f"[{memory[1]} обращений]")
                        memory[1] = 1
                    print(file, end=' ')
                    memory[0] = file
                else:
                    memory[1] += 1
            print(f"[{memory[1]} обращений]")
    
        


if __name__ == "__main__":
    print('Это программа "Текстовый менеджер" на русском')
    menu = MainMenu()
    menu.setup()
    
    
    


