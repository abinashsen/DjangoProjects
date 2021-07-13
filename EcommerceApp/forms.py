from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Orders, Product, Customer


class OrderForm(forms.ModelForm):
    class Meta:
        model=Orders
        fields=['customer','product','status']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'mobile', 'location']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]
