from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.UserPanelView.as_view(), name="user"),
    path("profile/update/", views.UserUpdateProfileView.as_view(), name="user_update"),
    path("change/password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("add/address/", views.AddressView.as_view(), name="add_address"),
]
