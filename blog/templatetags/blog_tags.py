from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


# simple_tag: обрабатывает данные и возвращает строку
@register.simple_tag
def total_posts():
    # возвращает общее количество опубликованных постов на сайте
    return Post.objects.filter(status='published').count()


# inclusion_tag: обрабатывает данные и возвращает обработанный шаблон
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    # возвращает словарь последних опубликованных постов (по умолчанию 5) в виде ссылок на шаблон latest_post.html
    latest_posts = Post.objects.filter(status='published').order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# simple_tag: обрабатывает данные и возвращает строку
@register.simple_tag
def get_most_commented_posts(count=5):
    # возвращает 5 (по умолчанию) наиболее комментируемых постов
    return Post.objects.filter(status='published').annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

# Создание тегов шаблонизатора Django :
# https://pocoz.gitbooks.io/django-v-primerah/content/rasshirenie-prilozheniya-blog/sozdanie-kastomizirovannyh-shablonov-tegov-i-filtrov/sozdanie-tegov-shablonizatora-django.html
# Django документация - https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/