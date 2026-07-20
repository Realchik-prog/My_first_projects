import sqlite3
import requests
from datetime import datetime
from requests.exceptions import RequestException, Timeout
from pathlib import Path
from typing import Generator, Optional
import logging
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

weather_logger = logging.getLogger('Логгер приложения погоды')
weather_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(Path(__file__).parent / "weather.log", 
                                   encoding="utf-8", mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
weather_logger.addHandler(file_handler)

weather_logger.debug("Запуск программы")


def get_weather(input_town: str) -> str:
    input_town = input_town.strip().title()
    weather_logger.info(f'Пользователь ввёл город: {input_town}')
    url: str = "https://api.openweathermap.org/data/2.5/weather"
    try: 
        params: dict[str, str | None] = {'q': input_town, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 404:
            weather_logger.warning('Город не найден')
            return "Город не найден. Проверьте название."
        response.raise_for_status()
        
        json_data: dict = response.json()
        
        country: str = json_data['sys']['country']
        town: str = json_data['name']
        description: str = json_data['weather'][0]['description'].title()
        temp: int = round(json_data['main']['temp'])
        pressure: int = json_data['main']['pressure']
        humidity: int = json_data['main']['humidity']
        time: str = datetime.now().strftime("%Y.%m.%d %H:%M")
        weather_logger.info('Информация о погоде успешно отражена')
    except Timeout:
        weather_logger.error('Превышено время ожидания от сервера')
        return 'Превышено время ожидания от сервера'
    except RequestException as e:
        weather_logger.error(f'Ошибка при запросе: {e}')
        return f'Ошибка при запросе: {e}'
    except KeyError:
        weather_logger.error(f'Неожиданный формат ответа от сервера')
        return 'Неожиданный формат ответа от сервера'
        
    cursor.execute(
        """INSERT INTO weather_history 
        (country, town, description, temp, pressure, humidity, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (country, town, description, temp, pressure, humidity, time))
    
    return (f'''\nСтрана: {country}
Город: {town}
Описание: {description}
Температура: {temp} °C
Давление: {pressure} мбар
Влажность: {humidity} %
        ''')
        
    
def save_weather() -> None:
    weather_logger.debug('Сохранение данных и завершение программы')
    connection.commit()
    connection.close()
    weather_logger.info('Данные сохранены')
    
def show_history() -> Generator[str]:
    weather_logger.info('Пользователь запрашивает показ истории')
    cursor.execute("SELECT country, town, description, temp, pressure, humidity, time from weather_history")
    weathers: list[tuple] = cursor.fetchall()
    if not weathers:
        weather_logger.info('Истории нет')
        yield 'Истории нет'
    else:
        weather_logger.debug('Вывод истории')
        i = 0
        for weather in weathers:
            weather_string: str = (f'{weather[0]}, {weather[1]}: {weather[2]}, {weather[3]} °C,' +
                                f' {weather[4]} мбар, {weather[5]} % ({weather[6]})')
            i += 1
            yield f'{i}) {weather_string}'
        weather_logger.info('Выведена история')
def get_old_weather(index: int) -> str:
    weather_logger.info('Пользователь выбрал старый запрос погоды')
    cursor.execute("SELECT country, town, description, temp, pressure, humidity, time from weather_history")
    weathers: list[tuple] = cursor.fetchall()
    i = 0
    for weather in weathers:
        i += 1
        if i == index:
            weather_logger.info('Нужный запрос успешно найден')
            return (f'''\nСтрана: {weather[0]}
Город: {weather[1]}
Описание: {weather[2]}
Температура: {weather[3]} °C
Давление: {weather[4]} мбар
Влажность: {weather[5]} %
        ''')
    weather_logger.error('Несуществующий индекс')
    raise IndexError
    
def instruction() -> Generator[str]:
    weather_logger.error("Не найден API-ключ")
    yield "API-ключ не найден!"
    yield "\n" + "="*60
    yield "Для работы с погодой нужно получить бесплатный ключ OpenWeatherMap:"
    yield "1. Зайдите на сайт: https://openweathermap.org/"
    yield "2. Зарегистрируйтесь и получите API-ключ."
    yield "3. Создайте в папке с программой файл config.py"
    yield "   и напишите в нём: API_KEY = 'ваш_ключ'"
    yield "="*60 + "\n"
    weather_logger.info('Инструкция по API-ключу выдана')
    
def clear_history() -> str:
    weather_logger.debug('Удаление истории')
    cursor.execute("DELETE FROM weather_history")
    weather_logger.info('История удалена')
    return "История успешно удалена"