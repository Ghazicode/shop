from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels 
User = get_user_model()


class ArticleStatus(models.TextChoices):
    DRAFT = 'draft', 'پیش‌نویس'
    PUBLISHED = 'published', 'منتشر شده'
    ARCHIVED = 'archived', 'بایگانی شده'

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='articles/')
    content = models.TextField()
    read_time = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='articles')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='articles')
    slug = models.SlugField(unique=True, max_length=250)
    status = models.CharField(max_length=10,choices=ArticleStatus.choices, default=ArticleStatus.DRAFT)
    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)

    def get_summary(self):
        if(len(self.content) < 40):
            return self.content[:40]
        return f"{self.content[:50]}..."

    def __str__(self):
        return self.title
    

    class Meta:
        ordering = ['-id', ]


class Tag(models.Model):
    title = models.CharField(max_length=250, unique=True)
    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)


    def __str__(self):
        return self.title
    






class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)

    def __str__(self):
        return self.title
    



class CommentStatus(models.TextChoices):
    PENDING = 'pending', 'در انتظار تأیید'
    APPROVED = 'approved', 'تأیید شده'
    REJECTED = 'rejected', 'رد شده'



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    fullname = models.CharField(max_length=250)
    comment = models.TextField()
    status = models.CharField(max_length=10,choices=CommentStatus.choices, default=CommentStatus.PENDING)
    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)



    def __str__(self):
        return self.article.title

