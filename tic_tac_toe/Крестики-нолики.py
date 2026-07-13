from random import choice
from time import sleep

class Cell:
    # Создание клетки
    sign = '*'
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TicTacToe_game:
    def __init__(self):
        self.area = None
        self.possible = None
    def print_area(self):
        # Изображение поля игры
        y_position = None
        for cell in self.area:
            if cell.y != y_position:
                print()
                print(cell.y, end='  ')
            print(cell.sign, end='  ')
            y_position = cell.y
        print()
        print('   ', end='')
        for x in range(1, int(len(self.area)**0.5)+1):
            print(x, end='  ')
        print()

    def computer_choice(self):
        # Ход компьютера
        print()
        print('Ход компьютера')
        is_necessary_move = False
        unpossible = set(self.area) - self.possible
        for pos in range(1, 4):
            for sign in ['x', 'o']:
                if not is_necessary_move:
                    if len(list(filter(lambda x: x == pos, map(lambda cell: cell.x if cell.sign==sign else 0, list(unpossible)))))==2:
                        # Если стоит 2 кружка/крестика по вертикали
                        for cell in self.possible:
                            if cell.x == pos:
                                selected_cell = cell
                                is_necessary_move = True
                                if sign == 'o':
                                    print('Компьютер защитился по вертикали')
                                else:
                                    print('Компьютер захотел выиграть по вертикали')
                                break
                    if len(list(filter(lambda y: y == pos, map(lambda cell: cell.y if cell.sign==sign else 0, list(unpossible)))))==2:
                        # Если стоит 2 кружка/крестика по горизонтали
                        for cell in self.possible:
                            if cell.y == pos:
                                selected_cell = cell
                                is_necessary_move = True
                                if sign == 'o':
                                    print('Компьютер защитился по горизонтали')
                                else:
                                    print('Компьютер захотел выиграть по горизонтали')
                                break
                    if True:
                        for cell_poss1, cell_poss2, cell_poss3 in [(0, 4, 8), (6, 4, 2)]:
                            if (1 if self.area[cell_poss1].sign == sign else 0) + (1 if self.area[cell_poss2].sign == sign else 0) + (1 if self.area[cell_poss3].sign == sign else 0) == 2:
                                # Если стоит 2 кружка/крестика по диагонали
                                for cell_poss in [cell_poss1, cell_poss2, cell_poss3]:
                                    if self.area[cell_poss].sign == '*':
                                        selected_cell = self.area[cell_poss]
                                        is_necessary_move = True
                                        if sign == 'o':
                                            print('Компьютер защитился по диагонали')
                                        else:
                                            print('Компьютер захотел выиграть по диагонали')
                                        break
        if not is_necessary_move:
            selected_cell = choice(list(self.possible))
        self.possible.remove(selected_cell)
        selected_cell.sign = 'x'
        self.print_area()

    def player_choice(self):
        # Ход игрока
        print()
        print('Ваш ход')
        while True:
            try:
                x = int(input('Выберите координату по горизонтали (x): '))
                y = int(input('Выберите координату по вертикали (y): '))
                if x not in [1, 2, 3] or y not in [1, 2, 3]:
                    print('Данной клетки нет в игровом поле')
                    continue
                selected_cell = self.area[x-1+(y-1)*3]
                if selected_cell in self.possible:
                    self.possible.discard(selected_cell)
                    selected_cell.sign = 'o'
                    self.print_area()
                    break
                print('На эту клетку невозможно сходить')
            except ValueError:
                print('Неправильный ввод')


    def check_player_victory(self):
        # Проверка, победил ли после хода игрок
        unpossible = set(self.area) - self.possible
        for x_pos in range(1, 4):
            if len(list(filter(lambda x: x == x_pos, map(lambda cell: cell.x if cell.sign=='o' else 0, list(unpossible)))))==3:
                # Если 3 кружка по вертикали
                print()
                print('Вы выиграли раунд!')
                return True
        for y_pos in range(1, 4):
            if len(list(filter(lambda y: y == y_pos, map(lambda cell: cell.y if cell.sign=='o' else 0, list(unpossible)))))==3:
                # Если 3 кружка по горизонтали
                print()
                print('Вы выиграли раунд!')
                return True
        if self.area[0].sign=='o' and self.area[4].sign=='o' and self.area[8].sign=='o' or self.area[6].sign=='o' and self.area[4].sign=='o' and self.area[2].sign=='o':
            # Если 3 кружка по диагонали
            print()
            print('Вы выиграли раунд!')
            return True

    def check_computer_victory(self):
        # Проверка, победил ли после хода компьютер
        unpossible = set(self.area) - self.possible
        for x_pos in range(1, 4):
            if len(list(filter(lambda x: x == x_pos, map(lambda cell: cell.x if cell.sign == 'x' else 0, list(unpossible))))) == 3:
                # Если 3 кружка по вертикали
                print()
                print('Компьютер выиграл раунд!')
                return True
        for y_pos in range(1, 4):
            if len(list(filter(lambda y: y == y_pos, map(lambda cell: cell.y if cell.sign == 'x' else 0, list(unpossible))))) == 3:
                # Если 3 кружка по горизонтали
                print()
                print('Компьютер выиграл раунд!')
                return True
        if self.area[0].sign == 'x' and self.area[4].sign == 'x' and self.area[8].sign == 'x' or self.area[6].sign == 'x' and self.area[4].sign == 'x' and self.area[2].sign == 'x':
            # Если 3 кружка по диагонали
            print()
            print('Компьютер выиграл раунд!')
            return True
    def restart_area(self):
        # Перезапуск поля игры для нового раунда
        self.area = [ # Поле игры в виде списка клеток с координатами
            Cell(1,1), Cell(2,1), Cell(3,1),
            Cell(1,2), Cell(2,2), Cell(3,2),
            Cell(1,3), Cell(2,3), Cell(3,3)
        ]
        self.possible = set(self.area) # Незанятые клетки
        self.print_area()

    def setup(self):
        print('Это игра "Крестики-нолики" с компьютером! Вы играете за нолики, компьютер - за крестики')
        print()
        print('Режимы игры:')
        print('1. Сражение (Классический)')
        print('2. Песочница')
        while True:
            print()
            mode = input('Выберите режим игры (цифра): ')
            if mode == '1':
                print('Выбран режим "Сражение"')
                break
            elif mode == '2':
                print('Выбран режим "Песочница"')
                break
            else:
                print('Режим не выбран')
        if mode == '1':
            while True:
                try:
                    rounds = int(input('Сколько хотите раундов?: '))
                    if rounds>0:
                        break
                    else:
                        print('Неположительное число')
                except ValueError:
                    print('Неправильный ввод')

            player_count = computer_count = 0
            for round in range(1, rounds+1):
                # Каждая итерация - 1 раунд
                print()
                print(f'РАУНД {round}/{rounds}')
                sleep(1)
                self.restart_area()
                sleep(1)
                count = 0
                while True:
                    count += 1
                    if count % 2 == round % 2:
                        self.player_choice()
                        sleep(1)
                        if self.check_player_victory():
                            player_count += 1
                            break
                    else:
                        self.computer_choice()
                        sleep(1)
                        if self.check_computer_victory():
                            computer_count += 1
                            break
                    if self.possible==set():
                        print()
                        print('Ничья!')
                        break
                if round!=rounds:
                    print(f'Счёт {player_count}:{computer_count}', end='')
                    if player_count > computer_count:
                        print(' в вашу пользу')
                    elif player_count < computer_count:
                        print(' в пользу компьютера')
                    else:
                        print(' в ничью')
                else:
                    print()
                    print(f'Финальный счёт {player_count}:{computer_count}!')
                sleep(1)
            if player_count == computer_count:
                print('Вы сыграли в ничью!')
            elif player_count > computer_count:
                print('Вы одержали победу!')
            else:
                print('Вы проиграли!')
        elif mode == '2':
            def fake_computer_choice():
                print()
                print('Ход компьютера (Выбираете вы)')
                while True:
                    try:
                        x = int(input('Выберите координату по горизонтали (x): '))
                        y = int(input('Выберите координату по вертикали (y): '))
                        if x not in [1, 2, 3] or y not in [1, 2, 3]:
                            print('Данной клетки нет в игровом поле')
                            continue
                        selected_cell = self.area[x - 1 + (y - 1) * 3]
                        if selected_cell in self.possible:
                            self.possible.discard(selected_cell)
                            selected_cell.sign = 'x'
                            self.print_area()
                            break
                        print('На эту клетку невозможно сходить')
                    except ValueError:
                        print('Неправильный ввод')
            self.restart_area()
            while True:
                print()
                print('Панель управления: ')
                print('1. Ход игрока')
                print('2. Ход компьютера')
                print('3. Ручной ход за компьютер')
                print('4. Рестарт игровой арены')
                print('5. Выход из программы')
                a = input()
                if (a == '1' or a == '2' or a == '3') and self.possible==set():
                    print('Все клетки заняты, нельзя сходить')
                elif a == '1':
                    self.print_area()
                    self.player_choice()
                elif a == '2':
                    self.print_area()
                    self.computer_choice()
                elif a == '3':
                    self.print_area()
                    fake_computer_choice()
                elif a == '4':
                    self.restart_area()
                elif a == '5':
                    break
                else:
                    print('Ничего не выбрано')

if __name__ == '__main__':
    area = TicTacToe_game()
    area.setup()



