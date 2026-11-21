from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages



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
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form':form})
    

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'با موفقیت خارج شدید')
            return redirect('accounts:login')
