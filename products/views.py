from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, ProductStatus, Category, WishList
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages


class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(status=ProductStatus.ACTIVE)
        cats = Category.objects.all()
        if q := request.GET.get("q"):
            products = products.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        if category := request.GET.get("category"):
            category = get_object_or_404(Category, slug=category)
            products = products.filter(category=category)
        products = Paginator(products, 9)

        try:
            page_number = request.GET.get("page")
            products = products.get_page(page_number)
        except PageNotAnInteger:
            products = products.get_page(1)
        except EmptyPage:
            products = products.get_page(1)
        return render(
            request, "products/product_list.html", {"products": products, "cats": cats}
        )


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, status=ProductStatus.ACTIVE)
        products = Product.objects.filter(status=ProductStatus.ACTIVE).exclude(
            slug=slug
        )[:4]
        if request.user.is_authenticated:

            product.is_wishlisted = product.wishlist.filter(user=request.user).exists()
            for item in products:
                item.is_wishlisted = item.wishlist.filter(user=request.user).exists()
        return render(
            request,
            "products/product_detail.html",
            {"product": product, "products": products},
        )


class WishListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        wishlist = WishList.objects.filter(
            user=request.user
        ).select_related("product")

        return render(
            request,
            "products/wishlist.html",
            {"wishlist": wishlist}
        )


class CreateWishListView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        slug = request.POST.get("product")

        if not slug:
            messages.error(request, "محصول یافت نشد")
            return redirect("products:list")

        product = get_object_or_404(
            Product,
            slug=slug,
            status=ProductStatus.ACTIVE
        )

        wishlist, created = WishList.objects.get_or_create(
            user=request.user,
            product=product
        )

        if created:
            messages.success(
                request,
                "محصول با موفقیت به لیست علاقه‌مندی‌ها اضافه شد"
            )
        else:
            messages.error(
                request,
                "محصول قبلاً به لیست علاقه‌مندی‌ها اضافه شده است"
            )

        return redirect("products:wishlist")


class DeleteWishListView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        slug = request.POST.get("product")

        if not slug:
            messages.error(request, "محصول یافت نشد")
            return redirect("products:list")

        product = get_object_or_404(
            Product,
            slug=slug,
            status=ProductStatus.ACTIVE
        )

        deleted_count, _ = WishList.objects.filter(
            user=request.user,
            product=product
        ).delete()

        if deleted_count:
            messages.success(
                request,
                "محصول با موفقیت از لیست علاقه‌مندی‌ها حذف شد"
            )
        else:
            messages.error(
                request,
                "محصول داخل لیست علاقه‌مندی‌ها نیست"
            )

        return redirect("products:wishlist")
