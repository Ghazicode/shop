from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile
from django.db import transaction
from .forms import AddressForm, UserProfileForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
User = get_user_model()


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:index")
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("home:index")
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd["email"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید")
                return redirect("home:index")
            else:
                messages.warning(request, "کاربر یافت نشد")
            return redirect("accounts:login")
        else:
            messages.error(request, "اطلاعات وارد شده صحیح نمیباشد")
            return redirect("accounts:login")


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:index")

        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("home:index")

        form = RegisterForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if User.objects.filter(email=cd["email"]).exists():
                messages.warning(request, "ایمیل از قبل وجود دارد")
                return render(request, "accounts/register.html", {"form": form})

            try:
                with transaction.atomic():

                    user = User.objects.create_user(
                        email=cd["email"], password=cd["password1"]
                    )

                    profile = Profile.objects.get(user=user)

                    profile.fullname = cd["fullname"]
                    profile.phone_number = cd["phone_number"]
                    profile.save()

                messages.success(request, "ثبت نام با موفقیت انجام شد")

                return redirect("accounts:login")
            except Exception as e:
                messages.error(request, "خطایی هنگام ثبت نام رخ داد")
        return render(request, "accounts/register.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "با موفقیت خارج شدید")
            return redirect("accounts:login")


class AddressView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "قبل از ثبت ادرس باید وارد شوید")
            return redirect("accounts:login")
        form = AddressForm()
        return render(request, "accounts/add_address.html", {"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "قبل از ثبت ادرس باید وارد شوید")
            return redirect("accounts:login")
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "ادرس با موفقیت ثبت شد")
            return redirect("cart:detail")
        else:
            messages.error(request, "اطلاعات را به درستی وارد نمایید")
            return redirect("accounts:add_address")


class UserPanelView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        return render(request, 'accounts/user/index.html', {})
    

class UserUpdateProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = UserProfileForm(instance = request.user.user_profile)
        return render(request, 'accounts/user/update.html', {'form':form})
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = UserProfileForm(instance=request.user.user_profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل شما با موفقیت بروزرسانی شد')
            return redirect('accounts:user')
        else:
            messages.error(request, 'اطلاعات را به درستی وارد نمایید')
            return redirect('accounts:user_update')
        




class ChangePasswordView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/user/change_password.html', {'form':form})
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'اطلاعات را به درستی وارد نمایید')
            return redirect('accounts:change_password')


            

        