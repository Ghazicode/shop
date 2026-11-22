from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='list'),
    path('<slug:slug>/detail/', views.ArticleDetailView.as_view(), name='detail'),
    path('<slug:slug>/comments/', views.AddArticleComment.as_view(), name='comments'),
]