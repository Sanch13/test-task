from django.urls import path

from .views import secondtask

app_name = 'second'

urlpatterns = [
    path('secondtask/', secondtask, name='secondtask'),
    # path('rate/<str:cur_date>/', rate, name='rate'),
    # path('nodata/<str:cur_date>/', nodata, name='nodata'),
]