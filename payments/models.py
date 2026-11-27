from django.db import models
from django.db.models import Q
from order.models import Order


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        SUCCESS = "success", "پرداخت موفق"
        FAILED = "failed", "پرداخت ناموفق"

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")

    authority = models.CharField(max_length=255, unique=True, null=True, blank=True)

    amount = models.PositiveBigIntegerField()

    ref_id = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["order"],
                condition=Q(status="pending"),
                name="unique_pending_payment_per_order",
            )
        ]

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order_id}"
