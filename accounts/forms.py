from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Форма для регистрации
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label = 'Имя',
        min_length = 4,
        widget=forms.TextInput(attrs= { 'placeholder' : 'Введите имя', 'minlength' : '4' })
    )

    email = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес электронной почты'}))


    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'type' : 'password' , 'placeholder' : 'Придумайте пароль'}))

    privacy_policy = forms.BooleanField(required=True, label="Я согласен с политикой конфиденциальности")

    class Meta:
        model = User
        fields = ['username', 'email']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже занят.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Имя пользователя уже занято.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


# Форма для логина
class LoginForm(forms.Form):
    login = forms.CharField(
        label="Email или имя пользователя",
        widget=forms.TextInput(attrs={'placeholder': 'Введите email или имя пользователя'})
    )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    auto_login = forms.BooleanField(required=False, label="Выполнять вход автоматически")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Проверяем, существует ли пользователь с таким email
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email не найден.")
        return email



