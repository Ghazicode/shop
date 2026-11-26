from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("", views.CartDetailView.as_view(), name="detail"),
    path("add/<slug:slug>/", views.AddToCartView.as_view(), name="add"),
    path("remove/<slug:slug>/", views.RemoveFromCartView.as_view(), name="remove"),
    path('increase/<slug:slug>/', views.IncreaseCartView.as_view(), name='increase'),
    path('decrease/<slug:slug>/', views.DecreaseCartView.as_view(), name='decrease'),
]
