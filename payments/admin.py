from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "amount",
        "status",
        "authority",
        "ref_id",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "authority",
        "ref_id",
        "order__id",
        "order__user__email",
    )

    readonly_fields = (
        "authority",
        "ref_id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
