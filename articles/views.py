from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Article, Tag, Category, Comment, ArticleStatus, CommentStatus
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm
from django.contrib import messages


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
        articles = Article.objects.filter(status = ArticleStatus.PUBLISHED).exclude(slug = slug)[:3]
        comments = Comment.objects.filter(article = article, status = CommentStatus.APPROVED)
        form = CommentForm()
        comments = Paginator(comments, 5)
        try:
            page_number = request.GET.get("page")
            comments = comments.get_page(page_number)
        except PageNotAnInteger:
            comments = comments.get_page(1)
        except EmptyPage:
            comments = comments.get_page(1)
        return render(request, 'articles/article_detail.html', {'article':article, 'comments':comments, 'form':form, 'articles':articles})
    
        


class AddArticleComment(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        form = CommentForm(request.POST)
        article = get_object_or_404(Article, slug = slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
        else:
            messages.error(request, 'اطلاعات را به درستی وارد نمایید')
        return redirect('articles:detail', slug)

            


    