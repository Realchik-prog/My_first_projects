import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.weather_core import get_weather, API_KEY, instruction, \
show_history, get_old_weather, clear_history
from app import app
from flask import render_template, redirect, url_for
from flask import request as req
from app.forms import WeatherRequest, ViewOldWeather
import sqlite3
from more_itertools import peekable

database = Path(__file__).parent.parent.parent / 'core' / 'history.db'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if API_KEY is None:
        return render_template('instruction.html', instruction=instruction())
    
    form = WeatherRequest()
    if form.validate_on_submit():
        errors = []
        connection = sqlite3.connect(database)
        response = get_weather(form.town.data, thread_connect=connection)
        connection.commit()
        connection.close()
        if not response.startswith('\nСтрана:'):
            errors.append(response)
            response = None
        else:
            response = response.split('\n')
        return render_template('view.html', form=form, 
                               response=response, errors=errors)
    return render_template('view.html', form=form)

@app.route('/history', methods=['GET', 'POST'])
def history():
    connection = sqlite3.connect(database)
    history = show_history(thread_connect=connection)
    history = peekable(history)
    if history.peek() == 'Истории нет':
        return render_template('no_history.html')
    view = ViewOldWeather()
    errors = []
    if view.validate_on_submit():
        connection = sqlite3.connect(database)
        try:
            response = get_old_weather(view.index.data, thread_connect=connection).split('\n')
        except IndexError:
            errors.append('Данный номер строки отсутствует')
            response = None
        connection.commit()
        connection.close()
        return render_template('history.html', history=history,
                               view=view, response=response, errors=errors)
    return render_template('history.html', history=history, view=view)
@app.route('/history/delete', methods=['GET', 'POST'])
def delete_history():
    if req.method == 'POST':
        action = req.form.get('action')
        if action == 'confirm':
            connection = sqlite3.connect(database)
            clear_history(thread_connect=connection)
            connection.commit()
            connection.close()
        return redirect(url_for('history'))
    return render_template('delete_history.html')