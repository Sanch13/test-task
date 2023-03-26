from datetime import date, timedelta
import requests
from first.models import RateDay
from logs.settings import logger_1


def get_exchange_rates(date: str) -> list:
    """Return the list of rate for date"""
    url = "https://www.nbrb.by/api/exrates/rates"
    params = {
        "ondate": date,
        "periodicity": 0
    }

    try:
        logger_1.info(f"Запрос по API в банк на {params.get('ondate')}")
        response = requests.get(url, params=params)
        if response.status_code == 200 and len(response.json()) >= 0:
            logger_1.success(f"Запрос по API в банк на {params.get('ondate')} произошел успешно")
            return response.json()
    except Exception as error:
        logger_1.error(f"Не смог получить данные, ошибка: ", error)
        # что тут делать дальше?


def get_list_name_currencies_yesterday(today=date.today()) -> list:
    """Return the list of all names currencies yesterday"""
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    url = "https://www.nbrb.by/api/exrates/rates"
    params = {
        "ondate": yesterday,
        "periodicity": 0
    }

    courses = []
    # courses => [{'name': '1 Австралийский доллар AUD'}, {'name': '1000 Армянских драмовAMD'}, ...]
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200 and len(response.json()) > 0:
            data = response.json()
            for obj in data:
                courses.append({"name": f"{obj.get('Cur_Scale')} "
                                        f"{obj.get('Cur_Name')} "
                                        f"{obj.get('Cur_Abbreviation')}"})
            return courses

    except Exception as error:
        print(f"Не смог получить данные, ошибка: ", error)


def check_record_exists_by_date(date: str) -> bool:
    """Return true if the record exists"""
    return RateDay.objects.filter(date=date).exists()
