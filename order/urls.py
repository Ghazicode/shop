from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("<int:id>/", views.OrderDetailView.as_view(), name="detail"),
    path("create/", views.CreateOrderView.as_view(), name="create"),
]
