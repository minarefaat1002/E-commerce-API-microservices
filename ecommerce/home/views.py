from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from .tasks import count_task

def home_view(request):
    return render(request,'home.html')


def count_to_10(request):
    count_task.delay()
    return redirect('home')