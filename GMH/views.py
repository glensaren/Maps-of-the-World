# myproject/views.py

from django.shortcuts import render

# Представление для главной страницы
def home_view(request):
    return render(request, 'home.html')
