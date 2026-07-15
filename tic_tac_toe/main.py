from random import choice
from time import sleep
from typing import Optional

class Cell:
    # Создание клетки
    sign: str = '*'
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

class TicTacToe_game:
    def __init__(self):
        self.area: list[Cell] = []
        self.possible: set = set()
    def print_area(self) -> None:
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

    def computer_choice(self) -> None:
        # Ход компьютера
        selected_cell: Optional[Cell] = None
        print()
        print('Ход компьютера')
        unpossible: set = set(self.area) - self.possible
        for sign in ['x', 'o']:
            if selected_cell is None:
                # Компьютер смотрит оси x и y
                for axle_variant in [1, 2]:
                    cell_pos: Optional[int] = None
                    for x_pos in range(1, 4):
                        length: int = 0
                        possible_pos: Optional[int] = None
                        for y_pos in range(1, 4):
                            if axle_variant == 1:
                                # Компьютер смотрит вертикальную ось
                                cell_pos = self.list_format_coordinates(x_pos, y_pos)
                            else:
                                # Компьютер смотрит горизонтальную ось
                                cell_pos = self.list_format_coordinates(y_pos, x_pos)
                            if self.area[cell_pos].sign == sign:
                                length += 1
                                continue
                            if self.area[cell_pos].sign == '*':
                                possible_pos = cell_pos
                        if length == 2 and possible_pos is not None:
                            selected_cell = self.area[possible_pos]
                            if sign == 'o':
                                print('Компьютер защитился по горизонтали')
                            break
            
                # Компьютер смотрит диагонали
                for line in ([0, 4, 8], [6, 4, 2]):
                    length: int = 0
                    possible_pos: Optional[int] = None
                    for cell_pos in line:
                        if self.area[cell_pos].sign==sign:
                            length += 1
                            continue
                        if self.area[cell_pos].sign == '*':
                            possible_pos = cell_pos
                    if length==2 and possible_pos is not None:
                        selected_cell = self.area[possible_pos]
            
        if selected_cell is None:
            selected_cell = choice(list(self.possible))
        self.possible.remove(selected_cell)
        selected_cell.sign = 'x'
        self.print_area()

    def player_choice(self) -> None:
        # Ход игрока
        print()
        print('Ваш ход')
        while True:
            try:
                x: int = int(input('Выберите координату по горизонтали (x): '))
                y: int = int(input('Выберите координату по вертикали (y): '))
                if x not in [1, 2, 3] or y not in [1, 2, 3]:
                    print('Данной клетки нет в игровом поле')
                    continue
                selected_cell: Cell = self.area[x-1+(y-1)*3]
                if selected_cell in self.possible:
                    self.possible.discard(selected_cell)
                    selected_cell.sign = 'o'
                    self.print_area()
                    break
                print('На эту клетку невозможно сходить')
            except ValueError:
                print('Неправильный ввод')

    def check_victory(self, sign: str) -> bool:
        victory: bool = False
        try:
            # Проверяем по вертикали
            for x_pos in range(1, 4):
                for y_pos in range(1, 4):
                    cell_pos = self.list_format_coordinates(x_pos, y_pos)
                    if self.area[cell_pos].sign==sign:
                        if y_pos==3:
                            victory = True
                            return True
                        continue
                    break
            # Проверяем по горизонтали
            for y_pos in range(1, 4):
                for x_pos in range(1, 4):
                    cell_pos = self.list_format_coordinates(x_pos, y_pos)
                    if self.area[cell_pos].sign==sign:
                        if x_pos==3:
                            victory = True
                            return True
                        continue
                    break
            # Проверяем по диагонали
            for line in ([0, 4, 8], [6, 4, 2]):
                for cell_pos in line:
                    if self.area[cell_pos].sign==sign:
                        if cell_pos==line[2]:
                            victory = True
                            return True
                        continue
                    break
        finally:
            if victory:
                print()
                if sign=='x':
                    print('Компьютер выиграл раунд!')
                elif sign=='o':
                    print('Вы выиграли раунд!')
        return False
    def restart_area(self) -> None:
        # Перезапуск поля игры для нового раунда
        self.area = [ # Поле игры в виде списка клеток с координатами
            Cell(1,1), Cell(2,1), Cell(3,1),
            Cell(1,2), Cell(2,2), Cell(3,2),
            Cell(1,3), Cell(2,3), Cell(3,3)
        ]
        self.possible = set(self.area) # Незанятые клетки
        self.print_area()
    def fake_computer_choice(self) -> None:
        print()
        print('Ход компьютера (Выбираете вы)')
        while True:
            try:
                x = int(input('Выберите координату по горизонтали (x): '))
                y = int(input('Выберите координату по вертикали (y): '))
                if x not in [1, 2, 3] or y not in [1, 2, 3]:
                    print('Данной клетки нет в игровом поле')
                    continue
                selected_cell: Cell = self.area[x - 1 + (y - 1) * 3]
                if selected_cell in self.possible:
                    self.possible.discard(selected_cell)
                    selected_cell.sign = 'x'
                    self.print_area()
                    break
                print('На эту клетку невозможно сходить')
            except ValueError:
                print('Неправильный ввод')
    @staticmethod
    def list_format_coordinates(x: int, y: int) -> int:
        return (x - 1) + 3 * (y - 1)
    def mode_battle(self) -> None:
        while True:
            try:
                rounds: int = int(input('Сколько хотите раундов?: '))
                if rounds>0:
                    break
                else:
                    print('Неположительное число')
            except ValueError:
                print('Неправильный ввод')
    
        player_count: int = 0
        computer_count: int = 0
        for round in range(1, rounds+1):
            # Каждая итерация - 1 раунд
            print()
            print(f'РАУНД {round}/{rounds}')
            sleep(1)
            self.restart_area()
            sleep(1)
            count: int = 0
            while True:
                count += 1
                if count % 2 == round % 2:
                    self.player_choice()
                    sleep(1)
                    if self.check_victory('o'):
                        player_count += 1
                        break
                else:
                    self.computer_choice()
                    sleep(1)
                    if self.check_victory('x'):
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
    def mode_sandbox(self) -> None:
        self.restart_area()
        while True:
            print()
            print('Панель управления: ')
            print('1. Ход игрока')
            print('2. Ход компьютера')
            print('3. Ручной ход за компьютер')
            print('4. Рестарт игровой арены')
            print('0. Выход из программы')
            a: str = input().strip()
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
                self.fake_computer_choice()
            elif a == '4':
                self.restart_area()
            elif a == '0':
                break
            else:
                print('Ничего не выбрано')

    def setup(self) -> None:
        print('Это игра "Крестики-нолики" с компьютером! Вы играете за нолики, компьютер - за крестики')
        print()
        print('Режимы игры:')
        print('1. Сражение (Классический)')
        print('2. Песочница')
        while True:
            print()
            mode: str = input('Выберите режим игры (цифра): ')
            if mode == '1':
                print('Выбран режим "Сражение"')
                break
            elif mode == '2':
                print('Выбран режим "Песочница"')
                break
            else:
                print('Режим не выбран')
        if mode == '1':
            self.mode_battle()
        elif mode == '2':
            self.mode_sandbox()

if __name__ == '__main__':
    area = TicTacToe_game()
    area.setup()



