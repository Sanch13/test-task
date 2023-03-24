from django.urls import path

from .views import *

app_name = 'first'

urlpatterns = [
    path('', index, name='index'),

]