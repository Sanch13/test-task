from django.urls import path

from .views import *

app_name = 'first'

urlpatterns = [
    path('firsttask/', firsttask, name='firsttask'),
    path('rate/<str:cur_date>/', rate, name='rate'),
]