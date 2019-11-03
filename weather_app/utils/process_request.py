import requests
from retry import retry
from requests import HTTPError
from weather_app import app

logger = app.logger


@retry(HTTPError, tries=5, delay=4)
def get(url):
    logger.info('--> start of process_request.get()')
    logger.info('loading url')
    resp = requests.get(url)
    resp.raise_for_status()
    logger.info('Successfully loaded URL')
    logger.info('<-- end of process_request.get()')
    return resp


def get_json(url):
    logger.info('--> start of process_request.get_json()')
    data = get(url).json()
    logger.info('--> start of process_request.get_json()')
    return data
