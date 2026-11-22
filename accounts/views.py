from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile
from django.db import transaction
User = get_user_model()



class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:index')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form':form})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home:index')
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd["email"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('home:index')
            messages.warning(request, 'کاربر یافت نشد')
            return redirect('accounts:login')
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('accounts:login')






class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:index')

        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home:index')

        form = RegisterForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if User.objects.filter(email=cd['email']).exists():
                messages.warning(request, 'ایمیل از قبل وجود دارد')
                return render(request, 'accounts/register.html', {'form': form})


            try:
                with transaction.atomic():

                    user = User.objects.create_user(
                        email=cd['email'],
                        password=cd['password1']
                    )

                    profile = Profile.objects.get(user=user)

                    profile.fullname = cd['fullname']
                    profile.phone_number = cd['phone_number']
                    profile.save()



                messages.success(request, 'ثبت نام با موفقیت انجام شد')

                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, 'خطایی هنگام ثبت نام رخ داد')
        return render(request, 'accounts/register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'با موفقیت خارج شدید')
            return redirect('accounts:login')
