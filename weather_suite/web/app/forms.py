from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class WeatherRequest(FlaskForm):
    town = StringField('Введите город', validators=[DataRequired()])
    submit = SubmitField('Получить погоду')

class ViewOldWeather(FlaskForm):
    index = IntegerField('Введите номер', validators=[DataRequired()])
    submit = SubmitField('Посмотреть детально')