from django.http import JsonResponse
from django.shortcuts import render

from logs.settings import logger_2
from second.forms import DateRateForm
from second.models import RateDay
from services.middleware import get_currency_rate_on_date, display_error_in_json, \
    check_record_exists_by_date_cur_id, get_body_and_headers_on_date_cur_id


def second_task(request):
    date = request.GET.get("date")
    uid = request.GET.get("uid")

    if check_record_exists_by_date_cur_id(date=date, uid=uid):
        logger_2.info(f"This instance is in the database. Display from the database")
        response_body, headers = get_body_and_headers_on_date_cur_id(date=date, uid=uid)
        return JsonResponse(response_body, headers=headers)

    response = get_currency_rate_on_date(date=date, uid=uid)

    try:
        RateDay(date=date, cur_id=uid, data=response).save()
        logger_2.success("Saved in the DB")
    except Exception as error:
        logger_2.error(f"Could not save in the DataBase: {error}")
        response_body = display_error_in_json()
        return JsonResponse(response_body)

    response_body, headers = get_body_and_headers_on_date_cur_id(date=date, uid=uid)
    return JsonResponse(response_body, headers=headers)


def second_task_doc(request):
    form = DateRateForm()
    context = {
        "form": form
    }
    return render(request, "second/secondtaskdoc.html", context=context)
