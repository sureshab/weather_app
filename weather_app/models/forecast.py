from datetime import datetime
from flask import request, abort, jsonify
from weather_app import app
from weather_app.utils import process_request


logger = app.logger


def parse_temperature(data):
    logger.info('--> start of parse_temperature()')
    temp_dict = dict()
    rain_dates = list()
    final_json = []
    logger.info('parsing temperature data from OpenWeatherMap API')
    for item in data['list']:
        date_ = str(datetime.fromtimestamp(item['dt']).date())
        if not temp_dict.get(date_):
            temp_dict[date_] = dict()
        # convert kelvin to degree scale
        temp_dict[date_]['min_temperature'] = round(min(item['main']['temp_min'] - 273.15,
                                                  temp_dict[date_].get('min_temperature', 9999999999)), 2)
        temp_dict[date_]['max_temperature'] = round(max(item['main']['temp_max'] - 273.15,
                                                  temp_dict[date_].get('max_temperature', -9999999999)), 2)
        if item['weather'][0]['main'].lower() == 'rain' and date_ not in rain_dates:
            rain_dates.append(date_)

    logger.info('Parsing city detail from API data')
    if data.get('name'):
        city_name = data['name'] + ', ' + data['sys']['country']
    else:
        city_name = data['city']['name'] + ', ' + data['city']['country']

    logger.info('Updating message based on temperature and preparing finale json data')
    for key in temp_dict:
        temp_dict[key]['city'] = city_name
        temp_dict[key]['date'] = key
        if key in rain_dates:
            temp_dict[key]['message'] = 'Carry Umbrella'
        elif temp_dict[key]['max_temperature'] > 40:
            temp_dict[key]['message'] = 'Use Sunscreen Lotion'
        else:
            temp_dict[key]['message'] = 'Enjoy the weather'
        final_json.append(temp_dict[key])

    logger.info('--> end of parse_temperature()')
    return final_json


@app.route('/forecast')
def get():
    logger.info('--> start of get()')
    app_id = app.config['API_KEY']
    city = request.args.get('city')
    logger.info(f'city is {city}')

    if city is None:
        logger.warning('City was not provided. Selecting Delhi, IN as default city')
        city = 'Delhi, IN'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={app_id}'
    logger.info('reading forecast data from OpenWeatherMap API')
    data = process_request.get_json(forecast_url)
    if data['cod'] in ['200', 200]:
        logger.info('Successfully loaded weather data')
        return jsonify(parse_temperature(data))
    if data['cod'] in ['404', 404]:
        logger.info('City was not found')
        abort(404, f'{city} - city not found')
    else:
        logger.error('OpenWeatherMap API is currently unavailable')
        abort(500, 'Internal Server Error')
