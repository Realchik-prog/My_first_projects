from tkinter import *
import json
from datetime import datetime
from tkinter import messagebox


class Calculation:
    def __init__(self, operand1, operation, operand2, result=None, time=None):
        self.operand1 = operand1
        self.operation = operation
        self.operand2 = operand2
        if result is None:
            if operation == "+":
                self.result = self.operand1 + self.operand2
            elif operation == "-":
                self.result = self.operand1 - self.operand2
            elif operation == "*":
                self.result = self.operand1 * self.operand2
            elif operation == "/":
                self.result = self.operand1 / self.operand2
            if 'e' not in str(self.result):
                if len(str(self.result).split('.')[1]) == 1 and str(self.result).split('.')[1] == '0':
                    self.result = round(self.result)
                elif 'e' not in str(self.operand1) and 'e' not in str(self.operand2):
                    if self.operation == "+" or self.operation == "-":
                        length1 = len(str(operand1).split('.')[1])
                        length2 = len(str(operand2).split('.')[1])
                        if length1 > length2:
                            length = length1
                        else:
                            length = length2
                        self.result = round(self.result, length)
                    elif self.operation == "*":
                        length = 0
                        if not(len(str(self.operand1).split('.')[1]) == 1 and str(self.operand1).split('.')[1] == '0'):
                            length += len(str(self.operand1).split('.')[1])
                        if not(len(str(self.operand2).split('.')[1]) == 1 and str(self.operand2).split('.')[1] == '0'):
                            length += len(str(self.operand2).split('.')[1])
                        self.result = round(self.result, length)
            if 'e' not in str(self.operand1):
                if len(str(self.operand1).split('.')[1]) == 1 and str(self.operand1).split('.')[1] == '0':
                    self.operand1 = round(self.operand1)
            if 'e' not in str(self.operand2):
                if len(str(self.operand2).split('.')[1]) == 1 and str(self.operand2).split('.')[1] == '0':
                    self.operand2 = round(self.operand2)
        else:
            self.result = result
        if time is None:
            self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.time = time
    def to_dict(self):
        return {
            'operand1': self.operand1,
            'operation': self.operation,
            'operand2': self.operand2,
            'result': self.result,
            'time': self.time
        }
    @classmethod
    def from_dict(cls, calculation):
        return cls(calculation['operand1'], calculation['operation'], calculation['operand2'], calculation['result'], calculation['time'])
    def __str__(self):
        return f'{self.operand1} {self.operation} {self.operand2} = {self.result} ({self.time})'
