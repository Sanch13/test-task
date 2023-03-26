from django.shortcuts import render, redirect
from first.forms import DateForm
from logs.settings import logger_1
from first.models import RateDay
from services.middleware import check_record_exists_by_date, get_exchange_rates


def index(request):
    return render(request, 'first/base.html')


def firsttask(request):
    if request.method == 'POST':
        form = DateForm(data=request.POST)

        if form.is_valid():
            cur_date = form.cleaned_data['date'].strftime('%Y-%m-%d')

            if check_record_exists_by_date(cur_date):
                logger_1.info(f"Данная запись есть в БД. Отображу из БД")
                return redirect("first:rate", cur_date=cur_date)

            response = get_exchange_rates(cur_date)
            if len(response) == 0:
                logger_1.warning(f"Нет данных о курсах валют")
                return redirect("first:nodata", cur_date=cur_date)

            try:
                RateDay(date=cur_date, data=response).save()
                logger_1.success(f"Успешная запись в БД")
                return redirect("first:rate", cur_date=cur_date)
            except Exception as error:
                logger_1.error(f"Не смог записать  в БД", error)  # что тут делать?

    form = DateForm()
    context = {
        'form': form
    }
    return render(request, "first/firsttask.html", context=context)


def rate(request, cur_date=''):  # как тут лучше поступить с cur_date=''?
    cur_data = RateDay.objects.filter(date=cur_date)
    for obj in cur_data:
        context = {
            "date": obj.date,
            "data": obj.data,
        }
    return render(request, "first/firsttask/rate.html", context=context)


def nodata(request, cur_date=''):  # как тут лучше поступить с cur_date=''?
    context = {
        "date": cur_date
    }
    return render(request, "first/firsttask/nodata.html", context=context)
