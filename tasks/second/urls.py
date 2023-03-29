from django.urls import path

from .views import second_task, second_task_doc

app_name = 'second'

urlpatterns = [
    path('secondtask', second_task, name='secondtask'),
    path('secondtaskdoc/', second_task_doc, name='secondtaskdoc'),
]