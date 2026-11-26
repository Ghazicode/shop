from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from products.models import Product, ProductStatus
from .cart import Cart


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(
            Product,
            id=product_id,
            status=ProductStatus.ACTIVE,
        )

        cart = Cart(request)

        success = cart.add(product)

        if not success:
            messages.error(request, "موجودی محصول کافی نیست.")
        else:
            messages.success(request, "محصول به سبد خرید اضافه شد.")

        return redirect("products:cart")


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)

        return render(
            request,
            "cart/cart.html",
            {
                "cart": cart,
            },
        )


class RemoveFromCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.remove(product)

        return redirect("products:cart")
