from weather_core import API_KEY, get_weather, \
save_weather, show_history, instruction, clear_history
        

print('Это программа для просмотра погоды!')
try:
    while True:
        print("""\nМеню действий:
    1. Посмотреть погоду сейчас
    2. Посмотреть историю запросов
    3. Удалить всю историю
    0. Выход\n""")
        command: str = input("> ").strip()
        print()
        if command=='1':
            if API_KEY is None:
                for string in instruction():
                    print(string)
            else:
                town: str = input('Введите название города: ').strip().title()
                print(get_weather(town))
        elif command=='2':
            for i in show_history():
                print(i)
        elif command=='3':
            print(clear_history())
        elif command=='0':
            break
        else:
            print('Неопознанная команда')
finally:
    save_weather()
