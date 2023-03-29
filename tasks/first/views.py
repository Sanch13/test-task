from django.http.response import JsonResponse
from django.shortcuts import render

from first.forms import DateForm
from first.models import RatesDay
from logs.settings import logger_1
from services.middleware import get_exchange_rates_on_date, display_error_in_json, \
    check_record_exists_by_date, get_body_and_headers_on_date


def index(request):
    return render(request, 'first/base.html')


def first_task(request):
    date = request.GET.get("date")

    if check_record_exists_by_date(date=date):
        logger_1.info(f"This instance is in the database. Display from the database")
        response_body, headers = get_body_and_headers_on_date(date=date)
        return JsonResponse(response_body, headers=headers)

    response = get_exchange_rates_on_date(date=date)

    try:
        RatesDay(date=date, data=response).save()
        logger_1.success("Saved in the DB")
    except Exception as error:
        logger_1.error(f"Could not save in the DataBase: {error}")
        response_body = display_error_in_json()
        return JsonResponse(response_body)

    response_body, headers = get_body_and_headers_on_date(date=date)
    return JsonResponse(response_body, headers=headers)


def first_task_doc(request):
    form = DateForm()
    context = {
        'form': form
    }
    return render(request, 'first/firsttaskdoc.html', context=context)
