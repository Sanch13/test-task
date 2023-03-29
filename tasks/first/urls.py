from django.urls import path

from .views import *

app_name = 'first'

urlpatterns = [
    path('firsttask', first_task, name='firsttask'),
    path('firsttaskdoc/', first_task_doc, name='firsttaskdoc'),
]