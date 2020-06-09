from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):

    changefreq = 'weekly'  # changefreq и priority указывают на частоту изменения страниц post и их релевантность
    priority = 0.9         # на веб-сайте (максимальное значение равно 1)

    def items(self):
        """возвращает QuerySet объектов, включаемых в эту схему сайта"""
        return Post.objects.filter(status='published')

    @staticmethod  # ?
    def lastmod(obj):
        """получает каждый объект, возвращаемый items(), и возвращает последний раз, когда объект был изменен"""
        return obj.publish

# Инфрмация о Sitemap
# https://pocoz.gitbooks.io/django-v-primerah/content/rasshirenie-prilozheniya-blog/dobavlenie-sitemap.html
