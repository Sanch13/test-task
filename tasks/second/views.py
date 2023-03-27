from django.shortcuts import render, redirect

from logs.settings import logger_2
from second.forms import DateRateForm
from second.models import RateDay
from services.middleware import get_currency_rate_on_date, compare_currency_rate, \
    check_record_exists_by_date_cur_id


def secondtask(request):
    if request.method == 'POST':
        form = DateRateForm(data=request.POST)

        if form.is_valid():
            cur_date = form.cleaned_data['date'].strftime('%Y-%m-%d')
            cur_id = form.cleaned_data['cur_id']

            if check_record_exists_by_date_cur_id(day=cur_date, cur_id=cur_id):
                logger_2.info(f"Данная запись есть в БД. Отображу из БД")
                return redirect("second:rate", cur_date=cur_date)

            response = get_currency_rate_on_date(cur_date, cur_id)

            if not response:
                logger_2.warning(f"Нет данных о курсах валют")
                return redirect("first:nodata", cur_date=cur_date)

            try:
                RateDay(date=cur_date, cur_id=cur_id, data=response).save()
                logger_2.success(f"Успешная запись в БД")
                return redirect("second:rate", cur_date=cur_date)
            except Exception as error:
                logger_2.error(f"Не смог записать  в БД", error)  # что тут делать?

    form = DateRateForm()
    context = {
        'form': form
    }
    return render(request, 'second/secondtask.html', context=context)


def rate(request, cur_date=''):  # как тут лучше поступить с cur_date=''?
    cur_data = RateDay.objects.filter(date=cur_date)
    for obj in cur_data:
        context = {
            "date": obj.date,
            "data": obj.data,
            "different_rate": compare_currency_rate(cur_date=obj.date,
                                                    cur_id=obj.data.get("Cur_ID"),
                                                    cur_rate=obj.data.get("Cur_OfficialRate"))
        }
    return render(request, "second/secondtask/rate.html", context=context)

