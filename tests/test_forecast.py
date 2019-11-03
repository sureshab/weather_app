import unittest
from unittest import mock
from weather_app.models import forecast
from werkzeug.exceptions import InternalServerError, NotFound


class ForecastGet(unittest.TestCase):

    @mock.patch('weather_app.models.forecast.request', autospec=True)
    @mock.patch('weather_app.models.forecast.app.route', autospec=True)
    @mock.patch('weather_app.models.forecast.parse_temperature', autospec=True)
    @mock.patch('weather_app.utils.process_request.get_json', autospec=True)
    def test_get_internal_server(self, mock_get_json, mock_parse_temp, mock_route, mock_request):
        mock_get_json.return_value = {'cod': '500'}
        mock_request.args = {}
        self.assertRaises(InternalServerError, forecast.get)

    @mock.patch('weather_app.models.forecast.request', autospec=True)
    @mock.patch('weather_app.models.forecast.app.route', autospec=True)
    @mock.patch('weather_app.models.forecast.parse_temperature', autospec=True)
    @mock.patch('weather_app.utils.process_request.get_json', autospec=True)
    def test_get_city_notfound(self, mock_get_json, mock_parse_temp, mock_route, mock_request):
        mock_get_json.return_value = {'cod': '404'}
        mock_request.args = {}
        self.assertRaises(NotFound, forecast.get)

    @mock.patch('weather_app.models.forecast.jsonify', autospec=True)
    @mock.patch('weather_app.models.forecast.request', autospec=True)
    @mock.patch('weather_app.models.forecast.app.route', autospec=True)
    @mock.patch('weather_app.models.forecast.parse_temperature', autospec=True)
    @mock.patch('weather_app.utils.process_request.get_json', autospec=True)
    def test_get(self, mock_get_json, mock_parse_temp, mock_route, mock_request, mock_jsonify):
        result = {'test': 'data'}
        mock_get_json.return_value = {'cod': '200'}
        mock_request.args = {'city': 'Test,IN'}
        mock_parse_temp.return_value = 'test'
        mock_jsonify.return_value = {'test': 'data'}
        self.assertEqual(forecast.get(), result)
        self.assertTrue(mock_parse_temp.called)


if __name__ == '__main__':
    unittest.main()
