from datetime import date, timedelta
import requests
from first.models import RatesDay
from logs.settings import logger_1, logger_2
from second.models import RateDay


def get_exchange_rates_on_date(day: str) -> list:
    """Return the list of rate for date"""
    url = "https://www.nbrb.by/api/exrates/rates"
    params = {
        "ondate": day,
        "periodicity": 0
    }

    try:
        logger_1.info(f"Запрос по API в банк на {params.get('ondate')}")
        response = requests.get(url=url, params=params)
        if response.status_code == 200 and len(response.json()) >= 0:
            logger_1.success(f"Запрос по API в банк на {params.get('ondate')} произошел успешно")
            return response.json()
    except Exception as error:
        logger_1.error(f"Не смог получить данные, ошибка: ", error)
        # что тут делать дальше?


def get_currency_rate_on_date(day: str, cur_id: str) -> tuple:
    """Return currency rate on date"""
    url = "https://www.nbrb.by/api/exrates/rates/" + cur_id
    params = {
        "ondate": day,
    }

    try:
        logger_2.info(f"Запрос по API в банк на {params.get('ondate')}")
        response = requests.get(url=url, params=params)

        if response.status_code == 200:
            logger_2.success(f"Запрос по API в банк на {params.get('ondate')} произошел успешно ")
            return response.json()

    except Exception as error:
        logger_2.error(f"Не смог получить данные, ошибка: ", error)
        # что тут делать дальше?


def get_list_name_currencies() -> list:
    """Return the list of all names currencies"""
    url = "https://www.nbrb.by/api/exrates/rates"
    params = {
        "ondate": date.today().strftime('%Y-%m-%d'),
        "periodicity": 0
    }

    currencies = []
    try:
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            data = response.json()
            for obj in data:
                currencies.append((f"{obj.get('Cur_ID')}", f"{obj.get('Cur_Scale')} "
                                                           f"{obj.get('Cur_Name')} "
                                                           f"{obj.get('Cur_Abbreviation')}"))
            logger_2.success(f"Получил список валют")
            return currencies

    except Exception as error:
        print(f"Не смог получить список валют, ошибка: ", error)
        # что тут делать дальше?


def get_yesterday_date(day: date) -> str:
    """Return yesterday date by string"""
    yesterday = day - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    return yesterday


def check_record_exists_by_date(day: str) -> bool:
    """Return true if the record exists"""
    return RatesDay.objects.filter(date=day).exists()


def check_record_exists_by_date_cur_id(day: str, cur_id: int) -> bool:
    """Return true if the record exists"""
    return RateDay.objects.filter(date=day, cur_id=cur_id).exists()


def compare_currency_rate(cur_date: date, cur_id: int, cur_rate: float) -> str:
    """Return str. Comparing courses yesterday and today """
    url = "https://www.nbrb.by/api/exrates/rates/" + str(cur_id)
    params = {
        "ondate": get_yesterday_date(cur_date),
    }
    yesterday_response = requests.get(url=url, params=params)
    try:
        if yesterday_response.status_code == 200:
            logger_2.success(f"Запрос по API в банк на {params.get('ondate')} произошел успешно ")
            yesterday_rate = yesterday_response.json().get('Cur_OfficialRate')
            if yesterday_rate > cur_rate:
                return f"Курс снизился был {yesterday_rate}, а стал {cur_rate}"
            elif yesterday_rate < cur_rate:
                return f"Курс увеличился был {yesterday_rate}, а стал {cur_rate}"
            return f"Курс остался прежним"
    except Exception as error:
        logger_2.error(f"Не смог получить данные, ошибка: ", error)
        # что тут делать дальше???
