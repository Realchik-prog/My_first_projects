import tkinter as tk
from tkinter import messagebox
from weather_core import API_KEY, get_weather, show_history, clear_history, save_weather, \
instruction, get_old_weather
from pathlib import Path

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Погодный информер")
        self.root.geometry("1200x500")
        self.root.resizable(True, False)
        self.root.iconbitmap(Path(__file__).parent / 'icon.ico')
        self.setup_ui()
        self.update_history()

    def setup_ui(self):
        # Основной фрейм
        self.main_frame = tk.Frame(self.root)
        self.main_frame.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=1, anchor='center')
        
        # Информационный фрейм
        self.info_frame = tk.Frame(self.main_frame, bg="#F9FAB5")
        self.info_frame.place(relx=0.5, rely=0.75, relwidth=1, relheight=0.5, anchor='center')
        self.info_label = tk.Label(self.info_frame, bg="#F9FAB5", justify='left', 
                                   font=('Comic Sans MS', 18, 'bold'), padx=20)
        self.info_label.pack(side='left')
        
        # Фрейм панели
        self.panel_frame = tk.Frame(self.main_frame)
        self.panel_frame.place(relx=0.5, rely=0.25, relwidth=1, relheight=0.5, anchor='center')
        self.input_town_label = tk.Label(self.panel_frame, text='Введите город',
                                         font = ('Comic Sans MS', 20, 'bold'), pady=20)
        self.input_town_label.place(relx=0.5, rely=0.3, anchor='center')
        self.town_entry = tk.Entry(self.panel_frame, font="Arial 20")
        self.town_entry.place(relx=0.5, rely=0.5, anchor='center')
        self.get_weather_button = tk.Button(self.panel_frame, text='Получить погоду', 
                                            font="Arial 20", command=self.on_get_weather)
        self.get_weather_button.place(relx=0.5, rely=0.7, anchor='center')
        self.root.bind('<Return>', lambda event: self.on_get_weather())
        
        
        # Фрейм истории
        self.history_frame = tk.Frame(self.root, bg="#D7F3F5")
        self.history_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor='center')
        self.history_title = tk.Label(self.history_frame, text='История', bg='#D7F3F5',
                                      font = ('Comic Sans MS', 20, 'bold'))
        self.history_title.pack()
        self.history_listbox = tk.Listbox(self.history_frame, bg="#D7F3F5", font=('Comic Sans MS', 14, 'bold'))
        self.history_listbox.place(relheight=0.75, relwidth=1, relx=0.5, rely=0.1, anchor='n')
        self.get_weather_from_history_button = tk.Button(self.history_frame, font=('Comic Sans MS', 20, 'bold'),
                                                         text='Посмотреть', padx=20, command=self.view_weather)
        self.get_weather_from_history_button.place(anchor='nw', relx=0.05, rely=0.86)
        self.clear_history_button = tk.Button(self.history_frame, text='Очистить историю', padx=20,
                                              font=('Comic Sans MS', 20, 'bold'), command=self.on_clear_history)
        self.clear_history_button.place(anchor='ne', relx=0.95, rely=0.86)
        
    def view_weather(self) -> None:
        index = self.history_listbox.curselection()[0] + 1
        self.info_label['text'] = get_old_weather(index)

    def on_get_weather(self):
        if API_KEY is None:
            # Если нет API-ключа, даём инструкцию в дочернем окне
            instruction_toplevel = tk.Toplevel(self.root)
            instruction_toplevel.title('Инструкция по API-ключу')
            instruction_toplevel.geometry('800x350')
            instruction_toplevel.grab_set()
            instruction_label = tk.Label(instruction_toplevel, justify='left', text='', 
                                         font=('Comic Sans MS', 15, 'bold'))
            for i in instruction():
                instruction_label['text'] += i + '\n'
            instruction_label.pack()
            return
        town = self.town_entry.get()
        if town.strip() == '':
            return
        weather = get_weather(town)
        if not weather.startswith('\nСтрана:'):
            self.info_label['text'] = ''
            messagebox.showerror('Ошибка', weather)
            return
        self.town_entry.delete(0, tk.END)
        self.info_label['text'] = weather
        self.update_history()


    def on_clear_history(self):
        if messagebox.askyesno('Удаление истории', 'Вы точно хотите удалить историю?'):
            clear_history()
            self.update_history()
    
    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for weather in show_history():
            if weather != 'Истории нет':
                weather = weather.split(", ")
                weather = '- ' + weather[1] + ' ' + weather[4].lstrip(" %0123456789")
                self.history_listbox.insert(tk.END, weather)

    def on_close(self):
        save_weather()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()