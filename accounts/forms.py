from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator



class LoginForm(forms.Form):
    email = forms.CharField(max_length=250, label='ایمیل', widget=forms.EmailInput(attrs={
            'class':'form-control',
            'id':'login-id',
            'placeholder':'ایمیل خود را وارد نمایید'
        }), validators=[MinLengthValidator(10)])


    password = forms.CharField(max_length=250, label='رمز عبور', widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'id':'login-pass',
            'placeholder':'رمز عبور خود را وارد نمایید'
        }), validators=[MinLengthValidator(8)])



    