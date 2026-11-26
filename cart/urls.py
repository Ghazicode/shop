from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("", views.CartDetailView.as_view(), name="detail"),
    path("add/<int:product_id>/", views.AddToCartView.as_view(), name="add"),
    path("remove/<int:product_id>/", views.RemoveFromCartView.as_view(), name="remove"),
]
