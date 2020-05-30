from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostListView(ListView):
    """Представление на основе класса"""
    queryset = Post.objects.filter(status='published')  # published
    context_object_name = 'posts'  # переменная для обращения в шаблоне (по умолчанию object_list)
    paginate_by = 3
    template_name = 'blog/post/list.html'  # по умолчанию blog/post_list.html


# def post_list(request):
#     """Представление на основе функции"""
#     object_list = Post.objects.all()
#     paginator = Paginator(object_list, 3)  # 3 posts in each page
#     page = request.GET.get('page')  # запрос номера страници
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, 'blog/post/detail.html', {'post': post})

