from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from . import models



class LoginForm(forms.Form):
    email = forms.EmailField(max_length=250, label='ایمیل', widget=forms.EmailInput(attrs={
            'class':'form-control',
            'id':'login-id',
            'placeholder':'ایمیل خود را وارد نمایید'
        }), validators=[MinLengthValidator(10)])


    password = forms.CharField(max_length=250, label='رمز عبور', widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'id':'login-pass',
            'placeholder':'رمز عبور خود را وارد نمایید'
        }), validators=[MinLengthValidator(8)])



    

class RegisterForm(forms.Form):
    fullname = forms.CharField(max_length=250, label='نام و نام خانوادگی', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'rag-name',
            'placeholder':'نام و نام خانوادگی خود را وارد نمایید'
            
        }
    ), validators=[MinLengthValidator(5)])
    email = forms.EmailField(max_length=250, label='ایمیل', widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'id':'reg-email',
            'placeholder':'ایمیل خود را وارد نمایید'
        }
    ), validators=[MinLengthValidator(10)]) # 10 == @gmail.com


    phone_number = forms.CharField(max_length=11, label='شماره تلفن', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'rag-mobile',
            'inputmode':'numeric',
            'placeholder':'شماره تلفن خود را وارد نمایید'
            
        }
    ), validators=[MinLengthValidator(11), MaxLengthValidator(11)])

    password1 = forms.CharField(max_length=250, label='رمز عبور', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'reg-pass',
            'placeholder':'رمز عبور خود را وارد نمایید'
        }
    ), validators=[MinLengthValidator(8)])


    password2 = forms.CharField(max_length=250, label='تکرار رمز عبور', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'reg-pass',
            'placeholder':'تکرار رمز عبور خود را وارد نمایید'
        }
    ), validators=[MinLengthValidator(8)])


    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password1", "رمزها با یکدیگر مطابقت ندارند")

        return cleaned_data
    


    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]

        regex = r'^(?:\+98|0)?9\d{9}$'

        if not re.match(regex, phone_number):
            raise ValidationError("شماره موبایل نامعتبر می‌باشد")

        return phone_number
    





class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        exclude = ('status', 'created_at', 'updated_at')
        widgets={
            'fullname':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'ct-fullname',
                    'placeholder':'نام و نام خانوادگی خود را وارد نمایید'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'id':'ct-email',
                    'placeholder':'ایمیل خود را وارد نمایید'
                }
            ),
            'subject':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'ct-subject',
                    'placeholder':'موضوع پیام خود را وارد نمایید'
                }
            ),
            'message':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'ct-text',
                    'placeholder':'پیام خود را بنویسید',
                    'rows':5
                }
            ),
        }