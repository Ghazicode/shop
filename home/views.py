from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from articles.models import Article, ArticleStatus
from accounts.forms import ContactForm
from products.models import Product, ProductStatus


class HomeView(View):
    def get(self, request):
        articles = Article.objects.filter(status=ArticleStatus.PUBLISHED)[:6]
        products = Product.objects.filter(status=ProductStatus.ACTIVE)[:12]
        return render(request, "home/index.html", {"articles": articles, 'products':products})


class AboutView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "home/about.html", {"form": form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ثبت شد")
            return redirect("home:about")
        else:
            messages.error(request, "اطلاعات را به درستی وارد نمایید")
            return redirect("home:about")
