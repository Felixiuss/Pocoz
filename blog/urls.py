from django.conf.urls import url
from django.urls import path

from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),  # все посты
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),  # поделиться по e-mail
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),  # RSS канал последних новостей
]
# TODO change to path