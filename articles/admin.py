from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models


@admin.register(models.Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

    list_display = (
        'title',
        'author',
        'category',
        'status',
        'read_time',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
    )

    search_fields = (
        'title',
        'content',
        'author__email',
    )



    autocomplete_fields = ('author', 'category')

    list_select_related = ('author', 'category')


    @admin.display(description='تعداد نظرات')
    def comments_count(self, obj):
        return obj.comments.count()

    actions = (
        'publish_articles',
        'archive_articles',
        'draft_articles',
    )

    @admin.action(description='انتشار مقالات انتخاب‌شده')
    def publish_articles(self, request, queryset):
        queryset.update(status='published')

    @admin.action(description='بایگانی مقالات انتخاب‌شده')
    def archive_articles(self, request, queryset):
        queryset.update(status='archived')

    @admin.action(description='تبدیل به پیش‌نویس')
    def draft_articles(self, request, queryset):
        queryset.update(status='draft')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'articles_count',
        'created_at',
    )

    search_fields = ('title', 'slug')

    prepopulated_fields = {
        'slug': ('title',)
    }



    @admin.display(description='تعداد مقالات')
    def articles_count(self, obj):
        return obj.articles.count()


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'articles_count',
        'created_at',
    )

    search_fields = ('title',)


    @admin.display(description='تعداد مقالات')
    def articles_count(self, obj):
        return obj.articles.count()


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'fullname',
        'author',
        'article',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'fullname',
        'comment',
        'author__email',
        'article__title',
    )

    autocomplete_fields = (
        'author',
        'article',
    )

    list_editable = ('status',)

    list_select_related = (
        'author',
        'article',
    )



    actions = (
        'approve_comments',
        'reject_comments',
        'pending_comments',
    )

    @admin.action(description='تأیید نظرات انتخاب‌شده')
    def approve_comments(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='رد نظرات انتخاب‌شده')
    def reject_comments(self, request, queryset):
        queryset.update(status='rejected')

    @admin.action(description='انتقال به انتظار تأیید')
    def pending_comments(self, request, queryset):
        queryset.update(status='pending')