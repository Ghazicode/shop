from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.UserPanelView.as_view(), name="user"),
    path("order/list/", views.OrderListView.as_view(), name="order_list"),
    path("comment/list/", views.UserCommentListView.as_view(), name="comment_list"),
    path("wishlist/", views.WishListView.as_view(), name="wishlist"),
    path("profile/update/", views.UserUpdateProfileView.as_view(), name="user_update"),
    path("change/password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("add/address/", views.AddressView.as_view(), name="add_address"),
]
