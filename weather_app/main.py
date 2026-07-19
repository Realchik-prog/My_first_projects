import requests
from requests.exceptions import RequestException
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
try:
    from config import API_KEY
except ImportError:
    API_KEY: Optional[str] = None
    
HISTORY_FILE: Path = Path(__file__).parent / 'history.db'
connection = sqlite3.connect(HISTORY_FILE)
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_history (
        country TEXT NOT NULL,
        town TEXT NOT NULL,
        description TEXT NOT NULL,
        temp INT NOT NULL,
        pressure INT NOT NULL,
        humidity INT NOT NULL,
        time TEXT NOT NULL
    )
""")

    
def get_weather() -> None:
    url: str = "https://api.openweathermap.org/data/2.5/weather"
    try:
        town: str = input('Введите название города: ').strip().title() 
        params: dict[str, str] = {'q': town, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'}
        response = requests.get(url, params=params)
        if response.status_code == 404:
            print("Город не найден. Проверьте название.")
            return
        response.raise_for_status()
        json_data: dict = response.json()
        
        country: str = json_data['sys']['country']
        town: str = json_data['name']
        description: str = json_data['weather'][0]['description']
        temp: int = round(json_data['main']['temp'])
        pressure: int = json_data['main']['pressure']
        humidity: int = json_data['main']['humidity']
        time: str = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        
        print(f'''\nСтрана: {country}
Город: {town}
Описание: {description}
Температура: {temp} °C
Давление: {pressure} мбар
Влажность: {humidity} %
              ''')
        
        cursor.execute(
            """INSERT INTO weather_history 
            (country, town, description, temp, pressure, humidity, time)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (country, town, description, temp, pressure, humidity, time))
        
        
    except RequestException as e:
        print('Ошибка при запросе:', e)
    except KeyError:
        print('Неожиданный формат ответа от сервера') 
        
def instruction() -> None:
    print("\n" + "="*60)
    print("Для работы с погодой нужно получить бесплатный ключ OpenWeatherMap:")
    print("1. Зайдите на сайт: https://openweathermap.org/")
    print("2. Зарегистрируйтесь и получите API-ключ.")
    print("3. Создайте в папке с программой файл config.py")
    print("   и напишите в нём: API_KEY = 'ваш_ключ'")
    print("="*60 + "\n")
    
def show_history() -> None:
    cursor.execute("SELECT country, town, description, temp, pressure, humidity, time from weather_history")
    weathers: list[tuple] = cursor.fetchall()
    if weathers:
        i = 0
        for weather in weathers:
            weather_string: str = (f'{weather[0]}, {weather[1]}: {weather[2]}, {weather[3]} °C,' +
                              f' {weather[4]} мбар, {weather[5]} % ({weather[6]})')
            i += 1
            print(f'{i}) {weather_string}')
    else:
        print('Истории нет')


print('Это программа для просмотра погоды!')
try:
    while True:
        print("""\nМеню действий:
    1. Посмотреть погоду сейчас
    2. Посмотреть историю запросов
    0. Выход\n""")
        command: str = input("> ").strip()
        print()
        if command=='1':
            if API_KEY is None:
                print('API-ключ не найден!')
                instruction()
            else:
                get_weather()
        elif command=='2':
            show_history()
        elif command=='0':
            break
finally:
    connection.commit()
    connection.close()
