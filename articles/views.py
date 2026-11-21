from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Article, Tag, Category, Comment, ArticleStatus, CommentStatus
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from django.db.models import Q

class ArticleListView(View):
    def get(self, request):
        articles = Article.objects.filter(status=ArticleStatus.PUBLISHED)
        if q := request.GET.get('q'):
            articles = articles.filter(Q(title__icontains=q) | Q(content__icontains=q))
        articles = Paginator(articles, 9)
        try:
            page_number = request.GET.get("page")
            articles = articles.get_page(page_number)
        except PageNotAnInteger:
            articles = articles.get_page(1)
        except EmptyPage:
            articles = articles.get_page(1)

        return render(request, 'articles/articles.html', {'articles': articles})
    


class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug = slug)
        comments = Comment.objects.filter(article = article, status = CommentStatus.APPROVED)
        return render(request, 'articles/article_detail.html', {'article':article, 'comments':comments})