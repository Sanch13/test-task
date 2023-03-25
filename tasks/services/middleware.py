import requests
from first.models import RateDay


def get_exchange_rates(date: str) -> list:
    """Return the list of rate for date"""
    url = "https://www.nbrb.by/api/exrates/rates"
    params = {
        "ondate": date,
        "periodicity": 0
    }

    return requests.get(url, params=params).json()


def check_record_exists_by_date(date: str) -> bool:
    """Return true if the record exists"""
    return RateDay.objects.filter(date=date).exists()
