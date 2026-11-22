from django.shortcuts import render
from django.views import View
from django.contrib import messages
from articles.models import Article, ArticleStatus



class HomeView(View):
    def get(self, request):
        articles = Article.objects.filter(status = ArticleStatus.PUBLISHED)[:6]
        return render(request, 'home/index.html', {'articles':articles})
    
class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html', {})