from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("start/<int:order_id>/", views.StartPaymentView.as_view(), name="start"),
    path("verify/", views.VerifyPaymentView.as_view(), name="verify"),
]
