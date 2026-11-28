from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels
from django.core.validators import MaxValueValidator
from products.models import Product
from accounts.models import Address

User = get_user_model()


class PaymentStatus(models.TextChoices):
    PAID = "paid", "پرداخت شده"
    PENDING = "pending", "در انتظار پرداخت"
    CANCELLED = "cancelled", "لغو شده"
    DELIVERED = "delivered", "تحویل داده شده"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="orders"
    )

    is_paid = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    total_price = models.PositiveBigIntegerField(default=0)

    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="order_items"
    )

    product_name = models.CharField(max_length=255)

    quantity = models.PositiveIntegerField(default=1)

    price = models.PositiveBigIntegerField(default=0)

    total_price = models.PositiveBigIntegerField(default=0)

    discount_percent = models.PositiveSmallIntegerField(
        null=True, blank=True, default=0, validators=[MaxValueValidator(100)]
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    @property
    def discount_amount(self):
        return self.subtotal * (self.discount_percent or 0) // 100

    @property
    def final_price(self):
        return self.subtotal - self.discount_amount

    def save(self, *args, **kwargs):
        self.total_price = self.final_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
