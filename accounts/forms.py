from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Телефон', max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'phone', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'birth_date', 'avatar', 'driver_license_number',
                  'driver_license_issued')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'driver_license_issued': forms.DateInput(attrs={'type': 'date'}),
        }


class TopUpForm(forms.Form):
    amount = forms.DecimalField(
        label='Сумма пополнения, ₽',
        min_value=100, max_value=50000, decimal_places=2,
    )
