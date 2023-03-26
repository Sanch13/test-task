from django.urls import path

from .views import firsttask, rate, nodata

app_name = 'first'

urlpatterns = [
    path('firsttask/', firsttask, name='firsttask'),
    path('rate/<str:cur_date>/', rate, name='rate'),
    path('nodata/<str:cur_date>/', nodata, name='nodata'),
]