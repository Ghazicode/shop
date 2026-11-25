from django.contrib import admin
from .models import Category, Product, WishList
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("id", "title", "slug")

    search_fields = ("title", "slug")

    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ("details",)

    list_display = (
        "id",
        "title",
        "category",
        "price",
        "discount_percent",
        "final_price_display",
        "stock",
        "status",
        "is_available",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "category__title",
    )

    prepopulated_fields = {"slug": ("title",)}

    list_editable = (
        "price",
        "discount_percent",
        "stock",
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 20

    @admin.display(description="قیمت نهایی")
    def final_price_display(self, obj):
        return obj.final_price


admin.site.register(WishList)
