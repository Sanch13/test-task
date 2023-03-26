from django.shortcuts import render


def secondtask(request):
    return render(request, 'second/secondtask.html')
