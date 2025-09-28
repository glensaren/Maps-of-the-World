# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Представление для регистрации
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создаём нового пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()
            login(request, user)  # Выполняем вход
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


# Представление для логина
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['login']  # email или username
            password = form.cleaned_data['password']

            # Попробуем найти пользователя по email
            try:
                user_obj = User.objects.get(email=login_input)
                username = user_obj.username
            except User.DoesNotExist:
                username = login_input  # возможно, это username напрямую

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Неверный email/имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user  # Получаем текущего пользователя
    return render(request, 'profile.html', {'user': user})

