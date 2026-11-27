from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from accounts.forms import AddressForm
from .models import Order, OrderItem
from cart.cart import Cart
from accounts.models import Address


class OrderDetailView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = AddressForm()
        order = get_object_or_404(Order, id = id, user = request.user)
        address = Address.objects.filter(user = request.user)
        return render(request, 'order/order_detail.html', {'form':form, 'order':order, 'address':address})



class CreateOrderView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        cart = Cart(request)

        if not cart:
            messages.error(request, 'سبد خرید شما خالی است.')
            return redirect('cart:detail')
        
        if address_id:= request.POST.get('address'):
            address = get_object_or_404(Address, id = address_id, user = request.user)
        else:
            return redirect('cart:detail')



        try:
            with transaction.atomic():
                total_price = cart.get_final_price()

                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price,
                    address = address
                )

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].title,
                        quantity=item['quantity'],
                        price=item['product'].price,
                        total_price = item['total_price'],
                        discount_percent=item['product'].discount_percent,
                    )

                cart.clear()

            messages.success(request, 'فاکتور شما با موفقیت ثبت شد.')
            return redirect('orders:detail', order.id)

        except Exception:
            messages.error(request, 'خطایی هنگام ثبت فاکتور رخ داد.')
            return redirect('cart:detail')





