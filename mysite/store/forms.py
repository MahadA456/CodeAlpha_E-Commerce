from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Order
from django import forms

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[('cash', 'Cash'), ('easypaisa', 'Easypaisa')])
    easypaisa_number = forms.CharField(required=False, max_length=15)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'city', 'state', 'postal_code', 'country']
