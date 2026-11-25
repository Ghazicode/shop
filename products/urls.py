from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("list/", views.ProductListView.as_view(), name="list"),
    path("<slug:slug>/detail/", views.ProductDetailView.as_view(), name="detail"),
    path("wishlist/", views.WishListView.as_view(), name="wishlist"),
    path("wishlist/create/", views.CreateWishListView.as_view(), name="add_wishlist"),
    path(
        "wishlist/delete/", views.DeleteWishListView.as_view(), name="delete_wishlist"
    ),
]
