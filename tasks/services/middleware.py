import json
import zlib
from datetime import date, timedelta

import requests

from first.models import RatesDay
from logs.settings import logger_1, logger_2
from second.models import RateDay

URL_API_BANK = "https://www.nbrb.by/api/exrates/rates/"


def get_exchange_rates_on_date(date: str) -> dict:
    """Return the list of rate for date"""
    url = URL_API_BANK
    params = {
        "ondate": date,
        "periodicity": 0
    }
    try:
        logger_1.info("API request to bank")
        response = requests.get(url=url, params=params)
        if response.status_code == 200 and len(response.json()) >= 0:
            logger_1.success("API request to bank completed successfully")
            return response.json()

    except Exception as error:
        logger_1.error(f"Could not get the data, error: {error}")
        # что тут делать дальше?


def get_currency_rate_on_date(date: str, uid: str) -> dict:
    """Return currency rate on date"""
    url = URL_API_BANK + uid
    params = {
        "ondate": date,
    }
    try:
        logger_2.info("API request to bank")
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            logger_2.success("API request to bank completed successfully")
            return response.json()

    except Exception as error:
        logger_2.error(f"Could not get the data, error: {error}")
        # что тут делать дальше?


def get_list_name_currencies() -> list:
    """Return the list of all names currencies"""
    url = URL_API_BANK
    params = {
        "ondate": date.today().strftime('%Y-%m-%d'),
        "periodicity": 0
    }
    # list_currencies = []
    try:
        logger_2.info("API request to bank for the list of all names currencies")
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            data = response.json()
            list_currencies = [(f"{obj.get('Cur_ID')}",
                                f"{obj.get('Cur_Scale')} "
                                f"{obj.get('Cur_Name')}"
                                f"{obj.get('Cur_Abbreviation')}") for obj in data]
            # for obj in data:
            #     list_currencies.append((f"{obj.get('Cur_ID')}", f"{obj.get('Cur_Scale')} "
            #                                                     f"{obj.get('Cur_Name')} "
            #                                                     f"{obj.get('Cur_Abbreviation')}"))

            logger_2.success(f"I have got the list currencies")
            return list_currencies

    except Exception as error:
        logger_2.error(f"Could not get the list of all names currencies, error: {error}")
        # что тут делать дальше?


def compare_currency_rate(cur_date: date, cur_id: int, cur_rate: float) -> str:
    """Return str. Comparing courses yesterday and today """
    url = URL_API_BANK + str(cur_id)
    params = {
        "ondate": get_yesterday_date(cur_date),
    }
    try:
        logger_2.info("API request to bank")
        yesterday_response = requests.get(url=url, params=params)
        if yesterday_response.status_code == 200:
            logger_2.success("API request to bank completed successfully")
            yesterday_rate = yesterday_response.json().get('Cur_OfficialRate')
            if yesterday_rate > cur_rate:
                return f"Курс снизился был {yesterday_rate}, а стал {cur_rate}"
            elif yesterday_rate < cur_rate:
                return f"Курс увеличился был {yesterday_rate}, а стал {cur_rate}"
            return f"Курс остался прежним"

    except Exception as error:
        logger_2.error(f"Could not get the data, error: {error}")
        # что тут делать дальше???


def get_body_and_headers_on_date(date: str):
    """Return response_body, headers objects"""
    cur_data = RatesDay.objects.get(date=date)
    response_body = {
        'status': 'success',
        'message': f"Currency rates for {date} loaded successfully and saved in the database",
        'data': cur_data.data
    }
    headers = get_crc32_from_body(response_body)
    return response_body, headers


def get_body_and_headers_on_date_cur_id(date: str, uid: str):
    """Return response_body, headers objects"""
    cur_data = RateDay.objects.get(date=date, cur_id=uid)
    response_body = {
        'status': 'success',
        'message': f"Currency rate for {date} loaded successfully and saved in the database",
        'data': cur_data.data,
        'Has rate change?': compare_currency_rate(cur_date=cur_data.date,
                                                  cur_id=cur_data.data.get("Cur_ID"),
                                                  cur_rate=cur_data.data.get(
                                                      "Cur_OfficialRate")),
    }
    headers = get_crc32_from_body(response_body)
    return response_body, headers


def get_crc32_from_body(response_body):
    crc = str(zlib.crc32(json.dumps(response_body).encode('utf-8')))
    headers = {"CRC": crc}
    return headers


def display_error_in_json():
    """Display error JSON format"""
    response_body = {
        'status': 'error',
        'message': "Error occurred while saving in the database"
    }
    return response_body


def get_yesterday_date(day: date) -> str:
    """Return yesterday date by string"""
    yesterday = day - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    return yesterday


def check_record_exists_by_date(date: str) -> bool:
    """Return true if the record exists"""
    return RatesDay.objects.filter(date=date).exists()


def check_record_exists_by_date_cur_id(date: str, uid: str) -> bool:
    """Return true if the record exists"""
    return RateDay.objects.filter(date=date, cur_id=uid).exists()
