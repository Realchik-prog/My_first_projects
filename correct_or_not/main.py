from tkinter import *
from random import randint, choice, random
from time import time
from tkinter.messagebox import askyesno, askyesnocancel, askokcancel
import json
import sys
from pathlib import Path

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # Если запуск через exe файл
        base_path = Path(sys._MEIPASS)
    else:
        # Если прямой запуск через программу
        base_path = Path.cwd()
    return base_path / relative_path

def get_save_path():
    # Возвращает путь к файлу сохранения в стандартной папке пользователя.
    if sys.platform == 'win32':
        # На Windows
        base = Path.home() / 'AppData' / 'Roaming'
    else:
        # На Linux/macOS
        base = Path.home() / '.mygame'

    # Создаём папку для игры (если её нет)
    game_folder = base / 'Correct_or_not'
    game_folder.mkdir(parents=True, exist_ok=True)

    # Возвращаем полный путь к файлу сохранения
    return game_folder / 'save.json'

root = Tk()
root.title('Верно или нет?')
root.geometry('720x720')
root.resizable(width=False, height=False)
root.iconbitmap(str(resource_path('icon.ico')))


# Темы
themes = {
    'light': {
        'button_bg': '#a3a3a3',
        'global_bg': '#f0f0f0',
        'global_fg': 'black',
        'activate_global_bg': 'white',
        'activate_button_bg': 'white'
    },
    'dark': {
        'button_bg': '#d3d3d3',
        'global_bg': 'black',
        'global_fg': '#dddddd',
        'activate_global_bg': '#505050',
        'activate_button_bg': '#8a8a8a'
    },
    'sky': {
        'button_bg': '#6383ff',
        'global_bg': '#8fa5ff',
        'global_fg': 'white',
        'activate_global_bg': '#b3c2ff',
        'activate_button_bg': '#88a0fc'
    },
    'sun': {
        'button_bg': '#ffff99',
        'global_bg': '#ffee33',
        'global_fg': 'black',
        'activate_global_bg': '#ffff88',
        'activate_button_bg': '#ffff77'
    }
}
game_start_time = time() # Время захода в игровую сессию
try:
    with open(get_save_path(), 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data == None:
        raise FileNotFoundError
    global_theme = data['global_theme']
    unlocked_themes = data['unlocked_themes']
    difficult = data['difficult']
    start_count = data['start_count']
    start_time = data['start_time']
    gamemode = data['gamemode']
    open_statistics = data['open_statistics']
    loss_on_mistake = data['loss_on_mistake']
    completed_q1 = data['completed_q1']
    completed_q2 = data['completed_q2']
    completed_q3 = data['completed_q3']
    have_quests = data['have_quests']
    quests_dict = data['quests_dict']
    max_score = data['max_score']
    min_score = data['min_score']
    global_starts = data['global_starts']
    global_correct = data['global_correct']
    global_mistakes = data['global_mistakes']
    game_time = data['game_time']
    solution_speed = data['solution_speed']
    mistakes_frequency = data['mistakes_frequency']
    victories_gm1 = data['victories_gm1']
    timeouts_gm2 = data['timeouts_gm2']
    surrenders_gm1 = data['surrenders_gm1']
    surrenders_gm2 = data['surrenders_gm2']
    starts_dict = {
        1: data['starts_dict']['1'],
        2: data['starts_dict']['2']
    }
    loss_on_mistake_count_gm1 = data['loss_on_mistake_count_gm1']
    loss_on_mistake_count_gm2 = data['loss_on_mistake_count_gm2']
    correct_counts = data['correct_counts']
    mistakes_counts = data['mistakes_counts']
    difficult_times = data['difficult_times']
except (FileNotFoundError, KeyError): # Если сохранения нет
    game_time = 0
    # Стартовые настройки
    global_theme = 'light'
    unlocked_themes = {
        'light': True,
        'dark': False,
        'sky': False,
        'sun': False
    }
    difficult = 'Возрастающая'
    start_count = 15
    start_time = 60
    gamemode = 1 # 1 - определённое количество примеров, 2 - определённое количество времени
    open_statistics = False
    loss_on_mistake = False
    completed_q1 = completed_q2 = completed_q3 = False
    have_quests = False
    quests_dict = {
        '1': {
            'текст': None,
            'примеры': None,
            'время': None,
            'сложность': None
        },
        '2': {
            'текст': None,
            'примеры': None,
            'время': None,
            'сложность': None
        },
        '3': {
            'тип': None # Для каждого типа своё
        },
        'выполнено': {
            '1': 0,
            '2': 0,
            '3': 0
        }
    }
    # Переменные для статистики
    max_score = None # Лучший счёт
    min_score = None # Худший счёт
    global_starts = 0 # Запусков
    global_correct = 0 # Всего правильно решённых примеров
    global_mistakes = 0 # Всего ошибок
    solution_speed = { # Скорость решения примеров по сложностям (правильно решённые/время)
        'Легко': None,
        'Средне': None,
        'Трудно': None
    }
    mistakes_frequency = { # Частота ошибок по сложностям (ошибки/(ошибки+правильно решённые))
        'Легко': None,
        'Средне': None,
        'Трудно': None
    }
    victories_gm1 = timeouts_gm2 = 0 # Положительные окончания игр в 1 и 2 режимах
    surrenders_gm1 = surrenders_gm2 = 0 # Сколько раз игрок сдался в 1 и 2 режимах
    starts_dict = { # Сколько было стартов на 1 и 2 режиме по сложностям
        1: {
            'Возрастающая': 0,
            'Убывающая': 0,
            'Рандомная': 0,
            'Легко': 0,
            'Средне': 0,
            'Трудно': 0
        },
        2: {
            'Возрастающая': 0,
            'Убывающая': 0,
            'Рандомная': 0,
            'Легко': 0,
            'Средне': 0,
            'Трудно': 0
        }
    }
    loss_on_mistake_count_gm1 = loss_on_mistake_count_gm2 = 0

    # Переменные для подсчёта скорости решения примеров и частоты ошибок разных сложностей
    correct_counts = {
        'Легко': 0,
        'Средне': 0,
        'Трудно': 0
    }
    mistakes_counts = {
        'Легко': 0,
        'Средне': 0,
        'Трудно': 0
    }
    difficult_times = {
        'Легко': 0,
        'Средне': 0,
        'Трудно': 0
    }
# Установка темы
def set_theme(global_theme):
    global button_bg, global_bg, global_fg, activate_global_bg, activate_button_bg
    button_bg = themes[global_theme]['button_bg']
    global_bg = themes[global_theme]['global_bg']
    global_fg = themes[global_theme]['global_fg']
    activate_global_bg = themes[global_theme]['activate_global_bg']
    activate_button_bg = themes[global_theme]['activate_button_bg']
    root['bg'] = global_bg
set_theme(global_theme)
# Функции меню
def menu():
    title_label1 = Label(root, text='Игра', fg=global_fg, font=('Comic Sans MS', 40, 'bold'), bg=global_bg)
    title_label2 = Label(root, text='"Верно или нет?"', fg=global_fg, font=('Comic Sans MS', 40, 'bold'), bg=global_bg)
    play_button = Button(root, text='Начать игру', bg=button_bg, fg='black', font=('Comic Sans MS', 30), command=game, activebackground=activate_button_bg)
    settings_button = Button(root, text='Настройки', bg=button_bg, fg='black', font=('Comic Sans MS', 30), command=settings, activebackground=activate_button_bg)
    statistics_button = Button(root, text='Статистика', bg=button_bg, fg='black', font=('Comic Sans MS', 30), command=statistics, activebackground=activate_button_bg)
    how_to_play_button = Button(root, text='Как играть', bg=button_bg, fg='black', font=('Comic Sans MS', 30), command=how_to_play, activebackground=activate_button_bg)
    quests_button = Button(root, text='Квесты', bg=button_bg, fg='black', font=('Comic Sans MS', 30), command=quests, activebackground=activate_button_bg)
    exit_button = Button(root, text='Выйти', bg=button_bg, fg='black', font=('Comic Sans MS', 30), command=exit, activebackground=activate_button_bg)
    title_label1.place(relx=0.5, rely=0.1, anchor='center')
    title_label2.place(relx=0.5, rely=0.2, anchor='center')
    play_button.place(relx=0.5, rely=0.35, anchor='center', relwidth=0.35)
    how_to_play_button.place(relx=0.32, rely=0.5, anchor='center', relwidth=0.35)
    settings_button.place(relx=0.68, rely=0.5, anchor='center', relwidth=0.35)
    quests_button.place(relx=0.32, rely=0.65, anchor='center', relwidth=0.35)
    statistics_button.place(relx=0.68, rely=0.65, anchor='center', relwidth=0.35)
    exit_button.place(relx=0.5, rely=0.8, anchor='center', relwidth=0.35)
def game():
    global difficult, start_count, max_score, min_score, loss_on_mistake, global_starts
    time1 = time()
    mistakes = 0
    global_starts += 1
    starts_dict[gamemode][difficult] += 1
    def surrender():
        global surrenders_gm1, surrenders_gm2, loss_on_mistake_count_gm1, loss_on_mistake_count_gm2
        # Когда игрок сдался
        for widget in root.winfo_children():
            widget.destroy()
        if loss_on_mistake and mistakes==1:
            if gamemode==1:
                loss_on_mistake_count_gm1 += 1
            elif gamemode==2:
                loss_on_mistake_count_gm2 += 1
        else:
            if gamemode==1:
                surrenders_gm1 += 1
            elif gamemode==2:
                surrenders_gm2 += 1
        win_label = Label(text='Вы проиграли!', fg='red', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
        win_label.place(relx=0.5, rely=0.3, anchor='center')
        difficult_label = Label(text=f'Сложность: {difficult}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        difficult_label.place(relx=0.5, rely=0.38, anchor='center')
        gamemode_label = Label(root, text=f'Режим: {gamemode}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        gamemode_label.place(relx=0.5, rely=0.45, anchor='center')
        if not loss_on_mistake:
            mistakes_label = Label(text=f'Ошибок: {mistakes}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        else:
            mistakes_label = Label(text=f'(Проигрыш при ошибке)', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        mistakes_label.place(relx=0.5, rely=0.52, anchor='center')
        time2 = time()
        if gamemode==1:
            time_label = Label(text=f'Время прохождения: {round(time2 - time1, 2)}',
                               font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            path_label = Label(text=f'Пройдено примеров: {start_count - count}/{start_count}',
                               font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        elif gamemode==2:
            time_label = Label(text=f'Время прохождения: {round(time2 - time1, 2)}/{start_time} сек',
                               font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            path_label = Label(text=f'Пройдено примеров: {start_count - count}',
                               font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        time_label.place(relx=0.5, rely=0.59, anchor='center')
        path_label.place(relx=0.5, rely=0.66, anchor='center')

        def go_back():
            for widget in root.winfo_children():
                widget.destroy()
            menu()

        go_menu_button = Button(root, text='В меню', bg=button_bg, fg='black', font=('Comic Sans MS', 20, 'bold'),
                                command=go_back, activebackground=activate_button_bg)
        go_menu_button.place(relx=0.5, rely=0.77, anchor='center')

    for widget in root.winfo_children():
        widget.destroy()

    # Виджеты игры
    ButtonYES = Button(root, text='Да', bg='lime', fg='black', font=('Comic Sans MS', 20, 'bold'), padx=10, pady=5)
    ButtonYES.place(relx=0.35, rely=0.5, anchor='center')

    ButtonNO = Button(root, text='Нет', bg='red', fg='black', font=('Comic Sans MS', 20, 'bold'), padx=10, pady=5)
    ButtonNO.place(relx=0.65, rely=0.5, anchor='center')

    example = Label(root, text='', fg=global_fg, font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    example.place(relx=0.5, rely=0.3, anchor='center')

    count_label = Label(root, text='', fg=global_fg, font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    count_label.place(relx=0.1, rely=0.7, anchor=W)

    difficult_label = Label(root, text='', fg=global_fg, font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    difficult_label.place(relx=0.1, rely=0.8, anchor=W)

    mistakes_label = Label(root, text='Ошибок: 0', fg=global_fg, font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    mistakes_label.place(relx=0.6, rely=0.7, anchor=W)

    teacher_label = Label(root, text='', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    teacher_label.place(relx=0.5, rely=0.6, anchor='center')

    surrender_button = Button(root, text='Сдаться', font=('Comic Sans MS', 20, 'bold'),
                              padx=10, pady=5, command=surrender, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
    surrender_button.place(relx=0, rely=0)

    count = start_count


    def create_example():
        nonlocal count, ButtonYES, ButtonNO, example, count_label, teacher_label, difficult_label
        global time_for_example_start
        time_now = time()
        time_left = start_time+time1-time_now
        if gamemode==1:
            count_label.configure(text=f'Осталось: {count}', bg=global_bg)
        elif gamemode==2:
            count_label.configure(text=f'Осталось: {round(time_left, 2)} сек', bg=global_bg)
            def time_out():
                # Меню победы режима 2
                global min_score, max_score, timeouts_gm2, open_statistics, completed_q2, quests_dict, completed_q3
                open_statistics = True
                timeouts_gm2 += 1
                time2 = time()
                for widget in root.winfo_children():
                    widget.destroy()
                win_label = Label(text='Время вышло!', fg='green', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
                win_label.place(relx=0.5, rely=0.25, anchor='center')
                difficult_label = Label(text=f'Сложность: {difficult}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                difficult_label.place(relx=0.5, rely=0.33, anchor='center')
                gamemode_label = Label(root, text='Режим: 2', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                gamemode_label.place(relx=0.5, rely=0.4, anchor='center')
                if not loss_on_mistake:
                    mistakes_label = Label(text=f'Ошибок: {mistakes}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                else:
                    mistakes_label = Label(text=f'(Проигрыш при ошибке)', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                mistakes_label.place(relx=0.5, rely=0.47, anchor='center')
                time_label = Label(text=f'Время: {start_time} сек',
                                       font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                time_label.place(relx=0.5, rely=0.54, anchor='center')
                path_label = Label(text=f'Пройдено примеров: {start_count - count}',
                                       font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                path_label.place(relx=0.5, rely=0.61, anchor='center')
                difficult_coefficient = 2 if difficult == 'Трудно' else 0.5 if difficult == 'Легко' else 1
                score = round(((start_count-count) ** 2 - mistakes ** 2) / (time2-time1) * difficult_coefficient * 1000)
                score_label = Label(root, text=f'Счёт: {score}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
                score_label.place(relx=0.5, rely=0.68, anchor='center')
                if min_score == None or min_score > score:
                    min_score = score
                if max_score == None or max_score < score:
                    max_score = score

                # Обработка квестов
                if have_quests:
                    # Квест 2
                    if score>0 and start_time==quests_dict['2']['время'] and start_count - count >= quests_dict['2']['примеры'] and difficult == quests_dict['2']['сложность']:
                        completed_q2 = True
                        quests_dict['выполнено']['2'] += 1
                    # Квест 3
                    if quests_dict['3']['тип']==1:
                        if score>=quests_dict['3']['счёт']:
                            completed_q3 = True
                            quests_dict['выполнено']['3'] += 1
                            quests_dict['3']['тип'] = None
                    elif quests_dict['3']['тип']==2:
                        if start_count - count>=quests_dict['3']['примеры']:
                            quests_dict['3']['прогресс'][difficult] = 1
                            if sum(quests_dict['3']['прогресс'].values())==len(quests_dict['3']['прогресс']):
                                completed_q3 = True
                                quests_dict['выполнено']['3'] += 1
                                quests_dict['3']['тип'] = None
                    elif quests_dict['3']['тип']==4:
                        if score>=quests_dict['3']['счёт'] and mistakes==0:
                            completed_q3 = True
                            quests_dict['выполнено']['3'] += 1
                            quests_dict['3']['тип'] = None


                def go_back():
                    for widget in root.winfo_children():
                        widget.destroy()
                    menu()

                go_menu_button = Button(root, text='В меню', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                        command=go_back, activebackground=activate_button_bg)
                go_menu_button.place(relx=0.5, rely=0.79, anchor='center')

        a = b = d = None
        a2 = b2= d2 = None
        a3 = b3 = result3 = None
        def easy_example():
            nonlocal a, b, d
            difficult_label.configure(text='Сложность примера: Легко')
            # Для сложения или вычитания
            a = randint(-10, 10)
            b = randint(1, 21)
            d = 3  # Разброс в ошибке примера
        def medium_example():
            nonlocal a, b, d, a2, b2, d2
            difficult_label.configure(text='Сложность примера: Средне')
            a = randint(-100, 100)
            b = randint(1, 201)
            d = 15  # Разброс в ошибке примера
            # Для умножения
            a2 = randint(-15, 15)
            b2 = randint(1, 15)
            d2 = choice((a2, b2))
        def hard_example():
            nonlocal a, b, d, a2, b2, d2, a3, b3, result3
            difficult_label.configure(text='Сложность примера: Трудно')
            a = randint(-1000, 1000)
            b = randint(1, 2001)
            d = 50  # Разброс в ошибке примера
            # Для умножения
            a2 = randint(-100, 100)
            b2 = randint(1, 100)
            d2 = choice((a2, b2))
            # Для деления
            result3 = randint(1, 100)
            b3 = randint(1, 100)
            a3 = result3 * b3

        if gamemode==1:
            if count > start_count * 2 // 3 and difficult=='Возрастающая' or count < start_count//3 and difficult=='Убывающая' or difficult=='Легко' or difficult=='Рандомная' and random()>2/3:
                easy_example()
            elif count > start_count // 3 and difficult=='Возрастающая' or count < start_count*2//3 and difficult=='Убывающая' or difficult=='Средне' or difficult=='Рандомная' and random()>1/3:
                medium_example()
            else:
                hard_example()
        elif gamemode==2 and time_left>0:
            if time_left > start_time * 2 // 3 and difficult=='Возрастающая' or time_left < start_time//3 and difficult=='Убывающая' or difficult=='Легко' or difficult=='Рандомная' and random()>2/3:
                easy_example()
            elif time_left > start_time // 3 and difficult=='Возрастающая' or time_left < start_time*2//3 and difficult=='Убывающая' or difficult=='Средне' or difficult=='Рандомная' and random()>1/3:
                medium_example()
            else:
                hard_example()
        else:
            time_out()
            return 0
        if difficult_label['text'] == 'Сложность примера: Легко':
            sign = choice(('+', '-'))
        elif difficult_label['text'] == 'Сложность примера: Средне':
            sign = choice(('+', '-', '*'))
        elif difficult_label['text'] == 'Сложность примера: Трудно':
            sign = choice(('+', '-', '*', '/'))
        if sign == '+':
            c = a + b
        elif sign == '-':
            c = a - b
        elif sign == '*':
            c = a2 * b2
        elif sign == '/':
            c = result3
        if random() < 0.5:
            if sign=='+' or sign=='-':
                example.configure(text=f'{a} {sign} {b} = {c}')
            elif sign=='*':
                example.configure(text=f'{a2} {sign} {b2} = {c}')
            elif sign=='/':
                example.configure(text=f'{a3} {sign} {b3} = {c}')
            ButtonYES.configure(command=correct)
            ButtonNO.configure(command=uncorrect)
        else:
            if sign=='+' or sign=='-':
                if random() < 0.5:
                    example.configure(text=f'{a} {sign} {b} = {c + randint(1, d)}')
                else:
                    example.configure(text=f'{a} {sign} {b} = {c - randint(1, d)}')
            elif sign == '*':
                if random() < 0.5:
                    example.configure(text=f'{a2} {sign} {b2} = {c + d2}')
                else:
                    example.configure(text=f'{a2} {sign} {b2} = {c - d2}')
            elif sign=='/':
                if random() < 0.5:
                    example.configure(text=f'{a3} {sign} {b3} = {c + randint(1, 2)}')
                else:
                    example.configure(text=f'{a3} {sign} {b3} = {c - randint(1, 2)}')
            ButtonYES.configure(command=uncorrect)
            ButtonNO.configure(command=correct)
        time_for_example_start = time()
    def correct():
        # При правильном ответе
        global record, max_score, min_score, global_correct, victories_gm1, time_for_example_start, open_statistics, \
        correct_counts, difficult_times, completed_q1, completed_q3, quests_dict
        nonlocal count, difficult_label
        count-=1
        difficult_times[difficult_label['text'][19:]] += time() - time_for_example_start
        correct_counts[difficult_label['text'][19:]] += 1
        global_correct += 1
        if have_quests and quests_dict['3']['тип']==3:
            quests_dict['3']['прогресс'] += 1
            if quests_dict['3']['прогресс']==quests_dict['3']['примеры']:
                completed_q3 = True
                quests_dict['выполнено']['3'] += 1
                quests_dict['3']['тип'] = None
        if count == 0 and gamemode==1:
            # Меню победы режима 1
            open_statistics = True
            victories_gm1 += 1
            for widget in root.winfo_children():
                widget.destroy()
            win_label = Label(root, text='Вы победили!', fg='green', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
            win_label.place(relx=0.5, rely=0.25, anchor='center')
            difficult_label = Label(root, text=f'Сложность: {difficult}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            difficult_label.place(relx=0.5, rely=0.33, anchor='center')
            gamemode_label = Label(root, text='Режим: 1', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            gamemode_label.place(relx=0.5, rely=0.4, anchor='center')
            if not loss_on_mistake:
                mistakes_label = Label(text=f'Ошибок: {mistakes}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            else:
                mistakes_label = Label(text=f'(Проигрыш при ошибке)', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            mistakes_label.place(relx=0.5, rely=0.47, anchor='center')
            time2 = time()
            time_label = Label(root, text=f'Время прохождения: {round(time2 - time1, 2)} сек', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            time_label.place(relx=0.5, rely=0.54, anchor='center')
            path_label = Label(text=f'Примеров на старте: {start_count}',
                               font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            path_label.place(relx=0.5, rely=0.61, anchor='center')
            difficult_coefficient = 2 if difficult == 'Трудно' else 0.5 if difficult == 'Легко' else 1
            score = round((start_count**2 - mistakes**2)/(time2-time1)*difficult_coefficient*1000)
            score_label = Label(root, text=f'Счёт: {score}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            score_label.place(relx=0.5, rely=0.68, anchor='center')
            if min_score==None or min_score>score:
                min_score = score
            if max_score==None or max_score<score:
                max_score = score

            # Обрабатываем квесты
            if have_quests:
                # Квест 1
                if score>0 and start_count == quests_dict['1']['примеры'] and time2 - time1 <= quests_dict['1']['время'] and difficult == quests_dict['1']['сложность']:
                    completed_q1 = True
                    quests_dict['выполнено']['1'] += 1
                # Квест 3
                if quests_dict['3']['тип'] == 1:
                    if score >= quests_dict['3']['счёт']:
                        completed_q3 = True
                        quests_dict['выполнено']['3'] += 1
                        quests_dict['3']['тип'] = None
                elif quests_dict['3']['тип'] == 2:
                    if start_count >= quests_dict['3']['примеры']:
                        quests_dict['3']['прогресс'][difficult] = 1
                        if sum(quests_dict['3']['прогресс'].values()) == len(quests_dict['3']['прогресс']):
                            completed_q3 = True
                            quests_dict['выполнено']['3'] += 1
                            quests_dict['3']['тип'] = None
                elif quests_dict['3']['тип'] == 4:
                    if score >= quests_dict['3']['счёт'] and mistakes == 0:
                        completed_q3 = True
                        quests_dict['выполнено']['3'] += 1
                        quests_dict['3']['тип'] = None
            def go_back():
                for widget in root.winfo_children():
                    widget.destroy()
                menu()

            go_menu_button = Button(root, text='В меню', bg=button_bg, fg='black', font=('Comic Sans MS', 20, 'bold'),
                                    command=go_back, activebackground=activate_button_bg)
            go_menu_button.place(relx=0.5, rely=0.79, anchor='center')
        else:
            # Если примеры не закончились
            teacher_label.configure(text='Правильно!', fg='green')
            create_example()
    def uncorrect():
        # При неправильном ответе
        global global_mistakes, time_for_example_start
        nonlocal count, mistakes
        count+=1
        difficult_times[difficult_label['text'][19:]] += time() - time_for_example_start
        mistakes_counts[difficult_label['text'][19:]] += 1
        global_mistakes += 1
        mistakes+=1
        mistakes_label['text'] = f'Ошибок: {mistakes}'
        teacher_label.configure(text='Неправильно!', fg='red')
        if loss_on_mistake:
            surrender()
            return 0
        create_example()

    create_example()
def settings(reward=False):
    global difficult
    def page1():
        for widget in root.winfo_children():
            widget.destroy()
        def back():
            for widget in root.winfo_children():
                widget.destroy()
            menu()
        back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
        back_button.place(x=0, y=0)

        # Настройка сложности
        difficult_label = Label(root, text='Сложность', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
        difficult_label.place(relx=0.5, rely=0.1, anchor='center')
        def green_increasing():
            global difficult
            for widget in [decreasing_difficult, easy_difficult, medium_difficult, hard_difficult, random_difficult]:
                widget.configure(bg=button_bg)
            increasing_difficult.configure(bg='green')
            difficult = 'Возрастающая'
        def green_decreasing():
            global difficult
            for widget in [increasing_difficult, easy_difficult, medium_difficult, hard_difficult, random_difficult]:
                widget.configure(bg=button_bg)
            decreasing_difficult.configure(bg='green')
            difficult = 'Убывающая'
        def green_easy():
            global difficult
            for widget in [increasing_difficult, decreasing_difficult, medium_difficult, hard_difficult, random_difficult]:
                widget.configure(bg=button_bg)
            easy_difficult.configure(bg='green')
            difficult = 'Легко'
        def green_medium():
            global difficult
            for widget in [increasing_difficult, decreasing_difficult, easy_difficult, hard_difficult, random_difficult]:
                widget.configure(bg=button_bg)
            medium_difficult.configure(bg='green')
            difficult = 'Средне'
        def green_hard():
            global difficult
            for widget in [increasing_difficult, decreasing_difficult, medium_difficult, easy_difficult, random_difficult]:
                widget.configure(bg=button_bg)
            hard_difficult.configure(bg='green')
            difficult = 'Трудно'
        def green_random():
            global difficult
            for widget in [increasing_difficult, decreasing_difficult, medium_difficult, easy_difficult, hard_difficult]:
                widget.configure(bg=button_bg)
            random_difficult.configure(bg='green')
            difficult = 'Рандомная'

        increasing_difficult = Button(root, text='Возрастающая', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                      activebackground='#ebd026', command=green_increasing)
        increasing_difficult.place(relx=0.2, rely=0.2, anchor='center', relwidth=0.3)
        decreasing_difficult = Button(root, text='Убывающая', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                      activebackground='#ebd026', command=green_decreasing)
        decreasing_difficult.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.3)
        random_difficult = Button(root, text='Рандомная', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                  activebackground='#ebd026', command=green_random)
        random_difficult.place(relx=0.8, rely=0.2, anchor='center', relwidth=0.3)
        easy_difficult = Button(root, text='Легко', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                activebackground='#ebd026', command=green_easy)
        easy_difficult.place(relx=0.2, rely=0.29, anchor='center', relwidth=0.3)
        medium_difficult = Button(root, text='Средне', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                  activebackground='#ebd026', command=green_medium)
        medium_difficult.place(relx=0.5, rely=0.29, anchor='center', relwidth=0.3)
        hard_difficult = Button(root, text='Трудно', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                activebackground='#ebd026', command=green_hard)
        hard_difficult.place(relx=0.8, rely=0.29, anchor='center', relwidth=0.3)
        if difficult == 'Возрастающая':
            increasing_difficult.configure(bg='green')
        elif difficult == 'Убывающая':
            decreasing_difficult.configure(bg='green')
        elif difficult == 'Легко':
            easy_difficult.configure(bg='green')
        elif difficult == 'Средне':
            medium_difficult.configure(bg='green')
        elif difficult == 'Трудно':
            hard_difficult.configure(bg='green')
        elif difficult == 'Рандомная':
            random_difficult.configure(bg='green')

        # Выбор режима игры
        def gamemode1_settings():
            global start_count_title, start_count_label, start_count_entry, start_count_button
            # Настройка количества примеров на старте
            def start_count_input():
                global start_count
                try:
                    count = int(start_count_entry.get())
                    if count > 0:
                        start_count = count
                        start_count_label['text'] = f'Установлено: {start_count}'
                except ValueError:
                    pass
                finally:
                    start_count_entry.delete(0, 'end')

            start_count_title = Label(root, text='Количество примеров на старте', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
            start_count_title.place(relx=0.5, rely=0.6, anchor='center')
            start_count_label = Label(root, text=f'Установлено: {start_count}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            start_count_label.place(relx=0.1, rely=0.7, anchor=W)
            start_count_entry = Entry(root, font=('Comic Sans MS', 20, 'bold'))
            start_count_entry.place(relx=0.5, rely=0.7, anchor=W, relwidth=0.2)
            start_count_button = Button(root, text='Ввести', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                        command=start_count_input, activebackground=activate_button_bg)
            start_count_button.place(relx=0.7, rely=0.7, anchor=W, relwidth=0.2, height=50)

        def gamemode2_settings():
            global start_time_title, start_time_label, start_time_entry, start_time_button
            # Настройка времени на игру
            def start_time_input():
                global start_time
                try:
                    time = int(start_time_entry.get())
                    if time > 0:
                        start_time = time
                        start_time_label['text'] = f'Установлено: {start_time}'
                except ValueError:
                    pass
                finally:
                    start_time_entry.delete(0, 'end')

            start_time_title = Label(root, text='Время на игру (в секундах)', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
            start_time_title.place(relx=0.5, rely=0.6, anchor='center')
            start_time_label = Label(root, text=f'Установлено: {start_time}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
            start_time_label.place(relx=0.1, rely=0.7, anchor=W)
            start_time_entry = Entry(root, font=('Comic Sans MS', 20, 'bold'))
            start_time_entry.place(relx=0.5, rely=0.7, anchor=W, relwidth=0.2)
            start_time_button = Button(root, text='Ввести', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                        command=start_time_input, activebackground=activate_button_bg)
            start_time_button.place(relx=0.7, rely=0.7, anchor=W, relwidth=0.2, height=50)
        def green_gamemode1():
            global gamemode, start_time_title, start_time_label, start_time_entry, start_time_button
            gamemode1_button['bg'] = 'green'
            gamemode2_button['bg'] = button_bg
            if gamemode == 2:
                gamemode1_settings()
                start_time_title.destroy()
                start_time_label.destroy()
                start_time_entry.destroy()
                start_time_button.destroy()
            gamemode = 1
        def green_gamemode2():
            global gamemode, start_count_title, start_count_label, start_count_entry, start_count_button
            gamemode2_button['bg'] = 'green'
            gamemode1_button['bg'] = button_bg
            if gamemode == 1:
                gamemode2_settings()
                start_count_title.destroy()
                start_count_label.destroy()
                start_count_entry.destroy()
                start_count_button.destroy()
            gamemode = 2
        gamemode_title = Label(root, text='Режим игры:', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
        gamemode_title.place(relx=0.1, rely=0.45, anchor=W)
        gamemode1_button = Button(root, text='1', bg=button_bg, font=('Comic Sans MS', 25, 'bold'), command=green_gamemode1, activebackground=activate_button_bg)
        gamemode1_button.place(relx=0.5, rely=0.45, anchor='center')
        gamemode2_button = Button(root, text='2', bg=button_bg, font=('Comic Sans MS', 25, 'bold'), command=green_gamemode2, activebackground=activate_button_bg)
        gamemode2_button.place(relx=0.57, rely=0.45, anchor='center')
        explanation_label1 = Label(root, text='1 - "Реши быстро!"',
                                  font=('Comic Sans MS', 15, 'bold'), bg=global_bg, fg=global_fg)
        explanation_label1.place(relx=0.66, rely=0.42, anchor=W)
        explanation_label2 = Label(root, text='2 - "Реши много!"',
                                   font=('Comic Sans MS', 15, 'bold'), bg=global_bg, fg=global_fg)
        explanation_label2.place(relx=0.66, rely=0.48, anchor=W)
        if gamemode == 1:
            gamemode1_button['bg'] = 'green'
            gamemode1_settings()
        elif gamemode == 2:
            gamemode2_button['bg'] = 'green'
            gamemode2_settings()

        # Настройка, будет ли проигрыш при ошибке
        def loss_on_mistake_on():
            global loss_on_mistake
            loss_on_mistake_button.configure(bg='green', text='Вкл', command=loss_on_mistake_off)
            loss_on_mistake = True
        def loss_on_mistake_off():
            global loss_on_mistake
            loss_on_mistake_button.configure(bg=button_bg, text='Выкл', command=loss_on_mistake_on)
            loss_on_mistake = False
        loss_on_mistake_title = Label(root, text='Проигрыш при ошибке: ', font=('Comic Sans MS', 25, 'bold'), bg=global_bg, fg=global_fg)
        loss_on_mistake_title.place(relx=0.1, rely=0.82, anchor=W)
        if not loss_on_mistake:
            loss_on_mistake_button = Button(root, text='Выкл', bg=button_bg, font=('Comic Sans MS', 25, 'bold'), command=loss_on_mistake_on, activebackground=activate_button_bg)
            loss_on_mistake_button.place(relx=0.67, rely=0.82, anchor=W, height=50, relwidth=0.15)
        else:
            loss_on_mistake_button = Button(root, text='Вкл', bg='green', font=('Comic Sans MS', 25, 'bold'), command=loss_on_mistake_off, activebackground=activate_button_bg)
            loss_on_mistake_button.place(relx=0.67, rely=0.82, anchor=W, height=50, relwidth=0.15)

        # Случайная настройка
        def random_settings():
            global difficult, loss_on_mistake, gamemode, start_count, start_time
            for widget in root.winfo_children():
                widget.destroy()
            difficult = choice(['Возрастающая', "Убывающая", "Рандомная", "Легко", "Средне", "Трудно"])
            loss_on_mistake = choice([True, False])
            gamemode = choice([1, 2])
            if gamemode == 1:
                start_count = choice([5, 10, 15, 20, 30, 50])
            elif gamemode == 2:
                start_time = choice([15, 30, 60, 120, 180, 250])
            settings()
        random_settings_button = Button(root, text='Случайная настройка', font=('Comic Sans MS', 20, 'bold'), command=random_settings, bg=button_bg, activebackground=activate_button_bg)
        random_settings_button.place(anchor='w', relx=0.05, rely=0.925)

        next_page_button = Button(root, text='->', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page2,
                                  activebackground=activate_button_bg)
        next_page_button.place(relx=0.85, rely=0.92, anchor='center', relheight=0.08)
    def page2():
        for widget in root.winfo_children():
            widget.destroy()
        def back():
            for widget in root.winfo_children():
                widget.destroy()
            menu()
        back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
        back_button.place(x=0, y=0)

        themes_title = Label(root, text='Темы оформления', font=('Comic Sans MS', 35, 'bold'), bg=global_bg, fg=global_fg)
        themes_title.place(relx=0.5, rely=0.07, anchor='center')

        def select_theme(theme):
            global global_theme
            global_theme = theme
            for theme_button in theme_buttons:
                theme_button['default'] = 'normal'
                if theme_button['text'] == theme.title():
                    theme_button['default'] = 'active'
            set_theme(theme)
            for widget in root.winfo_children():
                widget.destroy()
            page2()

        theme_buttons = []
        for theme in themes:
            if unlocked_themes[theme]:
                theme_button = Button(root, text=theme.title(), font=('Comic Sans MS', 25, 'bold'), fg='black', width=15,
                                      bg=themes[theme]['button_bg'], activebackground=themes[theme]['activate_button_bg'],
                                      borderwidth=10, default='normal')
                if global_theme==theme:
                    theme_button['default'] = 'active'
            else:
                theme_button = Button(root, text='?', font=('Comic Sans MS', 25, 'bold'), width=15,
                                      borderwidth=10, bg='white', state='disabled')
            theme_buttons.append(theme_button)
        theme_buttons[0]['command'] = lambda: select_theme('light')
        theme_buttons[1]['command'] = lambda: select_theme('dark')
        theme_buttons[2]['command'] = lambda: select_theme('sky')
        theme_buttons[3]['command'] = lambda: select_theme('sun')
        i=0
        for theme_button in theme_buttons:
            theme_button.place(relx=0.5, rely=0.25 + i, anchor='center')
            i+=0.2

        previous_page_button = Button(root, text='<-', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page1,
                                      activebackground=activate_button_bg)
        previous_page_button.place(relx=0.15, rely=0.92, anchor='center', relheight=0.08)
    if reward:
        page2()
        return None
    page1()
def statistics():
    global open_statistics, correct_counts, difficult_times
    def page1():
        for widget in root.winfo_children():
            widget.destroy()
        def back():
            for widget in root.winfo_children():
                widget.destroy()
            menu()
        back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
        back_button.place(x=0, y=0)
        if not open_statistics:
            not_open_label = Label(root, text='Выиграйте хотя бы в одной игре', font=('Comic Sans MS', 25, 'bold'), bg=global_bg, fg=global_fg)
            not_open_label.place(relx=0.5, rely=0.5, anchor='center')
            return 0
        general_statistics_title = Label(root, text='Общая статистика', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
        general_statistics_title.place(relx=0.5, rely=0.07, anchor='center')

        max_score_label = Label(root, text=f'Лучший счёт: {max_score if max_score!=None else 'Нет'}',
                                font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        max_score_label.place(relx=0.25, rely=0.2, anchor='center')
        min_score_label = Label(root, text=f'Худший счёт: {min_score if min_score != None else 'Нет'}',
                                font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        min_score_label.place(relx=0.25, rely=0.27, anchor='center')
        global_starts_label = Label(root, text=f'Запусков игры: {global_starts}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        global_starts_label.place(relx=0.25, rely=0.34, anchor='center')
        global_correct_label = Label(root, text=f'Решено правильно: {global_correct}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        global_correct_label.place(relx=0.25, rely=0.41, anchor='center')
        global_mistakes_label = Label(root, text=f'Ошибок: {global_mistakes}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        global_mistakes_label.place(relx=0.25, rely=0.48, anchor='center')
        time_output = time() - game_start_time + game_time
        if time_output>=3600:
            game_time_label = Label(root, text=f'Время в игре: {round(time_output//3600)} ч {round(time_output%3600//60)} мин',
                                    font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        else:
            game_time_label = Label(root,
                                    text=f'Время в игре: {round(time_output // 60)} мин',
                                    font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        game_time_label.place(relx=0.025, rely=0.55, anchor='w')

        quests_statistics_title = Label(root, text='Выполнено квестов', bg=global_bg, fg=global_fg, font=('Comic Sans MS', 20, 'bold'))
        quests_statistics_title.place(anchor='center', relx=0.75, rely=0.2)
        quest1_statistic_label = Label(root, text=f'Тип 1: {quests_dict['выполнено']['1']}', bg=global_bg, fg=global_fg,
                                       font=('Comic Sans MS', 20, 'bold'))
        quest1_statistic_label.place(anchor='center', relx=0.75, rely=0.27)
        quest2_statistic_label = Label(root, text=f'Тип 2: {quests_dict['выполнено']['2']}', bg=global_bg, fg=global_fg,
                                       font=('Comic Sans MS', 20, 'bold'))
        quest2_statistic_label.place(anchor='center', relx=0.75, rely=0.34)
        quest3_statistic_label = Label(root, text=f'Тип 3: {quests_dict['выполнено']['3']}', bg=global_bg, fg=global_fg,
                                       font=('Comic Sans MS', 20, 'bold'))
        quest3_statistic_label.place(anchor='center', relx=0.75, rely=0.41)
        all_quests_statistic_label = Label(root, text=f'Всего: {sum(quests_dict['выполнено'].values())}', bg=global_bg, fg=global_fg,
                                       font=('Comic Sans MS', 20, 'bold'))
        all_quests_statistic_label.place(anchor='center', relx=0.75, rely=0.48)

        solution_speed_title = Label(root, text='Скорость решения примеров', font=('Comic Sans MS', 18, 'bold'), bg=global_bg, fg=global_fg)
        solution_speed_title.place(relx=0.25, rely=0.62, anchor='center')
        i=0
        for difficult in solution_speed:
            i += 0.07
            if difficult_times[difficult]!=0:
                solution_speed[difficult] = round(correct_counts[difficult]*60//difficult_times[difficult])
                solution_speed_label = Label(root, text=f'{difficult}: {solution_speed[difficult]} в мин', font=('Comic Sans MS', 18, 'bold'), bg=global_bg, fg=global_fg)
            else:
                solution_speed_label = Label(root, text=f'{difficult}: Не определено', font=('Comic Sans MS', 18, 'bold'), bg=global_bg, fg=global_fg)
            solution_speed_label.place(relx=0.25, rely=0.62 + i, anchor='center')
        mistakes_frequency_title = Label(root, text='Частота ошибок', font=('Comic Sans MS', 18, 'bold'), bg=global_bg, fg=global_fg)
        mistakes_frequency_title.place(relx=0.75, rely=0.62, anchor='center')
        i = 0
        for difficult in mistakes_frequency:
            i += 0.07
            if mistakes_counts[difficult] != 0:
                mistakes_frequency[difficult] = round((mistakes_counts[difficult]+correct_counts[difficult]) / mistakes_counts[difficult])
                mistakes_frequency_label = Label(root, text=f'{difficult}: раз в {mistakes_frequency[difficult]} {'примера' if mistakes_frequency[difficult]%10<5 and not 10<mistakes_frequency[difficult]%100<20 else 'примеров'}',
                                             font=('Comic Sans MS', 18, 'bold'), bg=global_bg, fg=global_fg)
            else:
                mistakes_frequency_label = Label(root, text=f'{difficult}: Ошибок нет', font=('Comic Sans MS', 18, 'bold'), bg=global_bg, fg=global_fg)
            mistakes_frequency_label.place(relx=0.75, rely=0.62 + i, anchor='center')
        next_page_button = Button(root, text='->', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page2, activebackground=activate_button_bg)
        next_page_button.place(relx=0.55, rely=0.92, anchor='center', relheight=0.08)
    def page2():
        for widget in root.winfo_children():
            widget.destroy()
        def back():
            for widget in root.winfo_children():
                widget.destroy()
            menu()
        back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
        back_button.place(x=0, y=0)
        gm1_statistics_title = Label(root, text='Статистика режима 1', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
        gm1_statistics_title.place(relx=0.5, rely=0.07, anchor='center')
        victories_gm1_label = Label(root, text=f'Побед: {victories_gm1}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        victories_gm1_label.place(relx=0.5, rely=0.2, anchor='center')
        surrenders_gm1_label = Label(root, text=f'Сдались: {surrenders_gm1}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        surrenders_gm1_label.place(relx=0.5, rely=0.27, anchor='center')
        loss_on_mistake_count_gm1_label = Label(root, text=f'Проигрышей при ошибке: {loss_on_mistake_count_gm1}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        loss_on_mistake_count_gm1_label.place(relx=0.5, rely=0.34, anchor='center')
        starts_title = Label(root, text='Запусков игры', font=('Comic Sans MS', 25, 'bold'), bg=global_bg, fg=global_fg)
        starts_title.place(relx=0.5, rely=0.41, anchor='center')
        i=0
        for difficult in starts_dict[1]:
            i += 0.07
            starts_label = Label(root, text=f'{difficult}: {starts_dict[1][difficult]}', font=('Comic Sans MS', 18, 'bold'), fg=global_fg, bg=global_bg)
            if i<0.28:
                starts_label.place(relx=0.25, rely=0.41 + i, anchor='center')
            else:
                starts_label.place(relx=0.75, rely=0.2 + i, anchor='center')
        previous_page_button = Button(root, text='<-', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page1, activebackground=activate_button_bg)
        previous_page_button.place(relx=0.45, rely=0.92, anchor='center', relheight=0.08)
        next_page_button = Button(root, text='->', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page3, activebackground=activate_button_bg)
        next_page_button.place(relx=0.55, rely=0.92, anchor='center', relheight=0.08)
    def page3():
        for widget in root.winfo_children():
            widget.destroy()
        def back():
            for widget in root.winfo_children():
                widget.destroy()
            menu()
        back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
        back_button.place(x=0, y=0)
        gm2_statistics_title = Label(root, text='Статистика режима 2', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
        gm2_statistics_title.place(relx=0.5, rely=0.07, anchor='center')
        timeouts_gm2_label = Label(root, text=f'Истечений времени: {timeouts_gm2}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        timeouts_gm2_label.place(relx=0.5, rely=0.2, anchor='center')
        surrenders_gm2_label = Label(root, text=f'Сдались: {surrenders_gm2}', font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        surrenders_gm2_label.place(relx=0.5, rely=0.27, anchor='center')
        loss_on_mistake_count_gm2_label = Label(root, text=f'Проигрышей при ошибке: {loss_on_mistake_count_gm2}',
                                                font=('Comic Sans MS', 20, 'bold'), bg=global_bg, fg=global_fg)
        loss_on_mistake_count_gm2_label.place(relx=0.5, rely=0.34, anchor='center')
        starts_title = Label(root, text='Запусков игры', font=('Comic Sans MS', 25, 'bold'), bg=global_bg, fg=global_fg)
        starts_title.place(relx=0.5, rely=0.41, anchor='center')
        i = 0
        for difficult in starts_dict[2]:
            i += 0.07
            starts_label = Label(root, text=f'{difficult}: {starts_dict[2][difficult]}',
                                 font=('Comic Sans MS', 18, 'bold'), fg=global_fg, bg=global_bg)
            if i < 0.28:
                starts_label.place(relx=0.25, rely=0.41 + i, anchor='center')
            else:
                starts_label.place(relx=0.75, rely=0.2 + i, anchor='center')
        previous_page_button = Button(root, text='<-', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page2, activebackground=activate_button_bg)
        previous_page_button.place(relx=0.45, rely=0.92, anchor='center', relheight=0.08)
    page1()
def how_to_play():
    for widget in root.winfo_children():
        widget.destroy()

    def back():
        for widget in root.winfo_children():
            widget.destroy()
        menu()
    back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
    back_button.place(x=0, y=0)

    how_to_play_title = Label(root, text='Как играть', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
    how_to_play_title.place(anchor='n', relx=0.5, rely=0)

    htp_label1 = Label()
    next_page_button = Button()
    htp_label2 = Label()
    previous_page_button = Button()

    def page1():
        nonlocal htp_label2, previous_page_button, htp_label1, next_page_button
        htp_label2.destroy()
        previous_page_button.destroy()

        htp_label1 = Label(root,
                           text="""
1) Ваша задача - решать математические примеры. 
Нажимайте на "Да", если вы думаете, что пример 
верен, и на "Нет" в противном случае.

2) В конце каждой игры будет показан ваш счёт. Он 
показывает, как хорошо вы сыграли, и зависит 
от количества решённых примеров и ошибок, а также
от времени игры. Сложность тоже влияет на итоговый 
множитель: на "Легко" финальный счёт делится на 2, 
на "Трудно" — умножается на 2, чтобы поощрить игру 
на сложном уровне.

3) В разделе "Настройки" можно настроить игру под себя: 
режим, сложность и другое. Есть 2 режима игры: первый -
решение определённого количества примеров на время, 
второй - решение как можно большего количества примеров 
за ограниченное время.
        """,
                           font=('Comic Sans MS', 17),
                           justify=LEFT, bg=global_bg, fg=global_fg)
        htp_label1.place(x=20, rely=0.1, anchor='nw')
        next_page_button = Button(root, text='->', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page2, activebackground=activate_button_bg)
        next_page_button.place(relx=0.55, rely=0.92, anchor='center', relheight=0.08)

    def page2():
        nonlocal htp_label1, next_page_button, htp_label2, previous_page_button
        htp_label1.destroy()
        next_page_button.destroy()
        htp_label2 = Label(root,
                           text="""
4) В разделе "Квесты" вы найдёте испытания с особыми 
условиями. Чтобы квест был засчитан, ваш счёт в игре
должен быть больше нуля. За успешное выполнение всех 
3 квестов вы получите случайную тему оформления 

5) В разделе "Статистика" вы можете посмотреть 
разнообразную статистику о вашей игре:
от количества заходов в игру до скорости решения 
примеров на разных сложностях.

6) Перед выходом вам предложат сохранить прогресс. 
Если для вас это важно, не стоит закрывать игру на "x"

7) Наслаждайтесь игрой: побивайте рекорды, 
пробуйте разные настройки, смотрите статистику 
и выполняйте квесты!
        """,
                           font=('Comic Sans MS', 17),
                           justify=LEFT, bg=global_bg, fg=global_fg
                           )
        htp_label2.place(x=20, rely=0.1, anchor='nw')
        autor_label = Label(root, font=('Comic Sans MS', 17, 'italic'), text='Разработчик игры Realchik', bg=global_bg, fg=global_fg)
        autor_label.place(x=20, rely=0.87, anchor='w')
        previous_page_button = Button(root, text='<-', font=('Comic Sans MS', 25, 'bold'), bg=button_bg, command=page1, activebackground=activate_button_bg)
        previous_page_button.place(relx=0.55, rely=0.92, anchor='center', relheight=0.08)

    page1()
def quests():
    global have_quests, quests_dict
    for widget in root.winfo_children():
        widget.destroy()

    def back():
        for widget in root.winfo_children():
            widget.destroy()
        menu()

    back_button = Button(root, text='Назад', font=('Comic Sans MS', 20, 'bold'), command=back, bg=global_bg, fg=global_fg, activebackground=activate_global_bg)
    back_button.place(x=0, y=0)

    parts_of_quests12 = {
        'сложность': ['Возрастающая', 'Убывающая', 'Рандомная', 'Легко', 'Средне', 'Трудно'],
        'примеры': [5, 10, 15, 20, 30, 50],
        'время': [15, 30, 60, 120, 180, 250]
    }

    def quest1():
        # Квест про режим 1
        nonlocal parts_of_quests12
        # Реши ... примеров не более чем за ... секунд на сложности ... в режиме 1
        while True:
            quests_dict['1']['примеры'] = choice(parts_of_quests12['примеры'])
            quests_dict['1']['время'] = choice(parts_of_quests12['время'])
            quests_dict['1']['сложность'] = choice(parts_of_quests12['сложность'])
            difficult_coefficient = 2 if quests_dict['1']['сложность'] == 'Трудно' else 0.5 if quests_dict['1']['сложность'] == 'Легко' else 1
            if quests_dict['1']['время']/(quests_dict['1']['примеры']*difficult_coefficient) <= 2.5 or quests_dict['1']['время']/(quests_dict['1']['примеры']*difficult_coefficient)>=5:
                continue
            else:
                return (f'1) Реши {quests_dict['1']['примеры']} примеров не более чем за {quests_dict['1']['время']} секунд \nна сложности {quests_dict['1']['сложность']} в режиме 1')

    def quest2():
        # Квест про режим 2
        nonlocal parts_of_quests12
        # Реши ... примеров или более за ... секунд на сложности ... в режиме 2
        while True:
            quests_dict['2']['примеры'] = choice(parts_of_quests12['примеры'])
            quests_dict['2']['время'] = choice(parts_of_quests12['время'])
            quests_dict['2']['сложность'] = choice(parts_of_quests12['сложность'])
            difficult_coefficient = 2 if quests_dict['2']['сложность'] == 'Трудно' else 0.5 if quests_dict['2']['сложность'] == 'Легко' else 1
            if quests_dict['2']['время'] / (quests_dict['2']['примеры'] * difficult_coefficient) <= 2.5 or quests_dict['2']['время'] / (quests_dict['2']['примеры'] * difficult_coefficient) >= 5:
                continue
            else:
                return f'2) Реши {quests_dict['2']['примеры']} примеров или более за {quests_dict['2']['время']} секунд \nна сложности {quests_dict['2']['сложность']} в режиме 2'

    def quest3():
        # Общий квест
        quests_dict['3'] = {}
        quests_dict['3']['тип'] = randint(1, 4)
        if quests_dict['3']['тип']==1:
            quests_dict['3']['счёт'] = choice([5000, 10000, 15000])
            return f'3) Установи счёт {quests_dict['3']['счёт']} или более'
        elif quests_dict['3']['тип']==2:
            quests_dict['3']['примеры'] = choice([5, 10, 15, 20])
            quests_dict['3']['прогресс'] = {
                'Возрастающая': 0,
                'Убывающая': 0,
                'Рандомная': 0,
                'Легко': 0,
                'Средне': 0,
                'Трудно': 0
            }
            return f'3) Победи на всех сложностях, решив не менее {quests_dict['3']['примеры']} примеров за каждую игру'
        elif quests_dict['3']['тип']==3:
            quests_dict['3']['примеры'] = choice([20, 40, 50, 80, 100])
            quests_dict['3']['прогресс'] = 0
            return f'3) Реши {quests_dict['3']['примеры']} примеров правильно'
        elif quests_dict['3']['тип']==4:
            quests_dict['3']['счёт'] = choice([5000, 7500, 10000])
            return f'3) Выиграй без ошибок со счётом не менее {quests_dict['3']['счёт']}'

    if not have_quests:
        quests_dict['1']['текст'] = quest1()
        quests_dict['2']['текст'] = quest2()
        quests_dict['3']['текст'] = quest3()
        have_quests = True


    quests_title = Label(root, text='Квесты', font=('Comic Sans MS', 30, 'bold'), bg=global_bg, fg=global_fg)
    quests_title.place(relx=0.5, rely=0.07, anchor='center')

    # Квест 1
    quest1_label = Label(root, text=quests_dict['1']['текст'], font=('Comic Sans MS', 20, 'bold'), justify="left", wraplength=400, bg=global_bg, fg=global_fg)
    quest1_label.place(relx=0.05, rely=0.14, anchor='nw')
    if not completed_q1:
        completed_q1_label = Label(root, text='Не выполнено', fg='red',  font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    else:
        completed_q1_label = Label(root, text='Выполнено', fg='green', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    completed_q1_label.place(relx=0.78, rely=0.175, anchor='n')
    # Применение квеста 1
    def use_quest1():
        global gamemode, start_count, difficult, loss_on_mistake
        gamemode = 1
        start_count = quests_dict['1']['примеры']
        difficult = quests_dict['1']['сложность']
        loss_on_mistake = False
        quests()
    if not completed_q1:
        use_quest1_button = Button(root, text='Применить', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                   command=use_quest1, activebackground=activate_global_bg)
        use_quest1_button.place(relx=0.78, rely=0.25, anchor='n')
        if start_count==quests_dict['1']['примеры'] and gamemode==1 and difficult==quests_dict['1']['сложность']:
            use_quest1_button.configure(text='Применено', state='disabled')


    # Квест 2
    quest2_label = Label(root, text=quests_dict['2']['текст'], font=('Comic Sans MS', 20, 'bold'), justify="left", wraplength=400, bg=global_bg, fg=global_fg)
    quest2_label.place(relx=0.05, rely=0.4, anchor='nw')
    if not completed_q2:
        completed_q2_label = Label(root, text='Не выполнено', fg='red', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    else:
        completed_q2_label = Label(root, text='Выполнено', fg='green', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    completed_q2_label.place(relx=0.78, rely=0.445, anchor='n')
    # Применение квеста 2
    def use_quest2():
        global gamemode, start_time, difficult, loss_on_mistake
        gamemode = 2
        start_time = quests_dict['2']['время']
        difficult = quests_dict['2']['сложность']
        loss_on_mistake = False
        quests()
    if not completed_q2:
        use_quest2_button = Button(root, text='Применить', bg=button_bg, font=('Comic Sans MS', 20, 'bold'),
                                   command=use_quest2, activebackground=activate_global_bg)
        use_quest2_button.place(relx=0.78, rely=0.52, anchor='n')
        if start_time==quests_dict['2']['время'] and gamemode==2 and difficult==quests_dict['2']['сложность']:
            use_quest2_button.configure(text='Применено', state='disabled')


    # Квест 3
    quest3_label = Label(root, text=quests_dict['3']['текст'], font=('Comic Sans MS', 20, 'bold'), justify="left", wraplength=400, bg=global_bg, fg=global_fg)
    quest3_label.place(relx=0.05, rely=0.66, anchor='nw')
    if not completed_q3:
        completed_q3_label = Label(root, text='Не выполнено', fg='red', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
        if quests_dict['3']['тип']==2:
            progress_q3_label = Label(root, text=f'({sum(quests_dict['3']['прогресс'].values())}/{len(quests_dict['3']['прогресс'].values())})', font=('Comic Sans MS', 20), bg=global_bg, fg=global_fg)
        elif quests_dict['3']['тип']==3:
            progress_q3_label = Label(root, text=f'({quests_dict['3']['прогресс']}/{quests_dict['3']['примеры']})', font=('Comic Sans MS', 20), bg=global_bg, fg=global_fg)
    else:
        completed_q3_label = Label(root, text='Выполнено', fg='green', font=('Comic Sans MS', 20, 'bold'), bg=global_bg)
    completed_q3_label.place(relx=0.78, rely=0.74 if quests_dict['3']['тип']==2 else 0.68, anchor='n')
    if quests_dict['3']['тип']==2 or quests_dict['3']['тип']==3 and not completed_q3:
        progress_q3_label.place(relx=0.78, rely=0.8 if quests_dict['3']['тип']==2 else 0.74, anchor='n')

    # Обновление квестов
    def update_quests():
        global have_quests, completed_q1, completed_q2, completed_q3
        if askyesno('Обновление квестов', 'Вы точно хотите обновить квесты?\nВсе квесты будут сброшены'):
            for widget in root.winfo_children():
                widget.destroy()
            have_quests = False
            completed_q1 = completed_q2 = completed_q3 = False
            quests()
    update_quests_button = Button(root, text='Обновить квесты', bg=button_bg, font=('Comic Sans MS', 20, 'bold'), command=update_quests, activebackground=activate_button_bg)
    update_quests_button.place(relx=0, rely=0.9, anchor='nw', relwidth=0.5)

    # Награда за выполнение 3 квестов
    def get_reward():
        global have_quests, completed_q1, completed_q2, completed_q3
        for widget in root.winfo_children():
            widget.destroy()
        have_quests = False
        completed_q1 = completed_q2 = completed_q3 = False
        unlocked_theme = choice([theme_tuple[0] for theme_tuple in unlocked_themes.items() if not theme_tuple[1]]) # Выбирает случайную тему из неразблокированных
        unlocked_themes[unlocked_theme] = True
        info_label = Label(root, text=f'Разблокирована тема "{unlocked_theme.title()}"!', bg=global_bg, fg='green', font=('Comic Sans MS', 20, 'bold'))
        info_label.place(relx=0.5, rely=0.45, anchor='center')
        thanks_button = Button(root, text='В настройки', bg=button_bg, command=lambda: settings(True), font=('Comic Sans MS', 20, 'bold'))
        thanks_button.place(relx=0.5, rely=0.55, anchor='center')
    reward_button = Button(root, text='Получить награду', bg=button_bg, fg='black', font=('Comic Sans MS', 20, 'bold'),
                           state='disabled', command=get_reward, activebackground=activate_global_bg)
    reward_button.place(relx=1, rely=0.9, anchor='ne', relwidth=0.5)
    if completed_q1 and completed_q2 and completed_q3 and (False in unlocked_themes.values()):
        reward_button['state'] = 'normal'
        reward_button['bg'] = 'green'
    elif False not in unlocked_themes.values():
        reward_button['text'] = 'Все награды получены'
def exit():
    ask = askyesnocancel('Выход', 'Сохранить игровой прогресс после выхода?\nПри нажатии "Нет" статистика будет обнулена')
    if ask is True:
        with open(get_save_path(), 'w', encoding='utf-8') as f:
            data = {
                'global_theme': global_theme,
                'unlocked_themes': unlocked_themes,
                'difficult': difficult,
                'start_count': start_count,
                'start_time': start_time,
                'gamemode': gamemode,
                'open_statistics': open_statistics,
                'loss_on_mistake': loss_on_mistake,
                'completed_q1': completed_q1,
                'completed_q2': completed_q2,
                'completed_q3': completed_q3,
                'have_quests': have_quests,
                'quests_dict': quests_dict,
                'max_score': max_score,
                'min_score': min_score,
                'global_starts': global_starts,
                'global_correct': global_correct,
                'global_mistakes': global_mistakes,
                'game_time': time() - game_start_time + game_time,
                'solution_speed': solution_speed,
                'mistakes_frequency': mistakes_frequency,
                'victories_gm1': victories_gm1,
                'timeouts_gm2': timeouts_gm2,
                'surrenders_gm1': surrenders_gm1,
                'surrenders_gm2': surrenders_gm2,
                'starts_dict': starts_dict,
                'loss_on_mistake_count_gm1': loss_on_mistake_count_gm1,
                'loss_on_mistake_count_gm2': loss_on_mistake_count_gm2,
                'correct_counts': correct_counts,
                'mistakes_counts': mistakes_counts,
                'difficult_times': difficult_times
            }
            json.dump(data, f, ensure_ascii=False, indent=2)
        root.destroy()
    elif ask is False:
        with open(get_save_path(), 'w') as f:
            json.dump(None, f)
        root.destroy()
def warning_on_exit():
    if askokcancel('Выход без сохранения', 'При выходе через "x" данные последней игровой сессии не сохраняются'):
        root.destroy()
root.protocol("WM_DELETE_WINDOW", warning_on_exit)
menu()
root.mainloop()