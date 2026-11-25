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
        return render(
            request,
            "products/product_detail.html",
            {"product": product, "products": products},
        )


class WishListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        wishlist = WishList.objects.filter(user=request.user)
        return render(request, "products/wishlist.html", {"wishlist": wishlist})


class CreateWishListView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if slug := request.POST.get("product"):
            product = get_object_or_404(Product, slug=slug, status=ProductStatus.ACTIVE)
            if WishList.objects.filter(product=product, user=request.user).exists():
                messages.error(request, "محصول قبلا به لیست اضافه شده")
                return redirect("products:wishlist")
            WishList.objects.create(user=request.user, product=product)
            messages.success(request, "محصول با موفقیت به لیست علاقه مندی ها اضافه شد")
            return redirect("products:wishlist")
        else:
            messages.error(request, "محصول یافت نشد")
            return redirect("product:list")


class DeleteWishListView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if slug := request.POST.get("product"):
            product = get_object_or_404(Product, slug=slug, status=ProductStatus.ACTIVE)
            if WishList.objects.filter(product=product, user=request.user).exists():
                item = get_object_or_404(WishList, user=request.user, product=product)
                if item:
                    item.delete()
                    messages.success(
                        request, "محصول با موفقیت از لیست علاقه مندی ها حذف شد"
                    )
                return redirect("products:wishlist")
            else:
                messages.error(request, "محصول داخل لیست علاقه مندی ها نیست")
                return redirect("products:wishlist")
        else:
            messages.error(request, "محصول یافت نشد")
            return redirect("product:list")
