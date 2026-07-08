from tkinter import *
from tkinter import ttk
import json
from tkinter import filedialog
from tkinter.messagebox import showerror


# Файл для хранения заметок
FILE = "notes.json"

def show_listbox(select):
    global active_listbox
    active_listbox.destroy()
    active_listbox = Listbox(listbox_frame, width=18, font=("Arial", 17), bg='#eeeeee', selectmode=MULTIPLE)
    for index, string in enumerate(notes_info[select]):
        active_listbox.insert(index, "- " + string)
    active_listbox.pack(fill=BOTH, expand=1)
    if select == "Работа":
        active_listbox['bg'] = '#ffeeee'
    elif select == "Личное":
        active_listbox['bg'] = '#eeffee'
    elif select == "Идеи":
        active_listbox['bg'] = '#eeeeff'

def load_notes():
    global notes_info
    # TODO: Загрузить заметки из JSON, если файл есть, иначе вернуть пустой словарь
    try:
        with open(FILE, 'r') as f:
            notes_info = json.load(f)
    except FileNotFoundError:
        notes_info = {
            'Работа': [],
            'Личное': [],
            'Идеи': []
        }

def save_notes(notes_info):
    # TODO: Сохранить список заметок в JSON
    with open(FILE, 'w') as f:
        json.dump(notes_info, f)

def add_note():
    # TODO: Взять текст из Entry и категорию из Combobox, добавить в список
    category = category_string.get()
    text = add_entry.get().strip()
    if not text:
        add_entry.delete(0, END)
        return 0
    notes_info[category].append(text)
    active_listbox.insert(END, f"- {text}")
    add_entry.delete(0, END)

def delete_note():
    # TODO: Удалить выбранную заметку
    category = category_string.get()
    for index in reversed(active_listbox.curselection()):
        del notes_info[category][index]
        active_listbox.delete(index)
def edit_note():
    # TODO: Загрузить выбранную заметку в поле ввода для редактирования
    if len(active_listbox.curselection())==1:
        index = active_listbox.curselection()[0]
        add_entry.delete(0, END)
        add_entry.insert(0, active_listbox.get(index)[2:])
        delete_note()
def export_notes():
    file_path = filedialog.asksaveasfilename(
        title="Сохранить заметки как",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        defaultextension=".json"
    )
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(notes_info, f, ensure_ascii=False, indent=2)
def import_notes():
    file_path = filedialog.askopenfilename(
        title="Выберите файл заметок",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        global notes_info
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_notes = json.load(f)
            # Проверка структуры (должен быть словарь с теми же категориями)
            if all(cat in new_notes for cat in notes_info):
                notes_info = new_notes
                show_listbox(category_string.get())  # обновление активного списка
            else:
                showerror('Ошибка',"Неверный формат файла")
        except Exception as e:
            showerror("Ошибка", e)
# Создаём окно
root = Tk()
root.title("Мои заметки")
root.geometry("500x400")
# Виджеты
# Область списка слева и область меню справа
listbox_frame = Frame(root, bg="black")
listbox_frame.place(anchor='w', relx=0, relwidth=0.5, rely=0.5, relheight=1)
menu_frame = Frame(root, bg="white")
menu_frame.place(anchor='e', relx=1, relwidth=0.5, rely=0.5, relheight=1)
load_notes()
# Открытие начальной категории
active_listbox = Listbox(listbox_frame, width=18, font=("Arial", 17), bg='#eeeeee', selectmode=MULTIPLE)
for index, string in enumerate(notes_info['Работа']):
    active_listbox.insert(index, "- " + string)
active_listbox.pack(fill=BOTH, expand=1)
active_listbox['bg'] = '#ffeeee'
# Смена категории
categories_title = Label(menu_frame, font=("Arial", 17), text='Категория', bg='white')
categories_title.pack()
category_string = StringVar(value='Работа')
categories = ttk.Combobox(menu_frame, values=('Работа', 'Личное', 'Идеи'), textvariable = category_string, font=("Arial", 12))
categories.pack()
categories.bind("<<ComboboxSelected>>", lambda event: show_listbox(category_string.get()))
# Добавление
add_entry = Entry(menu_frame, font=("Arial", 15))
add_entry.place(relx=0.05, rely=0.3, anchor='nw', relwidth=0.6, relheight=0.1)
add_button = Button(menu_frame, font=("Arial", 25, 'bold'), bg='#eeeeee', text='+', command=add_note)
add_button.place(relx=0.65, rely=0.3, anchor='nw', relwidth=0.2, relheight=0.1)
# Удаление
selected_label = Label(menu_frame, font=("Arial", 20), text='Выделенное: ', bg='white')
selected_label.place(relx=0.5, rely=0.5, anchor='n')
delete_button = Button(menu_frame, font=("Arial", 15), bg='#eeeeee', text='Удалить', command=delete_note)
delete_button.place(relx=0.025, rely=0.6, anchor='nw', relwidth=0.35, relheight=0.1)
edit_button = Button(menu_frame, font=("Arial", 15), bg='#eeeeee', text='Редактировать', command=edit_note)
edit_button.place(relx=0.4, rely=0.6, anchor='nw', relwidth=0.575, relheight=0.1)
# Меню "Файл"
main_menu = Menu(root)
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Экспорт', command=export_notes)
file_menu.add_command(label='Импорт', command=import_notes)
main_menu.add_cascade(menu=file_menu, label='Файл')
root.config(menu=main_menu)

root.mainloop()
save_notes(notes_info)