import unittest
from unittest import mock
from jsonschema import validate
import weather_app


class WeatherAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = weather_app.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to weather_app', rv.data.decode())

    def test_forecast(self):
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["city", "date", "max_temperature", "message", "min_temperature"],
                "properties": {
                    "city": {"type": "string"},
                    "date": {"type": "string"},
                    "max_temperature": {"type": "number"},
                    "message": {"type": "string"},
                    "min_temperature": {"type": "number"}
                    }
                }
            }
        resp = self.app.get('/forecast')
        validate(resp.json, schema)

    @mock.patch('weather_app.utils.process_request.get_json', autospec=True)
    def test_forcast_failure(self, mock_get_json):
        mock_get_json.return_value = {'cod': '404', 'message': 'city not found'}
        resp = self.app.get('forecast')
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
