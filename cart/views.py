from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from products.models import Product, ProductStatus
from .cart import Cart
from accounts.models import Address


class AddToCartView(View):
    def post(self, request, slug):
        product = get_object_or_404(
            Product,
            slug=slug,
            status=ProductStatus.ACTIVE,
        )

        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            quantity = 1

        cart = Cart(request)
        success = cart.add(product, quantity=quantity)

        if not success:
            messages.error(request, "موجودی محصول کافی نیست.")
        else:
            messages.success(request, "محصول به سبد خرید اضافه شد.")

        return redirect("cart:detail")


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        context = {'cart':cart}
        if request.user.is_authenticated:
            address = Address.objects.filter(user = request.user)
            context['address'] = address

        return render(request, "cart/cart.html", context)


class RemoveFromCartView(View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        cart = Cart(request)
        cart.remove(product)

        return redirect("cart:detail")


class IncreaseCartView(View):
    def post(self, request, slug):
        product = get_object_or_404(
            Product,
            slug=slug,
            status=ProductStatus.ACTIVE,
        )

        cart = Cart(request)

        success = cart.add(product, quantity=1)

        if not success:
            messages.error(request, "موجودی محصول کافی نیست.")
        else:
            messages.success(request, "تعداد محصول افزایش یافت.")

        return redirect("cart:detail")


class DecreaseCartView(View):
    def post(self, request, slug):
        product = get_object_or_404(
            Product,
            slug=slug,
            status=ProductStatus.ACTIVE,
        )

        cart = Cart(request)

        cart.add(product, quantity=-1)

        messages.success(request, "تعداد محصول کاهش یافت.")

        return redirect("cart:detail")
