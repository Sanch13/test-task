from django.shortcuts import render, redirect
from first.forms import DateForm
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
                return redirect("first:rate", cur_date=cur_date)
            response = get_exchange_rates(cur_date)
            RateDay(date=cur_date, data=response).save()
            return redirect("first:rate", cur_date=cur_date)

    form = DateForm()
    context = {
        'form': form
    }
    return render(request, "first/firsttask.html", context=context)


def rate(request, cur_date=''):
    cur_data = RateDay.objects.filter(date=cur_date)
    for obj in cur_data:
        context = {
            "date": obj.date,
            "data": obj.data,
        }
    return render(request, "first/firsttask/rate.html", context=context)
