from django.urls import path

from .views import secondtask, rate

app_name = 'second'

urlpatterns = [
    path('secondtask/', secondtask, name='secondtask'),
    path('rate/<str:cur_date>/', rate, name='rate'),
    path('rate/', rate, name='rate'),
]