class History:
    def __init__(self):
        self.history = None
    def add_calculation(self, calc):
        self.history.append(calc)
    def delete_history(self):
        if messagebox.askyesno('Удаление истории', 'Вы точно хотите удалить всю историю вычислений?'):
            self.history = []
    def load_history(self):
        try:
            with open('history.json', 'r') as f:
                load_list = json.load(f)
            self.history = [Calculation.from_dict(calculation) for calculation in load_list]
        except FileNotFoundError:
            self.history = []
        except json.decoder.JSONDecodeError:
            messagebox.showerror('Ошибка', 'Ошибка формата файла')
            self.history = []
    def save_history(self):
        with open('history.json', 'w') as file:
            json.dump([calculation.to_dict() for calculation in self.history], file)
    def __str__(self):
        return [calculation + "\n" for calculation in self.history]
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Калькулятор с историей вычислений')
        self.root.geometry('1000x400')
        self.root.resizable(False, False)

        self.hist = History()
        self.hist.load_history()

        self.main_frame = None
        self.history_frame = None
        self.panel_frame = None

        self.demonstrative_entry = None

        self.digit_buttons = None
        self.plus_button = None
        self.minus_button = None
        self.multiplication_button = None
        self.division_button = None
        self.equals_button_button = None
        self.delete_button = None
        self.dot_button = None
        self.erase_button = None

        self.show_full_history_button = None
        self.history_toplevel = None
        self.full_history_listbox = None
        self.delete_history_button = None

        self.queue = 0 # Очередь: 0 - первое число, 1 - операция, 2 - второе число

        self.operand1 = []
        self.operation = None
        self.operand2 = []

        self.setup_ui()

    def setup_ui(self):
        # Фреймы
        self.main_frame = Frame(self.root)
        self.main_frame.place(x=0, y=0, relwidth=0.5, relheight=1)
        self.panel_frame = Frame(self.main_frame)
        self.panel_frame.place(relx=0, rely=0.14, relwidth=1, relheight=0.8)
        self.history_frame = Frame(self.root)
        self.history_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # Окно примера
        self.demonstrative_entry = Entry(self.main_frame, bg='#cccccc', readonlybackground='#cccccc', selectbackground='#777788',
                                         font=('Arial', 36, 'bold'), state='readonly', relief='solid')
        self.demonstrative_entry.pack(side=TOP, fill=X)

        size = 29
        # Цифры
        self.digit_buttons = []
        for i in range(0, 10):
            self.digit_buttons.append(Button(self.panel_frame, text=str(i), bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb'))
        self.digit_buttons[0]['command'] = lambda: self.input_digit(0)
        self.digit_buttons[1]['command'] = lambda: self.input_digit(1)
        self.digit_buttons[2]['command'] = lambda: self.input_digit(2)
        self.digit_buttons[3]['command'] = lambda: self.input_digit(3)
        self.digit_buttons[4]['command'] = lambda: self.input_digit(4)
        self.digit_buttons[5]['command'] = lambda: self.input_digit(5)
        self.digit_buttons[6]['command'] = lambda: self.input_digit(6)
        self.digit_buttons[7]['command'] = lambda: self.input_digit(7)
        self.digit_buttons[8]['command'] = lambda: self.input_digit(8)
        self.digit_buttons[9]['command'] = lambda: self.input_digit(9)
        for i in [1, 4, 7]:
            self.digit_buttons[i].grid(row=i//3, column=0)
        for i in [2, 5, 8]:
            self.digit_buttons[i].grid(row=i//3, column=1)
        for i in [3, 6, 9]:
            self.digit_buttons[i].grid(row=i//3-1, column=2)
        self.digit_buttons[0].grid(row=3, column=1)
        # Точка (Для вещественных чисел)
        self.dot_button = Button(self.panel_frame, text='.', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                  height=1, width=2, activebackground='#bbbbbb',  command=self.input_dot)
        self.dot_button.grid(row=3, column=2)
        # Действия
        self.plus_button = Button(self.panel_frame, text='+', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                  height=1, width=2, activebackground='#bbbbbb',  command=lambda: self.input_operation('+'))
        self.plus_button.grid(row=0, column=3)
        self.minus_button = Button(self.panel_frame, text='-', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb',  command=lambda: self.input_operation('-'))
        self.minus_button.grid(row=1, column=3)
        self.multiplication_button = Button(self.panel_frame, text='x', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb',  command=lambda: self.input_operation('*'))
        self.multiplication_button.grid(row=2, column=3)
        self.division_button = Button(self.panel_frame, text='/', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb', command=lambda: self.input_operation('/'))
        self.division_button.grid(row=3, column=3)
        # Кнопка удаления
        self.delete_button = Button(self.panel_frame, text='C', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb', command=self.clear)
        self.delete_button.grid(row=3, column=0)
        # Кнопка вывода результата
        self.equals_button = Button(self.panel_frame, text='=', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb', command=self.equals)
        self.equals_button.grid(row=1, column=4)
        # Кнопка стирания последнего символа
        self.erase_button = Button(self.panel_frame, text='<--', bg='#aaaaaa', font=('Arial', size, 'bold'),
                                   height=1, width=2, activebackground='#bbbbbb', command=self.erase)
        self.erase_button.grid(row=0, column=4)

        # Мини-история вычислений
        self.mini_history = Listbox(self.history_frame, activestyle='none', font=('Arial', 20),)
        self.mini_history.pack(side=TOP, fill=BOTH, expand=True)
        for i in range(-10, 0):
            try:
                self.mini_history.insert(END, self.hist.history[i])
            except IndexError:
                pass
        # Показать всю историю
        self.show_full_history_button = Button(self.history_frame, text='Показать всю историю', bg='#aaaaaa', font=('Arial', 20, 'bold'),
                                          activebackground='#bbbbbb', command=self.show_full_history)
        self.show_full_history_button.pack(side=BOTTOM)
        # Ввод с клавиатуры
        self.root.bind('<Key>', self.keyboard_input)
    def clear(self):
        self.demonstrative_entry['state'] = 'normal'
        self.demonstrative_entry.delete(0, 'end')
        self.demonstrative_entry['state'] = 'readonly'
        self.queue = 0
        self.operand1 = []
        self.operation = None
        self.operand2 = []
    def input_digit(self, digit):
        self.demonstrative_entry['state'] = 'normal'
        self.demonstrative_entry.insert(END, digit)
        self.demonstrative_entry['state'] = 'readonly'
        if self.queue == 0:
            self.operand1.append(str(digit))
        elif self.queue == 1 or self.queue == 2:
            self.operand2.append(str(digit))
            self.queue = 2
    def input_dot(self):
        self.demonstrative_entry['state'] = 'normal'
        if len(self.demonstrative_entry.get())!=0:
            last_symbol = self.demonstrative_entry.get()[-1]
            if last_symbol in "0123456789":
                if self.queue == 0 and '.' not in self.operand1:
                    self.demonstrative_entry.insert(END, '.')
                    self.operand1.append('.')
                elif self.queue == 2 and '.' not in self.operand2:
                    self.demonstrative_entry.insert(END, '.')
                    self.operand2.append('.')
            elif last_symbol in "+-*/":
                self.queue = 2
                self.demonstrative_entry.insert(END, '0.')
                self.operand2.append('0')
                self.operand2.append('.')
        else:
            self.demonstrative_entry.insert(END, '0.')
            self.operand1.append('0')
            self.operand1.append('.')
        self.demonstrative_entry['state'] = 'readonly'
    def input_operation(self, operation):
        self.demonstrative_entry['state'] = 'normal'
        if self.queue==0 and len(self.demonstrative_entry.get())!=0:
            self.demonstrative_entry.insert(END, operation)
            self.queue = 1
            self.operation = operation
        elif self.queue==1:
            string = self.demonstrative_entry.get()
            self.demonstrative_entry.delete(len(string)-1, 'end')
            self.demonstrative_entry.insert(len(string)-1, operation)
            self.operation = operation
        elif operation=='-' and len(self.demonstrative_entry.get())==0:
            self.demonstrative_entry.insert(END, '-')
            self.operand1.append('-')
        self.demonstrative_entry['state'] = 'readonly'
    def keyboard_input(self, event):
        if event.keysym in "0123456789":
            self.input_digit(event.keysym)
        elif event.keysym=='period':
            self.input_dot()
        elif event.keysym=='plus':
            self.input_operation('+')
        elif event.keysym=='minus':
            self.input_operation('-')
        elif event.keysym=='asterisk':
            self.input_operation('*')
        elif event.keysym=='slash':
            self.input_operation('/')
        elif event.keysym=='Return':
            self.equals()
        elif event.keysym=='BackSpace':
            self.erase()
        elif event.keysym=='Delete':
            self.clear()
    def equals(self):
        self.demonstrative_entry['state'] = 'normal'
        if len(self.operand2)!=0:
            operand1 = float(''.join(self.operand1))
            operand2 = float(''.join(self.operand2))
            if operand2 == 0 and self.operation=='/':
                messagebox.showerror('Ошибка', 'Нельзя делить на ноль')
                self.demonstrative_entry.delete(len(self.demonstrative_entry.get())-2, 'end')
                return None
            calc = Calculation(operand1, self.operation, operand2)
            self.demonstrative_entry.delete(0, 'end')
            self.demonstrative_entry.insert(0, calc.result)
            self.queue = 0
            self.operand1 = list(str(calc.result))
            self.operation = None
            self.operand2 = []
            self.hist.add_calculation(calc)
            self.update_history_display()
        self.demonstrative_entry['state'] = 'readonly'
    def erase(self):
        self.demonstrative_entry['state'] = 'normal'
        if len(self.demonstrative_entry.get())>0:
            erase_symbol = self.demonstrative_entry.get()[-1]
            next_symbol = self.demonstrative_entry.get()[-2] if len(self.demonstrative_entry.get())>=2 else ''
            if erase_symbol in "0123456789.":
                if next_symbol in "0123456789." or next_symbol=='':
                    self.demonstrative_entry.delete(len(self.demonstrative_entry.get())-1, END)
                    if self.queue == 2:
                        self.operand2.pop()
                    elif self.queue == 0:
                        self.operand1.pop()
                elif next_symbol in "+-*/" and self.queue == 2:
                    self.demonstrative_entry.delete(len(self.demonstrative_entry.get())-1, END)
                    self.queue = 1
                    self.operand2.pop()
                else:
                    self.demonstrative_entry.delete(len(self.demonstrative_entry.get()) - 1, END)
                    self.operand1.pop()
            elif erase_symbol in "+-*/":
                self.demonstrative_entry.delete(len(self.demonstrative_entry.get())-1, END)
                self.queue = 0
                self.operation = None
        self.demonstrative_entry['state'] = 'readonly'
    def show_full_history(self):
        # Создание дочернего окна
        self.history_toplevel = Toplevel(self.root)
        self.history_toplevel.title('История вычислений')

        # Список вычислений
        self.full_history_listbox = Listbox(self.history_toplevel, font='Arial 15 bold', width=60, height=25, borderwidth=10, activestyle='none')
        self.full_history_listbox.pack()
        for calculation in self.hist.history:
            self.full_history_listbox.insert(END, calculation)
        if self.hist.history == []:
            self.full_history_listbox.insert(END, 'Пока что тут ничего нет')
        # Кнопки
        self.delete_history_button = Button(self.history_toplevel, text='Удалить историю', bg='#aaaaaa', font=('Arial', 10, 'bold'),
                                   activebackground='#bbbbbb', command=lambda: (self.hist.delete_history(), self.update_history_display()))
        self.delete_history_button.pack(anchor='nw')
    def update_history_display(self):
        self.mini_history.delete(0, END)
        for i in range(-10, 0):
            try:
                self.mini_history.insert(END, self.hist.history[i])
            except IndexError:
                pass
        try:
            if self.history_toplevel:
                self.full_history_listbox.delete(0, END)
                for calculation in self.hist.history:
                    self.full_history_listbox.insert(END, calculation)
                if self.hist.history == []:
                    self.full_history_listbox.insert(END, 'Пока что тут ничего нет')
        except TclError:
                    pass

if __name__ == '__main__':
    root = Tk()
    app = CalculatorApp(root)
    root.mainloop()
    app.hist.save_history()

# "9.309+0.1 = 9.40899999999999..." - исправлено с помощью проверок self.result