from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = ("total_price",)

    fields = (
        "product",
        "product_name",
        "quantity",
        "price",
        "discount_percent",
        "total_price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "is_paid",
        "total_price",
        "created_at",
    )

    list_filter = (
        "is_paid",
        "created_at",
    )

    search_fields = ("user__email",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = (OrderItemInline,)

    list_per_page = 25


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "order",
        "quantity",
        "price",
        "discount_percent",
        "total_price",
    )

    list_filter = ("discount_percent",)

    search_fields = (
        "product_name",
        "order__user__email",
    )

    list_per_page = 25
