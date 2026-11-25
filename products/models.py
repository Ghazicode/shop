from django.db import models
from django.core.validators import MaxValueValidator
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductStatus(models.TextChoices):
    ACTIVE = "active", "فعال"
    INACTIVE = "inactive", "غیرفعال"


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [
            "-id",
        ]


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, allow_unicode=True)

    description = models.TextField()
    details = models.TextField()

    price = models.PositiveBigIntegerField()

    discount_percent = models.PositiveSmallIntegerField(
        # DecimalField example: 99.9
        null=True,
        blank=True,
        validators=[MaxValueValidator(100)],
    )

    stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=10, choices=ProductStatus.choices, default=ProductStatus.ACTIVE
    )

    image = models.ImageField(upload_to="products/")

    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.stock > 0

    def calculate_discount(self):
        if self.discount_percent:
            return self.price * self.discount_percent // 100

        return 0

    @property
    def final_price(self):
        return self.price - self.calculate_discount()

    def get_summary(self):
        return f"{self.description[:30]}..."


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlist"
    )

    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_wishlist"
            )
        ]
        ordering = ['-id']

    def __str__(self):
        return self.product.title
