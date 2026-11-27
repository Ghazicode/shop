from django import template
from order.models import OrderItem

register = template.Library()


@register.simple_tag
def get_order_totals(order_id):
    items = OrderItem.objects.filter(order_id=order_id)

    total_price = 0
    total_discount = 0

    for item in items:
        price = item.price * item.quantity
        discount = price * item.discount_percent // 100

        total_price += price
        total_discount += discount

    return {
        "total_price": total_price,
        "total_discount": total_discount,
    }
